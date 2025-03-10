import datetime

log_file_path = "logs/{}.txt"

def log(command, output=None):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time().strftime('%H:%M:%S')

    current_log_file_path = log_file_path.format(date)
    with open(current_log_file_path, 'a') as file:
        file.write(f"{time} {command}\n\n")
        if output is not None:
            file.write(f"\t{output}\n\n")

def log_program_start():
    log("---------------- program start ----------------")
