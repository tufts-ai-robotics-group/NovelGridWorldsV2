import pathlib
import time
import argparse

import yaml
from yaml.loader import Loader
from typing import Optional
from gym_novel_gridworlds2.actions.action import Action

from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
from gym_novel_gridworlds2.utils.game_report import report_game_result
from gym_novel_gridworlds2.utils.json_parser import ConfigParser, load_config
from gym_novel_gridworlds2.utils.game_report import get_game_time_str

import pygame
import numpy as np

from gym_novel_gridworlds2.utils.novelty_injection import inject

parser = argparse.ArgumentParser(description="Polycraft Environment")
parser.add_argument("filename", type=str, nargs=1, help="The path of the config file.")
parser.add_argument(
    '--novelty_config',
    type=str,
    help="The filename of the novelty to inject.",
    required=False,
    default=None
)
parser.add_argument(
    "-n",
    "--episodes",
    type=int,
    help="The number of episodes.",
    required=False,
)
parser.add_argument(
    "--exp_name",
    type=str, 
    help="The name of the experiment.", 
    required=False
)
parser.add_argument(
    "--gameport",
    type=int, 
    help="The port where NGW should listen on.", 
    required=False,
    default=2346
)
parser.add_argument(
    "--num_runs",
    type=int,
    help="The number of independent runs.",
    required=False,
    default=1
)
parser.add_argument(
    '--rendering',
    type=str,
    help="The rendering mode.",
    required=False,
    default="human"
)
parser.add_argument(
    '--seed',
    type=str,
    help="The seed.",
    required=False,
    default=None
)




args = parser.parse_args()
file_name = args.filename[0]
num_episodes = args.episodes
exp_name = args.exp_name
gameport = args.gameport
num_runs = args.num_runs
render_mode = args.rendering
seed = args.seed
novelty_file = args.novelty_config

json_parser = ConfigParser()
config_file_path = pathlib.Path(__file__).parent.resolve() / file_name

config_content = load_config(config_file_path)
print()

if num_episodes is None:
    num_episodes = config_content.get("num_episodes") or 1000
print(f"Running {num_episodes} episodes")
sleep_time = config_content.get("sleep_time") or 0.05
time_limit = config_content.get("time_limit") or 200
novelties = config_content.get("novelties")
config_content['filename'] = file_name.split('/')[-1]

# try manually changing the port for evaluation
try:
    config_content['entities']['main_1']['agent']['socket_port'] = gameport
    print("Using port", gameport)
except (KeyError, TypeError) as e:
    pass
# try manually changing the seed from the command line
if seed is not None:
    if seed == "random":
        seed = np.random.randint(0, 100000)
    config_content['seed'] = seed
print("Using seed", config_content['seed'])

# injection of an extra config file if needed.
if novelty_file is not None:
    with open(novelty_file, 'r') as f:
        novelty_config = yaml.load(f, Loader=Loader)
    config_content = inject(config_content, novelty_config)

env = NovelGridWorldSequentialEnv(
    render_mode=render_mode,
    config_dict=config_content, 
    max_time_step=4000, 
    time_limit=time_limit, 
    run_name=exp_name,
    logged_agents=["agent_0"]
)

last_agent = env.possible_agents[-1]


for episode in range(num_episodes):
    print()
    print("++++++++++++++ Running episode", episode, "+++++++++++++++")
    print()
    env.reset(return_info=True, options={"episode": episode})
    env.render(mode=render_mode)

    for agent in env.agent_iter():
        action: Optional[int] = None
        while (
            action is None
            or env.agent_manager.get_agent(agent)
            .action_set.actions[action][1]
            .allow_additional_action
        ):
            ## while action is valid, do action.
            if agent not in env.terminations or env.terminations[agent]:
                # skips the process if agent is done.
                env.step(0, {})
                break

            observation, reward, terminated, truncated, info = env.last()
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
                time.sleep(sleep_time)

env.close()
