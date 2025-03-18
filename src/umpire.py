import time, datetime, json, threading, os
from api.api import Api
from config_getter import get_config
from console_utils import print_progress_bar
from log import log

class Umpire:

    def __init__(self, api : Api, start_time = "") -> None:
        self.config = get_config()
        self.api = api
        self.data = {}
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') if start_time == "" else start_time

    def judge(self, json_file):
        judge_prompts = self.get_judge_prompts()
        threads = []
        print(judge_prompts)
        with open(json_file) as json_data:
            data = json.load(json_data)
            alterations = data["output"]
            for i, tup in enumerate(alterations.items()):
                (k, v) = tup
                self.data[k] = {
                    f"{judge_name}_scores": [] for judge_name in judge_prompts.keys()
                }
                for j, alteration in enumerate(v):
                    for judge_prompt_name, judge_prompt in judge_prompts.items():
                        print_progress_bar((j+i*len(v))/(len(alterations) * len(v)-1))
                        threads.append(threading.Thread(self.judge_alteration(k, alteration, judge_prompt_name, judge_prompt)).start())
                        time.sleep(60 / self.config["rpm"])
        while (False in [t.done() for t in threads]): pass
        os.rename(f"output/in-progress-{self.start_time}.json", f"output/{self.start_time}.json")

    def judge_alteration(self, original, alteration, judge_prompt_name, judge_prompt):
        prompt = judge_prompt.format(original=original, alteration=alteration)
        api_call_result = self.api.request(prompt)
        result_text = api_call_result.get_result_text()
        self.data[original][f"{judge_prompt_name}_scores"].append({
            "alteration": alteration,
            "score": api_call_result.get_judgement_value()
        })
        self.update_output()
        log(f"------------------------------------------ {judge_prompt_name}\n\tOriginal: {original}\n\tAlteration: {alteration}", result_text)

    def get_judge_prompts(self):
        judge_prompts = {}
        for judge_prompt_name in self.config["judge_prompt_names"]:
            judge_prompts[judge_prompt_name] = self.config[judge_prompt_name]
        return judge_prompts

    def update_output(self):
        with open(f"output/in-progress-{self.start_time}.json", "w") as f:
            f.write(json.dumps(self.data))
            
