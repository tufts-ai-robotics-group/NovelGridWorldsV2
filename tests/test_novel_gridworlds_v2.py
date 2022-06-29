from gym_novel_gridworlds2.utils.json_parser import ConfigParser
import gym
from gym.utils.play import play
import pygame
import numpy as np
import pathlib


def test_novel_gridworlds():
    file_name = "specificationtest2.json"

    json_parser = ConfigParser()
    config_file_path = pathlib.Path(__file__).parent.resolve() / file_name
    state, dynamic, agent_manager = json_parser.parse_json(config_file_path)

    print(state)
    env = gym.make('NovelGridWorldEnv', state=state, dynamic=dynamic, agent_manager=agent_manager)

    n_agents = 1
    i = 0

    observation, info = env.reset(return_info=True)

    for _ in range(1000):
        for i in range(n_agents):
            # randomly sample
            action_picked = env.action_space[i].sample()

            # all zeros unless it's the picked agent
            actions = np.zeros(n_agents)
            actions[i] = action_picked
            observation, reward, done, info = env.step(actions)
            env.render()

            if done.all():
                observation, info = env.reset(return_info=True)
                print(observation)

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
