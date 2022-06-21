import gym
from gym.utils.play import play
import pygame
import gym_examples


env = gym.make('NovelGridWorlds-v2')

n_agents = 1
i = 0

observation, info = env.reset(return_info=True)

for _ in range(1000):
    for i in n_agents:
        observation, reward, done, info = env.step(env.action_space[i].sample())
        env.render()

        if done:
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