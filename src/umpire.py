import time, datetime, json, threading, os
from api.api import Api
from config_getter import get_config, get_txt_data
from console_utils import print_progress_bar
from log import log

class Umpire:

    def __init__(self, api : Api, start_time = "") -> None:
        self.config = get_config()
        self.log_config()
        self.set_metrics()
        self.log_metric_prompts()
        
        self.api = api
        self.data = {}
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') if start_time == "" else start_time

    def judge(self, json_file):
        metrics = self.config["metrics"]
        threads = []
        with open(json_file) as json_data:
            data = json.load(json_data)
            alterations = data["output"]
            for i, tup in enumerate(alterations.items()):
                (k, v) = tup
                self.data[k] = {
                    f"{metric_name}_scores": [] for metric_name in metrics.keys()
                }
                for j, alteration in enumerate(v):
                    for metric_name, metric_data in metrics.items():
                        print_progress_bar((j+i*len(v))/(len(alterations) * len(v)-1))
                        thread = threading.Thread(self.judge_alteration(k, alteration, metric_name, metric_data["prompt"]))
                        thread.start()
                        threads.append(thread)
                        time.sleep(60 / self.config["rpm"])
        for t in threads: t.join()
        os.rename(f"output/in-progress-{self.start_time}.json", f"output/{self.start_time}.json")

    def judge_alteration(self, original, alteration, metric_name, prompt):
        prompt = prompt.format(original=original, alteration=alteration)
        api_call_result = self.api.request(prompt)
        result_text = api_call_result.get_result_text()
        self.data[original][f"{metric_name}_scores"].append({
            "alteration": alteration,
            "score": api_call_result.get_judgement_value()
        })
        self.update_output()
        log(f"------------------------------------------ {metric_name}\n\tOriginal: {original}\n\tAlteration: {alteration}", result_text)

    def set_metrics(self):
        metrics = self.config["metrics"]
        for metric_name, metric_data in metrics.items():
            prompt_path = metric_data["prompt_path"]
            prompt = get_txt_data(prompt_path)
            metrics[metric_name]["prompt"] = prompt

    def update_output(self):
        with open(f"output/in-progress-{self.start_time}.json", "w") as f:
            f.write(json.dumps(self.data))
            
    def log_config(self):
        log("Config:", self.config)

    def log_metric_prompts(self):
        str = ""
        for metric_name, metric_data in self.config["metrics"].items():
            str += f"--- {metric_name} ---\n\n{metric_data["prompt"]}\n"
        log("Metric prompts:", str)
