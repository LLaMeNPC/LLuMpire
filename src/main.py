import sys
from api.gemini import Gemini
from umpire import Umpire
from log import log, log_program_start

log_program_start()
api = Gemini()
umpire = Umpire(api)
log("Config:", umpire.config)
umpire.judge(sys.argv[1])
