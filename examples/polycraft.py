from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
import gym
import numpy as np
import pathlib
import time

from gym_novel_gridworlds2.utils.json_parser import ConfigParser

file_name = "automaptest.json"

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name
state, dynamic, agent_manager = json_parser.parse_json(config_file_path)

# print(state)
env = NovelGridWorldSequentialEnv(
    state=state, dynamic=dynamic, agent_manager=agent_manager
)

n_agents = 1
i = 0

env.reset(return_info=True)

last_agent = env.possible_agents[-1]

for agent in env.agent_iter(max_iter=100):
    observation, reward, done, info = env.last()
    action = agent_manager.agents[agent].agent.policy(observation)
    env.step(action)

    if agent == last_agent:
        env.render()
        time.sleep(0.05)

env.close()
