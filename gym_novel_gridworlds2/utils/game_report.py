from datetime import datetime

time_str = ""

def get_game_time_str():
    global time_str
    if time_str == "":
        time_str = datetime.now().strftime("%y%m%d_%H%M%S")
    return time_str


def get_output_log_path(output_prefix: str = None):
    output_prefix = "results/ngwlog_" + (output_prefix or "") + "_"
    return output_prefix + get_game_time_str() + ".csv"


def report_game_result(
    episode: int,
    total_steps: int,
    total_time: int,
    total_cost: int,
    success: bool,
    notes: str = "",
    output_prefix: str = None,
    output_log_path: str = None,
):
    if output_log_path is None:
        output_log_path = get_output_log_path(output_prefix)
    print(output_log_path)
    with open(output_log_path, "a") as output_log:
        output_log.write(
            f"{episode},{total_steps},{total_time},{total_cost},{success},\"{notes}\"\n")


def create_empty_game_result_file(
    output_prefix: str = None,
    output_log_path: str = None,
):
    if output_log_path is None:
        output_log_path = get_output_log_path(output_prefix)
    with open(output_log_path, "w") as output_log:
        output_log.write(
            f"episode,total_steps,total_time,total_cost,success,notes\n"
        )

