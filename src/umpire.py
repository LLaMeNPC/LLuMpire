import time, datetime, json, threading, os
from api.api import Api
from config_getter import get_config, get_txt_data
from console_utils import print_progress_bar, digit_percentage
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
            generation_dicts = data["output"]
            for i, (title, generation_dict) in enumerate(generation_dicts.items()):
                self.data[title] = {
                    f"{metric_name}_scores": [] for metric_name in metrics.keys()
                }
                generation_prompt = generation_dict["prompt"]
                generations = generation_dict["generations"]
                for j, generation in enumerate(generations):
                    for k, (metric_name, metric_data) in enumerate(metrics.items()):
                        progress_percentage = digit_percentage((i, len(generation_dicts)), (j, len(generations)), (k, len(metrics)))
                        print_progress_bar(progress_percentage)
                        thread = threading.Thread(self.judge_alteration(title, generation_prompt, generation, metric_name, metric_data["prompt"]))
                        thread.start()
                        threads.append(thread)
                        time.sleep(60 / self.config["rpm"])
        for t in threads: t.join()
        os.rename(f"output/in-progress-{self.start_time}.json", f"output/{self.start_time}.json")

    def judge_alteration(self, title, generation_prompt, generation, metric_name, judge_prompt):
        judge_prompt = judge_prompt.format(original=title, alteration=generation)
        api_call_result = self.api.request(judge_prompt)
        result_text = api_call_result.get_result_text()
        self.data[title][f"{metric_name}_scores"].append({
            "alteration": generation,
            "score": api_call_result.get_judgement_value()
        })
        self.update_output()
        log(f"------------------------------------------ {metric_name}\n\tOriginal: {title}\n\tAlteration: {generation}", result_text)

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
