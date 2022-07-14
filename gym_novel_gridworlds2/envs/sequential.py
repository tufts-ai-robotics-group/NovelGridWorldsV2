import numpy as np
import functools
import pygame
from copy import deepcopy
from typing import List

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from pettingzoo.utils import wrappers
from gym.spaces import MultiDiscrete

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError
from gym_novel_gridworlds2.utils.novelty_injection import inject_novelty

from ..agents import Agent, AgentManager
from ..state.dynamic import Dynamic
from ..state.state import State
from ..utils.MultiAgentActionSpace import MultiAgentActionSpace
from ..utils.json_parser import ConfigParser


class NovelGridWorldSequentialEnv(AECEnv):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, config_dict: str, MAX_ITER: int = 2000):
        """
        Init
        TODO more docs
        """
        ### custom variables environment
        self.config_dict = config_dict


        self.json_parser = ConfigParser()
        self.state, self.dynamic, self.agent_manager = self.json_parser.parse_json(
            json_content=config_dict
        )
        self.goal_item_to_craft = ""  # TODO add to config
        self.MAX_ITER = MAX_ITER
        ##### Required properties for the environment
        # Agent lists
        self.possible_agents = self.agent_manager.get_possible_agents()
        self.agent_name_mapping = self.agent_manager.get_agent_name_mapping()

        # The agent is done when it's killed or when the goal is reached.
        self.dones = {key: False for key, a in self.agent_manager.agents.items()}

        # spaces: we get from the agent
        self._action_spaces = {
            key: a.agent.get_action_space()
            for key, a in self.agent_manager.agents.items()
        }
        self._observation_spaces = {
            key: a.agent.get_observation_space(self.state._map.shape, 10)
            for key, a in self.agent_manager.agents.items()
        }

        # rendering
        self.window = None

    def observe(self, agent_name):
        return self.agent_manager.get_agent(agent_name).agent.get_observation()

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        return self._observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        return self._action_spaces[agent]

    def step(self, action):
        """
        TAKEN FROM
        https://www.pettingzoo.ml/environment_creation#example-custom-environment

        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - dones
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        if self.dones[self.agent_selection]:
            # handles stepping an agent which is already done
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next done agent,  or if there are no more done agents, to the next live agent
            return self._was_done_step(None)

        agent = self.agent_selection

        # do the action
        action_set = self.agent_manager.get_agent(agent).action_set
        agent_entity = self.agent_manager.get_agent(agent).entity
        # TODO only print when verbose
        print(
            "{:<12}  {:<12} | action_picked: {:<12}".format(
                agent, agent_entity.name, action_set.actions[action][0]
            )
        )
        print(agent_entity.inventory)
        try:
            action_set.actions[action][1].do_action(agent_entity)
        except PreconditionNotMetError:
            pass

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # collect reward if it is the last agent to act
        if self._agent_selector.is_last():
            # rewards for all agents are placed in the .rewards dictionary
            # self.rewards[self.agents[0]], self.rewards[self.agents[1]] = REWARD_MAP[
            #     (self.state[self.agents[0]], self.state[self.agents[1]])
            # ]
            # TODO: rewards
            self.rewards = {agent: 0 for agent in self.possible_agents}

            self.num_moves += 1
            # The dones dictionary must be updated for all players.
            self.dones = {
                agent: self.num_moves >= self.MAX_ITER for agent in self.agents
            }
        else:
            # necessary so that observe() returns a reasonable observation at all times.
            # no rewards are allocated until both players give an action
            self._clear_rewards()

        # selects the next agent.
        self.agent_selection = self._agent_selector.next()
        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

    def reset(self, seed=None, return_info=False, options=None):
        """
        Resets the novelty and injects novelty
        """
        
        ## injection of novelty
        episode = 0
        if options is not None:
            episode = options.get("episode") or 0
        
        if str(episode) in (self.config_dict.get("novelties") or {}):
            self.config_dict = inject_novelty(self.config_dict,  self.config_dict["novelties"][str(episode)])

        # initialization
        self.state, self.dynamic, self.agent_manager = self.json_parser.parse_json(
            json_content=self.config_dict
        )

        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.num_moves = 0

        # Agent
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()
        return self.state._map, None

    def render(self, mode="human"):
        print(self.state.mapRepresentation())
        print("-----------------------------")

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
