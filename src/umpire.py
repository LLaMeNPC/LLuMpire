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
        judge_prompts = self.get_judge_prompts()
        print(judge_prompts)
        with open(json_file) as json_data:
            data = json.load(json_data)
            alterations = data["output"]
            for i, tup in enumerate(alterations.items()):
                (k, v) = tup
                for j, alteration in enumerate(v):
                    for x, (judge_prompt_name, judge_prompt) in enumerate(judge_prompts.items()):
                        print_progress_bar((j+i*len(v))/(len(alterations) * len(v)-1))
                        threading.Thread(self.judge_alteration(k, alteration, judge_prompt_name, judge_prompt)).start()
                        time.sleep(60 / self.config["rpm"])


    def judge_alteration(self, original, alteration, judge_prompt_name, judge_prompt):
        prompt = judge_prompt.format(original=original, alteration=alteration)
        api_call_result = self.api.request(prompt)
        result_text = api_call_result.get_result_text()
        log(f"------------------------------------------ {judge_prompt_name}\n\tOriginal: {original}\n\tAlteration: {alteration}", result_text)

    def get_judge_prompts(self):
        judge_prompts = {}
        for judge_prompt_name in self.config["judge_prompt_names"]:
            judge_prompts[judge_prompt_name] = self.config[judge_prompt_name]
        return judge_prompts
