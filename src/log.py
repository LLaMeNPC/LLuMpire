import datetime

log_file_path = "logs/{}.txt"

def _log(command, output=None, include_timestamp = False, include_newlines = False):
    date = datetime.datetime.now().date()
    time = datetime.datetime.now().time().strftime('%H:%M:%S')

    current_log_file_path = log_file_path.format(date)
    with open(current_log_file_path, 'a') as file:
        file.write(f"{f"{time} " if include_timestamp else ""}{command}{"\n\n" if include_newlines or output is not None else ""}")
        if output is not None:
            file.write(f"\t{output}{"\n\n" if include_newlines else ""}")

def log(command, output=None):
    _log(command, output, True, True)

def log_program_start():
    log("---------------- program start ----------------")
