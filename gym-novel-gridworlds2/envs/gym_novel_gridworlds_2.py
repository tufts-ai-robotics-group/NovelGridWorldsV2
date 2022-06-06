import gym

class NovelGridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def step(self, action_n):
        obs_n    = list()
        reward_n = list()
        done_n   = list()
        info_n   = {'n': []}
        # ...
        return obs_n, reward_n, done_n, info_n
