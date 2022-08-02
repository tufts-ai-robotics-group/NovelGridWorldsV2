import pathlib
import time
import argparse

import json
from typing import Optional
from gym_novel_gridworlds2.actions.action import Action

from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
from gym_novel_gridworlds2.utils.json_parser import ConfigParser, load_json

import pygame

parser = argparse.ArgumentParser(description="Polycraft Environment")
parser.add_argument("filename", type=str, nargs=1, help="the path of the config file")

args = parser.parse_args()
file_name = args.filename[0]

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name

config_content = load_json(config_file_path)

env = NovelGridWorldSequentialEnv(config_dict=config_content, MAX_ITER=1000)

num_episodes = config_content.get("num_episodes") or 1000
sleep_time = config_content.get("sleep_time") or 0.05
novelties = config_content.get("novelties")

last_agent = env.possible_agents[-1]


for episode in range(num_episodes):
    print()
    print("++++++++++++++ Running episode", episode, "+++++++++++++++")
    print()
    env.reset(return_info=True, options={"episode": episode})
    env.render()
    for agent in env.agent_iter():
        action: Optional[int] = None
        while action is None or \
                env.agent_manager.get_agent(agent).action_set.actions[action][1].allow_additional_action:
            observation, reward, done, info = env.last()
            result = env.agent_manager.agents[agent].agent.policy(observation)

            # getting the actions
            extra_params = {}
            if type(result) == tuple:
                # symbolic agent sending extra params
                action, extra_params = result
            else:
                # rl agent / actions with no extra params
                action = result
            
            env.step(action, extra_params)

            if agent == last_agent:
                env.render()
                time.sleep(sleep_time)

env.close()
