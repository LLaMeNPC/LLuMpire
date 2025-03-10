import time
import json, threading
from api.api import Api
from config_getter import get_config
from console_utils import print_progress_bar
from log import log

class Umpire:

    def __init__(self, api : Api) -> None:
        self.config = get_config()
        self.api = api

    def judge(self, json_file):
        with open(json_file) as json_data:
            data = json.load(json_data)
            alterations = data["output"]
            for i, tup in enumerate(alterations.items()):
                (k, v) = tup
                for j, alteration in enumerate(v):
                    print_progress_bar((j+i*len(v))/(len(alterations) * len(v)-1))
                    threading.Thread(self.judge_alteration(k, alteration)).start()
                    time.sleep(60 / self.config["rpm"])


    def judge_alteration(self, original, alteration):
        prompt = self.config["judge_prompt"].format(original=original, alteration=alteration)
        api_call_result = self.api.request(prompt)
        result_text = api_call_result.get_result_text()
        log(f"------------------------------------------\n\tOriginal: {original}\n\tAlteration: {alteration}", result_text)
