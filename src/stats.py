import os, json
from console_utils import cls, choice, get_element_from_choice, queue_exit
from log import log


def user_initialize():
    global chosen_file
    cls()

    print("Which output file would you like to view stats on?")
    output_files = os.listdir("output")
    output_files.remove(".gitkeep")
    output_files.sort()
    chosen_file = f"output/{get_element_from_choice(choice(output_files), output_files)}"
    
    options = [
        "averages",
        "input_averages"
    ]

    while True:
        cls()
        print("What stats do you want to see?")
        accumulations = None
        averages = None

        user_choice = get_element_from_choice(choice(options), options)
        if user_choice == "averages":
            cls()
            accumulations = get_accumulation(chosen_file) if accumulations == None else accumulations
            averages = get_averages(accumulations) if averages == None else averages
            print("-------- metric averages --------")
            for metric, average in averages["metric_averages"].items():
                print(f"{metric}: {average}")
            print(f"\ntotal average: {averages["total_average"]}")
            queue_exit()
        elif user_choice == "input_averages":
            cls()
            accumulations = get_accumulation(chosen_file) if accumulations == None else accumulations
            averages = get_averages(accumulations) if averages == None else averages
            print("-------- input averages --------")
            for _input, metrics in averages["input_averages"].items():
                print(f"Metric averages for \"{_input}\":")
                for metric, average in metrics.items():
                    print(f"\t\t{metric}: {average}")
                print()
            queue_exit()


def _add_value_to_acc(value, acc_d):
    acc_d["acc"] += value
    acc_d["n"] += 1

def get_accumulation(data_file):
    acc = {
        "total": {"acc": 0, "n": 0},
        "metric": {},
        "input": {}
    }
    with open(data_file, "r") as f:
        for original, metrics in json.load(f).items():
            acc["input"][original] = {}
            for metric, judgements in metrics.items():                
                metric_key = metric.removesuffix("_prompt_scores")
                if not metric_key in acc["metric"].items():
                    acc["metric"][metric_key] = {"acc": 0, "n": 0}
                if not metric_key in acc["input"][original]:
                    acc["input"][original][metric_key] = {"acc": 0, "n": 0}
                for judgement in judgements:
                    _add_value_to_acc(judgement["score"], acc["metric"][metric_key])
                    _add_value_to_acc(judgement["score"], acc["input"][original][metric_key])
    return acc
    
def _get_average(acc):
    if acc["n"] == 0:
        return "Not implemented"
    return acc["acc"] / acc["n"]

def get_averages(accs):
    averages = {
        "total_average": _get_average(accs["total"]),
        "metric_averages": {},
        "input_averages": {}
    }
    for metric, acc in accs["metric"].items():
        averages["metric_averages"][metric] = _get_average(acc)
    for input, metrics in accs["input"].items():
        averages["input_averages"][input] = {}
        for metric, acc in metrics.items():
            averages["input_averages"][input][metric] = _get_average(acc)

    return averages
