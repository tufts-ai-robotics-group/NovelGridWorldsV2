from copy import deepcopy
from typing import List
import gym
from gym import spaces
import pygame

from gym_novel_gridworlds2.agents import Agent
from gym_novel_gridworlds2.agents.agent_manager import AgentManager
from gym_novel_gridworlds2.state.dynamic import Dynamic
from gym_novel_gridworlds2.utils.MultiAgentActionSpace import MultiAgentActionSpace
import numpy as np

from ..utils.json_parser import ConfigParser

from ..state.state import State
from gym.spaces import MultiDiscrete
import json

class NovelGridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, state: State, dynamic: Dynamic, agent_manager: AgentManager):
        self.reset_info = {
            "state": deepcopy(state),
            "dynamic": deepcopy(dynamic)
        }
        #
        self.state = state
        self.dynamic = dynamic
        self.agent_manager = agent_manager
        self.action_space = self.dynamic.action_space
        self.observation_space = MultiDiscrete(state._map.shape)
        self.goal_item_to_craft = ""
    
    def generate_observation(self, state):
        return self.state._map

    def step(self, action_n):
        obs      = self.state
        reward_n = np.zeros(self.agent_manager.agent_count)
        done_n   = np.ones(self.agent_manager.agent_count)
        info_n   = []
        for agent_id, action in enumerate(action_n):
            if action != 0: 
                print(agent_id, action)
                self.agent_manager.do_action(agent_id, int(action))

            # .. execute th action
        return obs, reward_n, done_n, info_n

    def reset(self, seed=None, return_info=False, options=None):
        # TODO check if deepcopy works well
        self.state = deepcopy(self.reset_info['state'])
        self.dynamic = deepcopy(self.reset_info['dynamic'])
        return self.state._map, None

    def render(self, mode):
        pass

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
