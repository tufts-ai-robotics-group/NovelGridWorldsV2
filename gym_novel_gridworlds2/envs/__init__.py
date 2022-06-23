from gym_novel_gridworlds_2 import NovelGridWorldEnv
from gym.envs.registration import register

register(
    id='NovelGridWorlds-v2',
    entry_point='gym_novel_gridworlds2.envs:NovelGridWorldEnv',
    max_episode_steps=1000,
)
