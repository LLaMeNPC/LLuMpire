import json
from api.api import Api
from config_getter import get_config
from log import log

class Umpire:

    def __init__(self, api : Api) -> None:
        self.config = get_config()
        self.api = api

    def judge(self, json_file):
        with open(json_file) as json_data:
            data = json.load(json_data)
            alterations = data["output"]
            for k, v in alterations.items():
                for alteration in v:
                    self.judge_alteration(k, alteration)

    def judge_alteration(self, original, alteration):
        prompt = self.config["judge_prompt"].format(original=original, alteration=alteration)
        api_call_result = self.api.request(prompt)
        result_text = api_call_result.get_result_text()
        print(result_text)
        log(f"Original: {original}, alteration: {alteration}", result_text)
