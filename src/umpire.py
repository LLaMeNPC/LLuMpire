import time, datetime, json, threading, os
from api.api import Api
from config_getter import get_config, get_txt_data
from console_utils import print_progress_bar, digit_percentage
from log import log, _log

class Umpire:

    def __init__(self, api : Api, start_time = "") -> None:
        self.config = get_config()
        self.log_config()
        self.set_metrics()
        self.log_metric_prompts()
        
        self.api = api
        self.data = {}
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') if start_time == "" else start_time

    def judge(self, json_file):
        file_name = f"{self.start_time}_{os.path.basename(json_file).removesuffix(".json")}.json"
        self.tmp_file_path = f"output/in-progress-{file_name}"
        self.final_file_path = f"output/{file_name}"

        metrics = self.config["metrics"]
        threads = []
        with open(json_file) as json_data:
            data = json.load(json_data)
            generation_dicts = data["output"]
            for i, (title, generation_dict) in enumerate(generation_dicts.items()):
                generation_prompt = generation_dict["prompt"]
                generations = generation_dict["generations"]
                self.data[title] = {
                    metric_name: [None for _ in generations] for metric_name in metrics.keys()
                }
                thread = threading.Thread(self.judge_variation(title, generation_prompt, generations))
                thread.start()
                threads.append(thread)
                time.sleep(60 / self.config["rpm"])
                for j, generation in enumerate(generations):
                    metric_threads = []
                    for k, (metric_name, metric_data) in enumerate(metrics.items()):
                        progress_percentage = digit_percentage((i, len(generation_dicts)), (j, len(generations)), (k, len(metrics)))
                        print_progress_bar(progress_percentage)
                        thread = threading.Thread(self.judge_alteration(title, generation_prompt, generation, j, metric_name, metric_data["prompt"]))
                        thread.start()
                        threads.append(thread)
                        metric_threads.append(thread)
                        time.sleep(60 / self.config["rpm"])
                    threading.Thread(self.log_metric_threads(title, generation_prompt, generation, j, metric_threads)).start()
        for t in threads: t.join()
        os.rename(self.tmp_file_path, self.final_file_path)

    def judge_alteration(self, title, generation_prompt, generation, generation_index, metric_name, judge_prompt):
        #judge_prompt = judge_prompt.format(original=title, alteration=generation)
        judge_prompt = judge_prompt.format(llm_prompt=generation_prompt, generated_output=generation)
        api_call_result = self.api.request(judge_prompt)
        self.data[title][metric_name][generation_index] = {
            "generation": generation,
            "score": api_call_result.get_judgement_value(),
            "reasoning": api_call_result.get_text(),
        }
        self.update_output()
        #log(f"------------------------------------------ {metric_name}\n\tOriginal: {title}\n\tAlteration: {generation}", result_text)

    def judge_variation(self, title, generation_prompt, generations):
        judge_prompt = self.config["variation_prompt"].format(dialogue=generations)
        api_call_result = self.api.request(judge_prompt)
        log(f"------------------------------------------ Title: {title}\n\tGeneration prompt: {generation_prompt}\n\tGenerations: {generations}")
        log(api_call_result.get_text())
        self.data[title]["variation"] = [{
            "score": api_call_result.get_judgement_value(),
            "reasoning": api_call_result.get_text(),
        }]

    def set_metrics(self):
        metrics = self.config["metrics"]
        for metric_name, metric_data in metrics.items():
            prompt_path = metric_data["prompt_path"]
            prompt = get_txt_data(prompt_path)
            metrics[metric_name]["prompt"] = prompt

    def update_output(self):
        with open(self.tmp_file_path, "w") as f:
            f.write(json.dumps(self.data))
            
    def log_config(self):
        log("Config:", self.config)

    def log_metric_prompts(self):
        str = ""
        for metric_name, metric_data in self.config["metrics"].items():
            str += f"--- {metric_name} ---\n\n{metric_data["prompt"]}\n"
        log("Metric prompts:", str)

    def log_metric_threads(self, title, generation_prompt, generation, generation_index, metric_threads):
        for t in metric_threads: t.join()
        log(f"------------------------------------------ Title: {title} \n\tGeneration prompt: {generation_prompt}\n\tGeneration: {generation}\n\tGeneration index: {generation_index}")
        for metric_name, v in self.data[title].items():
            if metric_name == "variation":
                continue
            _log(f"{metric_name} score: {v[generation_index]["score"]}\n")
        _log("\n")
        for metric_name, v in self.data[title].items():
            if metric_name == "variation":
                continue
            _log(f"{metric_name} reasoning:\n\t{v[generation_index]["reasoning"]}\n")
