import numpy as np
import functools
import pygame
from copy import deepcopy
from typing import List
import time

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector
from pettingzoo.utils import wrappers
from gym.spaces import MultiDiscrete

from gym_novel_gridworlds2.actions.action import PreconditionNotMetError
from gym_novel_gridworlds2.utils.novelty_injection import inject

from ..utils.json_parser import ConfigParser


class NovelGridWorldSequentialEnv(AECEnv):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, config_dict: str, MAX_ITER: int = 2000, time_limit=5000):
        """
        Init
        TODO more docs
        """
        ### custom variables environment
        self.config_dict = config_dict

        self.json_parser = ConfigParser()
        (
            self.internal_state,
            self.dynamic,
            self.agent_manager,
        ) = self.json_parser.parse_json(json_content=config_dict)
        self.goal_item_to_craft = ""  # TODO add to config
        self.MAX_ITER = MAX_ITER
        ##### Required properties for the environment
        # Agent lists
        self.possible_agents = self.agent_manager.get_possible_agents()
        self.agent_name_mapping = self.agent_manager.get_agent_name_mapping()

        # The agent is done when it's killed or when the goal is reached.
        self.dones = {key: False for key, a in self.agent_manager.agents.items()}

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

    def was_done_metadata(self, extra_params, agent):
        """
        Sends a dummy metadata to the agent.
        """
        # The reason is that agent selects an action before
        # the check_done action is called so it will still get a second
        # extra action (after the delay) and we will need to send a message back
        # to the agent.
        metadata = {}
        metadata["goal"] = {
            "goalType": "ITEM",
            "goalAchieved": self.internal_state.goalAchieved,
            "Distribution": "Uninformed",
        }
        metadata["step"] = self.num_moves
        metadata["gameOver"] = True
        metadata["command_result"] = {
            "command": extra_params.get("_command"),
            "argument": extra_params.get("_raw_args") or "",
            "result": "SUCCESS",
            "message": "",
            "stepCost": 0,  # TODO cost
        }
        self.agent_manager.agents[agent].agent.update_metadata(metadata)

    def step(self, action, extra_params={}):
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
        if self.agent_selection == self.agents[0]:
            print(f"--------------------- step {self.num_moves} ---------------------")
        self.internal_state.time_updates()

        # reset rewards for current step ("stepCost")
        self.rewards = {agent: 0 for agent in self.possible_agents}

        agent = self.agent_selection

        if self.dones[self.agent_selection]:
            # handles stepping an agent which is already done
            # accepts a None action for the one agent, and moves the agent_selection to
            # the next done agent,  or if there are no more done agents, to the next live agent
            return self._was_done_step(None)

        # set to be done if the agent is done
        # DELAYED one round
        self.dones[agent] = (
            self.internal_state.given_up or self.internal_state.goalAchieved
        )

        # do the action
        action_set = self.agent_manager.get_agent(agent).action_set
        agent_entity = self.agent_manager.get_agent(agent).entity
        # self.agent_manager.update_agent(agent, self.internal_state)
        # TODO only print when verbose
        print(
            "------- {:<12}  {:<12} | action_picked: {:<15} [{}]".format(
                agent,
                agent_entity.nickname,
                action_set.actions[action][0],
                extra_params,
            )
        )
        if agent_entity.nickname == "main_1":
            self.internal_state.selected_action = action_set.actions[action][0]
        # print(agent_entity.inventory)
        metadata = {}

        step_cost = action_set.actions[action][1].get_step_cost(agent_entity, **extra_params) or 0

        try:
            metadata = action_set.actions[action][1].do_action(
                agent_entity, **extra_params
            )
        except PreconditionNotMetError as e:
            # TODO set an error message
            action_failed = True
            metadata = {
                "command_result": {
                    "command": extra_params.get("_command")
                    or action_set.actions[action][0],
                    "argument": extra_params.get("_raw_args") or "",
                    "result": "FAILED",
                    "message": e.message if hasattr(e, "message") else "",
                    "stepCost": step_cost,  # TODO cost
                }
            }
            pass

        self.rewards[agent] -= step_cost

        # send the metadata of the command execution result
        # to the agent (mostly for use in the socket connection)
        # TODO: rn accomodating the string
        if metadata is None:
            metadata = {}
        if type(metadata) == str:
            self.agent_manager.agents[agent].agent.update_metadata(metadata)
        else:
            metadata["goal"] = {
                "goalType": "ITEM",
                "goalAchieved": self.dones[agent] and self.internal_state.goalAchieved,
                "Distribution": "Uninformed",
            }
            metadata["step"] = self.num_moves
            # TODO below is delayed by one step
            metadata["gameOver"] = self.dones[agent]
            if "command_result" not in metadata:
                metadata["command_result"] = {
                    "command": extra_params.get("_command")
                    or action_set.actions[action][0],
                    "argument": extra_params.get("_raw_args") or "",
                    "result": "SUCCESS",
                    "message": "",
                    "stepCost": step_cost,
                }
            self.agent_manager.agents[agent].agent.update_metadata(metadata)

        # print inventory info
        print("inventory:", agent_entity.inventory)

        # the agent which stepped last had its _cumulative_rewards accounted for
        # (because it was returned by last()), so the _cumulative_rewards for this
        # agent should start again at 0
        self._cumulative_rewards[agent] = 0

        # collect reward if it is the last agent to act.
        # if the action allows an additional action to be done immediately
        # after it, (like SENSE_ALL in polycraft)
        # then don't update info until the next action is done.
        if (
            self._agent_selector.is_last()
            and not action_set.actions[action][1].allow_additional_action
        ):  # if
            # rewards for all agents are placed in the .rewards dictionary
            # self.rewards[self.agents[0]], self.rewards[self.agents[1]] = REWARD_MAP[
            #     (self.internal_state[self.agents[0]], self.internal_state[self.agents[1]])
            # ]
            # TODO: rewards

            self.num_moves += 1

            # update of done, by setting game_over
            # to test: stepCost and max_step_cost
            self.internal_state.given_up = (
                self.internal_state.given_up
                or time.time() - self.initial_time > self.time_limit
            )
            self.internal_state.given_up = (
                self.internal_state.given_up
                or self._cumulative_rewards[agent]
                > self.agent_manager.get_agent(agent).max_step_cost
            )

            # The dones dictionary must be updated for all players.
            # TODO a super RESET command should terminate everything
            self.dones = {
                agent: self.dones[agent] or self.num_moves >= self.MAX_ITER
                for agent in self.agents
            }

        else:
            # necessary so that observe() returns a reasonable observation at all times.
            # no rewards are allocated until both players give an action
            self._clear_rewards()

        # selects the next agent.
        if not action_set.actions[action][1].allow_additional_action:
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
            self.config_dict = inject(
                self.config_dict, self.config_dict["novelties"][str(episode)]
            )

        # initialization
        (
            self.internal_state,
            self.dynamic,
            self.agent_manager,
        ) = self.json_parser.parse_json(json_content=self.config_dict)

        #### agent novelties
        self.possible_agents = self.agent_manager.get_possible_agents()
        self.agent_name_mapping = self.agent_manager.get_agent_name_mapping()

        # more reset
        self.agents = self.possible_agents[:]
        self.rewards = {agent: 0 for agent in self.agents}
        self._cumulative_rewards = {agent: 0 for agent in self.agents}
        self.dones = {agent: False for agent in self.agents}
        self.infos = {agent: {} for agent in self.agents}
        self.num_moves = 0

        # Agent
        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.next()

        # reset timer
        self.initial_time = time.time()
        return self.internal_state._map, None

    def renderTextCenteredAt(self, text, font, colour, x, y, screen, allowed_width):
        # first, split the text into words
        words = text.split()

        # now, construct lines out of these words
        lines = []
        while len(words) > 0:
            # get as many words as will fit within allowed_width
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(" ".join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            # add a line consisting of those words
            line = " ".join(line_words)
            lines.append(line)

        # now we've split our text into lines that fit into the width, actually
        # render them

        # we'll render each line below the last, so we need to keep track of
        # the culmative height of the lines we've rendered so far
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            # (tx, ty) is the top-left of the font surface
            tx = x - fw / 2
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh

    def render(self, mode="human"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        self.internal_state.SCREEN.fill((171, 164, 164))
        self.internal_state.drawMap()

        font = pygame.font.Font("freesansbold.ttf", 18)

        # north
        facing_text = font.render("North: -->", True, (0, 0, 0))
        facing_rect = facing_text.get_rect()
        facing_rect.center = (900, 60)
        self.internal_state.SCREEN.blit(facing_text, facing_rect)

        # step
        step_text = font.render(
            "Step:" + str(self.internal_state._step_count), True, (0, 0, 0)
        )
        step_rect = step_text.get_rect()
        step_rect.center = (1120, 30)
        self.internal_state.SCREEN.blit(step_text, step_rect)

        agent = self.internal_state.get_objects_of_type("agent")[0]

        # facing
        facing_text = font.render("Agent Facing:" + str(agent.facing), True, (0, 0, 0))
        facing_rect = facing_text.get_rect()
        facing_rect.center = (1120, 60)
        self.internal_state.SCREEN.blit(facing_text, facing_rect)

        # selected action
        action_text = font.render(
            "Selected Action:" + str(self.internal_state.selected_action),
            True,
            (0, 0, 0),
        )
        action_rect = action_text.get_rect()
        action_rect.center = (1120, 90)
        self.internal_state.SCREEN.blit(action_text, action_rect)

        black = (0, 0, 0)

        # step cost
        cost_text = font.render(
            "total cost:" + str(self._cumulative_rewards["agent_" + str(agent.id)]),
            True,
            (0, 0, 0),
        )
        print(self._cumulative_rewards)
        cost_rect = cost_text.get_rect()
        cost_rect.center = (1120, 110)
        self.internal_state.SCREEN.blit(cost_text, cost_rect)

        #### inventory
        self.internal_state.renderTextCenteredAt(
            "Agent Inventory:",
            font,
            black,
            1130,
            140,
            self.internal_state.SCREEN,
            200,
        )
        inv_text = "\n".join(
            [
                "{}: {:>4}".format(item, quantity)
                for item, quantity in agent.inventory.items()
            ]
        )
        self.internal_state.renderMultiLineTextRightJustifiedAt(
            inv_text,
            font,
            black,
            1200,
            160,
            self.internal_state.SCREEN,
            200,
        )


        #### goal reached statement
        if self.internal_state.goalAchieved or self.internal_state.given_up:
            timer = 4
            if self.internal_state.given_up:
                game_over_str = f"Given Up. Restarting soon..."
            else:
                game_over_str = f"You Won. Restarting soon..."
            win_text = font.render(game_over_str, True, (255, 0, 0))
            win_rect = win_text.get_rect()
            win_rect.center = (1120, 530)
            self.internal_state.SCREEN.blit(win_text, win_rect)
            for i in range(timer * 2):
                pygame.display.update()
                time.sleep(0.5)

        pygame.display.update()

    def close(self):
        if hasattr(self, "window") and self.window is not None:
            pygame.display.quit()
            pygame.quit()
