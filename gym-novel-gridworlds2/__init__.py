from gym.envs.registration import register

register(
    id='NovelGridWorldEnv',
    entry_point='gym_novel_gridworlds2.envs:NovelGridWorldEnv',
)