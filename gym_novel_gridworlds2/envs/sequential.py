import numpy as np
import functools
import pygame
from copy import deepcopy
from typing import List, Tuple
import time

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from pettingzoo.utils import wrappers
from gymnasium.spaces import MultiDiscrete

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError
from gym_novel_gridworlds2.object.entity import Entity
from gym_novel_gridworlds2.utils.novelty_injection import inject

from ..utils.json_parser import ConfigParser
from ..utils.game_report import create_empty_game_result_file, report_game_result
from ..utils.terminal_colors import bcolors

class NovelGridWorldSequentialEnv(AECEnv):
    metadata = {"render_modes": ["human", None]}

    def __init__(self, 
            config_dict: dict, 
            max_time_step: int = 2000, 
            time_limit=5000, 
            run_name=None, 
            render_mode=None,
            logged_agents=[], 
            generate_csv=False, 
            seed=None
        ):
        """
        Init
        TODO more docs
        """
        assert type(logged_agents) == list
        ### custom variables environment
        self.run_name = run_name
        self.config_dict = config_dict
        self.render_mode = render_mode
        if render_mode == "human":
            pygame.display.set_caption(f"NovelGym - {config_dict.get('filename')}")

        self.rng = np.random.default_rng(seed=seed)

        self.json_parser = ConfigParser()
        (
            self.internal_state,
            self.dynamic,
            self.agent_manager
        ) = self.json_parser.parse_json(
            json_content=config_dict, 
            rendering=(render_mode == "human"), 
            rng=self.rng
        )

        self.goal_item_to_craft = ""  # TODO add to config
        self.MAX_ITER = max_time_step
        ##### Required properties for the environment
        # Agent lists
        self.possible_agents = self.agent_manager.get_possible_agents()
        self.agent_name_mapping = self.agent_manager.get_agent_name_mapping()

        # The list of non-environmental agents.
        # Game over when all non-env agents are done.
        # And environmental agents will be automatically terminated
        # when all other active agents are done.
        self.active_non_env_agents = self.agent_manager.get_non_env_agents()

        # the episode will stop when it exceeds time limit.
        self.initial_time = time.time()
        self.time_limit = time_limit

        # spaces: we get from the agent
        self._action_spaces = {
            key: a.agent.get_action_space()
            for key, a in self.agent_manager.agents.items()
        }
        self._observation_spaces = {
            key: a.agent.get_observation_space(self.internal_state._map.shape, 10)
            for key, a in self.agent_manager.agents.items()
        }

        # initialize the game result file
        self.generate_csv = generate_csv
        if self.generate_csv:
            create_empty_game_result_file(self.run_name)

        # initialize the logged agents set
        self.logged_agents = {*logged_agents}


    def observe(self, agent_name):
        return self.agent_manager.get_agent(agent_name).agent.get_observation(
            self.internal_state, self.dynamic
        )

    @functools.lru_cache(maxsize=None)
    def observation_space(self, agent):
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        return self._observation_spaces[agent]

    @functools.lru_cache(maxsize=None)
    def action_space(self, agent):
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces
        return self._action_spaces[agent]

    def step(self, action, extra_params={}):
        """
        TAKEN FROM
        https://www.pettingzoo.ml/environment_creation#example-custom-environment

        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - terminations / truncations
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        agent = self.agent_selection

        if self.terminations[self.agent_selection] or self.truncations[self.agent_selection]:
            # handles stepping an agent which is already done
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next done agent,  or if there are no more done agents, to the next live agent
            return self._was_dead_step(None)

        agent = self.agent_selection

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # stores action of current agent
        self.state[self.agent_selection] = action

        ############# BEGIN EXECUTION ################
        action_set = self.agent_manager.get_agent(agent).action_set
        agent_entity = self.agent_manager.get_agent(agent).entity

        info = {
            "message": ""
        }

        step_cost = action_set.actions[action][1].get_step_cost(agent_entity, **extra_params) or 0
        action_failed = False

        # execution of the action, adding info
        try:
            result = action_set.actions[action][1].do_action(
                agent_entity, **extra_params
            )
            if type(result) is str:
                info["message"] = result
        except PreconditionNotMetError as e:
            # TODO set an error message
            action_failed = True
            info = {
                "message": str(e.message) if hasattr(e, "message") else "",
            }
            pass

        info["success"] = not action_failed
        self.infos[agent] = info
        
        # process step cost
        self.rewards[agent] -= step_cost

        # TODO only print when verbose
        if "agent_{}".format(agent_entity.id) in self.logged_agents:
            self._print_curr_agent_action_info(
                not action_failed, agent, 
                agent_entity.nickname, action_set.actions[action][0], 
                agent_entity, info)

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # collect reward and do scheduled updates if it is the last agent to act.
        # if the action allows an additional action to be done immediately
        # after it, (like SENSE_ALL in polycraft)
        # then don't update info until the next action is done.
        if (
            self._agent_selector.is_last()
            and not action_set.actions[action][1].allow_additional_action
        ):  
            self._check_truncate_env_agents()
            self.num_moves += 1
            self.internal_state.time_updates()

        # necessary so that observe() returns a reasonable observation at all times.
        # no rewards are allocated until both players give an action
        self._clear_rewards()

        # selects the next agent, unless the action that the current
        # agent has taken an action that allows for 
        # an additional action in the round.
        if not action_set.actions[action][1].allow_additional_action \
                    or self.truncations[agent] or self.terminations[agent]:
            self.agent_selection = self._agent_selector.next()

        # Adds .rewards to ._cumulative_rewards
        self._accumulate_rewards()

        # process terminations
        self.truncations[agent] = self.MAX_ITER is not None and self.num_moves > self.MAX_ITER
        self.terminations[agent] = self.internal_state._given_up or self.internal_state._goal_achieved
        if self.truncations[agent] or self.terminations[agent] and agent in self.active_non_env_agents:
            self.active_non_env_agents.remove(agent)

        if self.render_mode == "human":
            self.render()

    
    def _check_truncate_env_agents(self):
        """
        Checks and sets all agent to be done based on if the whole world is over
        """
        # stop the world, by truncating all environment agents
        if len(self.active_non_env_agents) <= 0:
            for agent in self.possible_agents:
                if not self.terminations[agent]:
                    self.truncations[agent] = True


    def _print_curr_agent_action_info(self, 
            is_success: bool, agent_name: str, 
            agent_nickname: str, action_name: str, 
            agent_entity: Entity, info: dict
        ):
        if is_success:
            colorized_result = bcolors.OKGREEN + "SUCCESS" + bcolors.ENDC
        else:
            colorized_result = " " + bcolors.FAIL + "FAILED" + bcolors.ENDC
        print(
            " {:>4} | [{}] | {:<12}  {:<12} | action_picked: {:<15}".format(
                self.num_moves,
                colorized_result,
                agent_name,
                agent_nickname,
                action_name,
            )
        )

        # print inventory info
        agent_entity.print_agent_status()
        if not is_success:
            print("Info:", info)


    def reset(self, seed=None, return_info=False, options=None):
        """
        Resets the novelty and injects novelty
        """
        if seed is not None:
            # print("Setting seed to", seed)
            self.rng = np.random.default_rng(seed=seed)

        ## injection of novelty
        episode = 0
        if options is not None:
            episode = options.get("episode") or 0

        if str(episode) in (self.config_dict.get("novelties") or {}):
            self.config_dict = inject(
                self.config_dict, self.config_dict["novelties"][str(episode)]
            )

        # initialization
        (
            self.internal_state,
            self.dynamic,
            self.agent_manager,
        ) = self.json_parser.parse_json(
            json_content=self.config_dict, 
            episode=episode,
            rng = self.rng,
            rendering=(self.render_mode == "human"),
        )

        #### agent novelties
        self.possible_agents = self.agent_manager.get_possible_agents()
        self.agent_name_mapping = self.agent_manager.get_agent_name_mapping()

        # more reset
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.terminations = {agent: False for agent in self.agents}
        self.truncations = {agent: False for agent in self.agents}
        self.infos = {agent: {"message": "", "success": False} for agent in self.agents}
        self.state = {agent: None for agent in self.agents}
        self.observations = {agent: None for agent in self.agents}
        self.num_moves = 0

        # Agent
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()
        self.active_non_env_agents = self.agent_manager.get_non_env_agents()

        # reset timer
        self.initial_time = time.time()
        return self.internal_state._map, None

    def render(self, mode=None):
        # TODO generalize
        if self.render_mode != "human":
            return
        
        agent = self.internal_state.get_objects_of_type("agent")[0]
        # agent_obj = self.agent_manager.get_agent(f"agent_{agent.id}")
        self.internal_state.renderer.clear_map()
        self.internal_state._draw_map()
        curr_action_set = self.agent_manager.agents["agent_0"].action_set.actions
        curr_action = self.state["agent_" + str(agent.id)]
        self.internal_state.renderer.draw_info(
            episode=self.internal_state.episode,
            step_count=self.internal_state._step_count,
            agent_facing=agent.facing,
            selected_action=curr_action_set[curr_action][0] if curr_action is not None else None,
            agent_selected_item=agent.selectedItem,
            total_cost=self._cumulative_rewards["agent_" + str(agent.id)],
            agent_inventory=agent.inventory,
            goal_achieved=self.internal_state._goal_achieved,
            given_up=self.internal_state._given_up
        )

    def close(self):
        if hasattr(self, "window") and self.window is not None:
            pygame.display.quit()
            pygame.quit()
