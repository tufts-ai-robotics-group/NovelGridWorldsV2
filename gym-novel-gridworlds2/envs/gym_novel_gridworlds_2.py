import gym
from gym import spaces
import pygame

class NovelGridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, actions):
        self.action_space = spaces.Discrete(len(actions))
        self.recipes = []
        self.unbreakable_items = []
        self.goal_item_to_craft = ""
        #note: other parameters could be passed in here, like the names of JSON folders

    def step(self, action_n):
        obs_n    = list()
        reward_n = list()
        done_n   = list()
        info_n   = {'n': []}
        # ...
        return obs_n, reward_n, done_n, info_n

    def reset(self, seed=None, return_info=False, options=None):
        pass

    def render(self):
        pass

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

