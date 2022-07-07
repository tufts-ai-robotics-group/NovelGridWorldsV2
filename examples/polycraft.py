from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
import gym
import numpy as np
import pathlib

from gym_novel_gridworlds2.utils.json_parser import ConfigParser


file_name = "automaptest.json"

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name
state, dynamic, agent_manager = json_parser.parse_json(config_file_path)

print(state)
env = NovelGridWorldSequentialEnv(state=state, dynamic=dynamic, agent_manager=agent_manager)

n_agents = 1
i = 0

env.reset(return_info=True)

for _ in range(1000):
    for agent in env.agent_iter():
        observation, reward, done, info = env.last()
        action = agent_manager.agents[agent].agent.policy(observation)
        env.step(action)
        env.render()

env.close()


# env = gym.make('NovelGridWorlds-v2')

# n_agents = 1
# i = 0

# observation, info = env.reset(return_info=True)

# for _ in range(1000 * n_agents):
#     observation, reward, done, info = env.step(env.action_space[i].sample())
#     env.render()

#     if i == n_agents:
#       i = 0
#     else:
#       i += 1

#     if done:
#         observation, info = env.reset(return_info=True)
#         print(observation)

# env.close()