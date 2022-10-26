import os
import subprocess
import signal
import time
import tempfile
import keyboard
import sys

from datetime import datetime

# given the json file, initialize the episode using the file to instantiate the env
def init_episode(json_file):
    # assumes that the ade folder is in the same directory as NG2

    print(os.getcwd())

    d_string = "diarchoutput" + get_game_time_str() + str(episode_count + 1) + ".txt"
    p_string = "polycraftoutput" + get_game_time_str() + str(episode_count + 1) + ".txt"

    diarchoutput = open(d_string, "w")
    polycraftoutput = open(p_string, "w")

    polycraft_str = "python polycraft.py" + json_file

    p1 = subprocess.Popen(polycraft_str, shell=True, stdout=subprocess.PIPE)

    time.sleep(1)
    # path to ade
    os.chdir("../../")
    os.chdir("ade")
    print(os.getcwd())

    time.sleep(3)
    # specify correct java path, open output file and begin diarch
    os.system("jenv local 1.8")
    os.system("echo $JAVA_HOME")

    p2 = subprocess.Popen(
        'ant launch -Dmain=com.config.polycraft.PolycraftAgent -Dargs="-gameport 2346"',
        shell=True,
        stdout=subprocess.PIPE,
    )

    while not episode_done:
        diarchline = str(p2.stdout.readline())
        polycraftline = str(p1.stdout.readline())
        print(diarchline)
        diarchoutput.write(diarchline)
        polycraftoutput.write(polycraftline)
        if "TRIAL" in diarchline and "COMPLETED" in diarchline:
            completion_details.append(diarchline)
            for i in range(20):
                diarchline = str(p2.stdout.readline())
                print(diarchline)
            episode_count += 1
            if episode_count == target_episode:
                episode_done = True

    time.sleep(5)

    os.chdir("../")
    os.chdir("/NovelGridworldsv2/examples")
    print(os.getcwd())

    os.killpg(os.getpgid(p1.pid), signal.SIGTERM)
    time.sleep(2)
    os.killpg(os.getpgid(p2.pid), signal.SIGTERM)


time_str = ""


def get_game_time_str():
    global time_str
    if time_str == "":
        time_str = datetime.now().strftime("%y%m%d_%H%M%S")
    return time_str


episode_count = -1  # start at -1 as first episode is 0
novelty_episode = 100  # the episode to inject the novelty in
target_episode = 0
episode_done = False
completion_details = []

# assumes that the ade folder is in the same directory as NG2

print(os.getcwd())

d_string = "diarchoutput" + get_game_time_str() + ".txt"
p_string = "polycraftoutput" + get_game_time_str() + ".txt"

diarchoutput = open(d_string, "w")
polycraftoutput = open(p_string, "w")

p1 = subprocess.Popen(
    "python polycraft.py pre_novelty_diarc.json", shell=True, stdout=subprocess.PIPE
)

# with novelties...
# p1 = subprocess.Popen(
#     "python polycraft.py novelties/break_axe/break_axe_easy.json",
#     shell=True,
#     stdout=subprocess.PIPE,
# )

time.sleep(1)
# path to ade
os.chdir("../../")
os.chdir("ade")
print(os.getcwd())

time.sleep(3)
# specify correct java path, open output file and begin diarch
os.system("jenv local 1.8")
os.system("echo $JAVA_HOME")

p2 = subprocess.Popen(
    'ant launch -Dmain=com.config.polycraft.PolycraftAgent -Dargs="-gameport 2346"',
    shell=True,
    stdout=subprocess.PIPE,
)

while not episode_done:
    if episode_count == novelty_episode:
        pass
        # need to make above shit a function to start everything up
        # recall the function
    diarchline = str(p2.stdout.readline())
    polycraftline = str(p1.stdout.readline())
    print(diarchline)
    diarchoutput.write(diarchline)
    polycraftoutput.write(polycraftline)
    if "TRIAL" in diarchline and "COMPLETED" in diarchline:
        completion_details.append(diarchline)
        for i in range(20):
            diarchline = str(p2.stdout.readline())
            print(diarchline)
        episode_count += 1
        if episode_count == target_episode:
            episode_done = True


time.sleep(5)

diarchoutput.close()
polycraftoutput.close()

# terminate both processes automatically
os.killpg(os.getpgid(p1.pid), signal.SIGTERM)
time.sleep(2)
os.killpg(os.getpgid(p2.pid), signal.SIGTERM)
sys.exit()

###OLD CODE INVOLVING REPORTING GAME DATA###

# episode_count = -1  # start at -1 as first episode is 0
# target_episode = 0
# terminate = False
# episode_done = False
# lines_left = 10
# completion_details = []
# successes = []

# # assumes that the ade folder is in the same directory as NG2

# print(os.getcwd())

# # p1 = subprocess.Popen(["python", "polycraft.py", "pre_novelty_diarc.json"])
# # p1 = subprocess.Popen(
# #     "python polycraft.py pre_novelty_diarc.json", shell=True, stdout=subprocess.DEVNULL
# # )
# # we do DEVNULL so that the output isn't printed out from PC

# # with novelties...
# p1 = subprocess.Popen(
#     "python polycraft.py novelties/break_axe/break_axe_easy.json",
#     shell=True,
#     stdout=subprocess.DEVNULL,
# )

# time.sleep(1)
# # path to ade
# os.chdir("../../")
# os.chdir("ade")
# print(os.getcwd())

# time.sleep(3)
# # specify correct java path, open output file and begin diarch
# os.system("jenv local 1.8")
# os.system("echo $JAVA_HOME")

# file = open("diarchoutput.txt", "w")

# p2 = subprocess.Popen(
#     'ant launch -Dmain=com.config.polycraft.PolycraftAgent -Dargs="-gameport 2346"',
#     shell=True,
#     stdout=subprocess.PIPE,
# )

# while not episode_done:
#     line = str(p2.stdout.readline())
#     print(line)
#     if "TRIAL" in line and "COMPLETED" in line:
#         completion_details.append(line)
#         for i in range(20):
#             line = str(p2.stdout.readline())
#             print(line)
#         episode_count += 1
#         if episode_count == target_episode:
#             episode_done = True
#     if "Goal" in line and "success" in line:
#         successes.append(line)

# print("Completion details:")
# c = 0
# for item in completion_details:
#     item = str(item)
#     episode_index1 = item.find("in") + 3
#     episode_index2 = item.find("sec") + 3
#     print(item)
#     # file.write(item)
#     file.write("episode number: ")
#     file.write(str(c))
#     file.write("\n")
#     file.write("episode time: ")
#     file.write(item[episode_index1:episode_index2])
#     file.write("\n")

#     c += 1

# # for item in successes:
# #     file.write(str(item))
# #     file.write("\n")

# time.sleep(5)
# # can pipe diarch output, but can't pipe output of polycraft without game crash

# file.close()

# # terminate both processes automatically
# os.killpg(os.getpgid(p1.pid), signal.SIGTERM)
# os.killpg(os.getpgid(p2.pid), signal.SIGTERM)

