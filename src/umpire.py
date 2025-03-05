import json
from api.api import Api

class Umpire:

    def __init__(self, api : Api) -> None:
        self.api = api

    def judge(self, json_file):
        with open(json_file) as json_data:
            data = json.load(json_data)
            for k, v in data.items():
                for alteration in v:
                    print(f"Call LLM here!! \n{k} \naltered to \n{alteration}")
