import sys
from api.gemini import Gemini
from umpire import Umpire

api = Gemini()
umpire = Umpire(api)
print(sys.argv)
umpire.judge(sys.argv[1])
