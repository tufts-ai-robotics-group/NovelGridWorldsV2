from typing import List
import gym
from gym import spaces
import pygame

from gym_novel_gridworlds2.agents import Agent
from gym_novel_gridworlds2.state.dynamic import Dynamic
from gym_novel_gridworlds2.utils.MultiAgentActionSpace import MultiAgentActionSpace
import numpy as np

from ..utils.json_parser import ConfigParser

from ..state.state import State
import json

class NovelGridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, state: State, dynamic: Dynamic):
        #
        self.state = state
        self.dynamic = dynamic
        self.action_space = self.dynamic.action_space
        self.goal_item_to_craft = ""

    def step(self, action_n):
        obs      = self.state
        reward_n = np.zeros(len(self.agents))
        done_n   = np.ones(len(self.agents))
        info_n   = []
        for action in action_n:
            if action == 0: 
                continue
            # .. execute th action
        # ...
        return obs, reward_n, done_n, info_n

    def reset(self, seed=None, return_info=False, options=None):
        pass

    def render(self):
        pass

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
