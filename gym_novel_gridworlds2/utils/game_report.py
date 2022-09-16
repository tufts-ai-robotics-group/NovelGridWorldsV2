from datetime import datetime

time_str = ""

def get_game_time_str():
    global time_str
    if time_str == "":
        time_str = datetime.now().strftime("%y%m%d_%H%M%S")
    return time_str


def report_game_result(
    episode: int,
    total_steps: int,
    total_time: int,
    success: bool,
    notes: str = "",
    output_log_path: str = "game_log_" + get_game_time_str(),
):
    with open(output_log_path, "a") as output_log:
        output_log.write(
            f"{episode},{total_steps},{total_time},{success},\"{notes}\"\n")
