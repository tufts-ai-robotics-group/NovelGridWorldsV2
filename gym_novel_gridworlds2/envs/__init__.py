from .sequential import NovelGridWorldSequentialEnv
from gymnasium.envs.registration import register

register(
    id='NovelGridWorlds-Sequential-v2',
    entry_point='gym_novel_gridworlds2.envs:NovelGridWorldSequentialEnv',
    max_episode_steps=9600,
)
