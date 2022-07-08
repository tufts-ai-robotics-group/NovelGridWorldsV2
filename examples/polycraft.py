import pathlib
import time

import json

from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
from gym_novel_gridworlds2.utils.json_parser import ConfigParser

file_name = "automaptest.json"

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name
with open(config_file_path, "r") as f:
    config_content = json.load(f)

# print(state)
env = NovelGridWorldSequentialEnv(
    config_dict=config_content
)

n_agents = 1
i = 0

env.reset(return_info=True)

last_agent = env.possible_agents[-1]

for agent in env.agent_iter(max_iter=100):
    observation, reward, done, info = env.last()
    action = env.agent_manager.agents[agent].agent.policy(observation)
    env.step(action)

    if agent == last_agent:
        env.render()
        time.sleep(0.05)

env.close()
