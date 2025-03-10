import sys, math

def delete_last_line():
    "Deletes the last line in the STDOUT"
    # cursor up one line
    sys.stdout.write('\x1b[1A')
    # delete last line
    sys.stdout.write('\x1b[2K')


is_new_progress_bar = True
def print_progress_bar(progress : float):
    global is_new_progress_bar
    #    if progress < 0 or progress > 1:
    #    raise Exception("Invalid progress given")
    if progress == 0.0:
        is_new_progress_bar = True
    if not is_new_progress_bar:
        delete_last_line()
    is_new_progress_bar = False
    progress_string = "█" * math.floor(progress * 50) + "-" * math.ceil((1-progress) * 50) + f"| {progress * 100:.2f}%"
    print(progress_string)
