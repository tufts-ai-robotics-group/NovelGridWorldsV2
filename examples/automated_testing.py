# AUTOMATED TESTING PIPELINE
# Note: must create a diarch compatible JSON file to be used for the config path
# See break_axe_easy_diarch.json vs break_axe_easy.json

import os
import subprocess
import signal
import time
import sys

from datetime import datetime

time_str = ""


def get_game_time_str():
    global time_str
    if time_str == "":
        time_str = datetime.now().strftime("%y%m%d_%H%M%S")
    return time_str


### IMPORTANT: SUPPLY NUMBER OF EPISODES TO RUN AND JSON SPECIFICATION HERE!!! ###
NUM_EPISODES = 2
NG2_CONFIG_PATH = "novelties/break_axe/break_axe_easy_diarch.json"  # relative to examples folder or absolute path
### -------------------------------------------------------------------------- ###

# "pre_novelty_diarc.json"
# "novelties/break_axe/break_axe_easy_diarch.json"

EPISODE_COUNT = 0
done = False

print(os.getcwd())

d_string = "diarchoutput" + get_game_time_str() + ".txt"
p_string = "polycraftoutput" + get_game_time_str() + ".txt"

diarchoutput = open(d_string, "w")
polycraftoutput = open(p_string, "w")

polycraft_str = f"python polycraft.py {NG2_CONFIG_PATH} -n {NUM_EPISODES}"

p1 = subprocess.Popen(polycraft_str, shell=True, stdout=subprocess.PIPE)
print("Loaded polycraft")

time.sleep(1)
# path to ade
os.chdir("../../")
os.chdir("ade")
print(os.getcwd())

time.sleep(3)

p2 = subprocess.Popen(
    'ant launch -Dmain=com.config.polycraft.PolycraftAgent -Dargs="-gameport 2346"',
    shell=True,
    stdout=subprocess.PIPE,
)
print("Started diarch")

while not done:
    diarchline = p2.stdout.readline().decode("unicode-escape")
    polycraftline = p1.stdout.readline().decode("unicode-escape")
    print(diarchline)
    print(polycraftline)
    diarchoutput.write(diarchline)
    polycraftoutput.write(polycraftline)
    if "TRIAL" in diarchline and "COMPLETED" in diarchline:
        for i in range(20):
            diarchline = str(p2.stdout.readline())
        EPISODE_COUNT += 1
        print("FINISHED EPISODE # ", EPISODE_COUNT)
        if EPISODE_COUNT == NUM_EPISODES:
            done = True
    if "Giving up" in diarchline:
        for i in range(20):
            diarchline = str(p2.stdout.readline())
        EPISODE_COUNT += 1
        print("GAVE UP EPISODE # ", EPISODE_COUNT)
        if EPISODE_COUNT == NUM_EPISODES:
            done = True

print("Done! Terminating processes.")
# terminate both processes automatically
os.killpg(os.getpgid(p2.pid), signal.SIGTERM)
time.sleep(2)
os.killpg(os.getpgid(p1.pid), signal.SIGTERM)
sys.exit()
