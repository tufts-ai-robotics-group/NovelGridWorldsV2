import pathlib
import time
import argparse

import json
from typing import Optional
from gym_novel_gridworlds2.actions.action import Action

from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
from gym_novel_gridworlds2.utils.game_report import report_game_result
from gym_novel_gridworlds2.utils.json_parser import ConfigParser, load_json
from gym_novel_gridworlds2.utils.game_report import get_game_time_str

import pygame

parser = argparse.ArgumentParser(description="Polycraft Environment")
parser.add_argument("filename", type=str, nargs=1, help="The path of the config file.")
parser.add_argument(
    "-n",
    "--episodes",
    type=int,
    nargs=1,
    help="The number of episodes.",
    required=False,
)

args = parser.parse_args()
file_name = args.filename[0]
num_episodes = (
    args.episodes[0] if args.episodes is not None and len(args.episodes) > 0 else None
)

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name

config_content = load_json(config_file_path)
print()

if num_episodes is None:
    num_episodes = config_content.get("num_episodes") or 1000
print(f"Running {num_episodes} episodes")
sleep_time = config_content.get("sleep_time") or 0.05
time_limit = config_content.get("time_limit") or 200
novelties = config_content.get("novelties")

env = NovelGridWorldSequentialEnv(
    config_dict=config_content, MAX_ITER=1000, time_limit=time_limit
)

last_agent = env.possible_agents[-1]


for episode in range(num_episodes):
    print()
    print("++++++++++++++ Running episode", episode, "+++++++++++++++")
    print()
    env.reset(return_info=True, options={"episode": episode})
    # TODO change way of reporting novelty
    # if str(episode) in (env.config_dict.get("novelties") or {}):
    #     novelty_str = (
    #         "++++++++++++++ INJECTING NOVELTY AT EPISODE "
    #         + str(episode)
    #         + " "
    #         + str(env.config_dict["novelties"][str(episode)])
    #         + "+++++++++++++++\n"
    #     )
    #     print(novelty_str)
    #     output_log_path = "novelty_log_" + get_game_time_str() + ".csv"
    #     with open(output_log_path, "a") as output_log:
    #         output_log.write(novelty_str)
    env.render()

    for agent in env.agent_iter():
        action: Optional[int] = None
        while (
            action is None
            or env.agent_manager.get_agent(agent)
            .action_set.actions[action][1]
            .allow_additional_action
        ):
            ## while action is valid, do action.
            if agent not in env.dones or env.dones[agent]:
                # skips the process if agent is done.
                env.step(0, {})
                break

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
# report_game_result(
#     episode=episode,
#     total_steps=env._step_count,
#     total_time=time.time() - env._start_time,
#     success=False,
#     notes="Max step cost reached for agent {agent}.",
# )

