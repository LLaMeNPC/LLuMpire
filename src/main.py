import sys, stats
from api.gemini import Gemini
from umpire import Umpire
from log import log, log_program_start
from console_utils import cls, choice, get_element_from_choice



log_program_start()

if len(sys.argv) == 1:
    cls()
    view_mode_options = [
        "Alterations",
        "Stats"
    ]
    print("You are running LLuMpire in view mode. To run LLuMpire on output, please give a data file as argument.")
    print("What do you want to view?")
    user_choice = get_element_from_choice(choice(view_mode_options), view_mode_options)
    
    if user_choice == "Alterations":
        pass
    elif user_choice == "Stats":
        stats.user_initialize()
else:
    api = Gemini()
    umpire = Umpire(api)
    log("Config:", umpire.config)
    umpire.judge(sys.argv[1])
