import sys, math, os

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

def cls():
    print(chr(27) + "[2J")
    #os.system('cls' if os.name=='nt' else 'clear')

def choice(ls):
    for i, le in enumerate(ls):
        print(f"  {i}) {le}")
    return input("Please select an option: ")

def get_element_from_choice(choice, ls):
    for i, le in enumerate(ls):
        if choice == str(i) or choice == le:
            return le
        elif i == len(ls) - 1:
            cls()
            print(f"Option \"{choice}\" not recognized")
            return None

def queue_exit():
    user_input = ""
    while user_input != "q":
        if user_input == "":
            user_input = input("Input q to exit: ")
        else:
            user_input = input(f"\"{user_input}\" not recognized, input q to exit: ")
        delete_last_line()

def digit_percentage(*digit_tups):
    value = 0
    max_value = 1
    for digit, max_digit in reversed(digit_tups):
        value += digit * max_value
        max_value *= max_digit
    return value / (max_value - 1)            
