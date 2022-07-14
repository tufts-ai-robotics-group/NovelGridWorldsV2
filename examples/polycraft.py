import pathlib
import time
import argparse

import json

from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
from gym_novel_gridworlds2.utils.json_parser import ConfigParser

# file_name = "automaptest.json"

parser = argparse.ArgumentParser(description='Polycraft Environment')
parser.add_argument('filename', type=str, nargs=1,
                    help='the path of the config file')

args = parser.parse_args()
file_name = args.filename[0]

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name
with open(config_file_path, "r") as f:
    config_content = json.load(f)

# print(state)
env = NovelGridWorldSequentialEnv(config_dict=config_content, MAX_ITER=1000)

num_episodes = config_content.get("num_episodes") or 1000
novelties = config_content.get("novelties")

last_agent = env.possible_agents[-1]

for episode in range(num_episodes):
    print()
    print("++++++++++++++ Running episode", episode, "+++++++++++++++")
    print()
    env.reset(return_info=True, options={"episode": episode})
    for agent in env.agent_iter():
        observation, reward, done, info = env.last()
        action = env.agent_manager.agents[agent].agent.policy(observation)
        env.step(action)

        if agent == last_agent:
            env.render()
            time.sleep(0.05)

env.close()
