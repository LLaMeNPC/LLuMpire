import os, json, re
from console_utils import cls, choice, get_element_from_choice, queue_exit, print_progress_bar
import matplotlib.pyplot as plt

def user_initialize():
    global chosen_file
    cls()

    print("Which output file would you like to view stats on?")
    output_files = os.listdir("output")
    output_files.remove(".gitkeep")
    output_files.sort()
    chosen_file = f"output/{get_element_from_choice(choice(output_files), output_files)}"
    
    options = [
        "metric_averages",
        "input_averages",
        "metric_graphs",
        "input_graphs"
    ]

    while True:
        cls()
        print("What stats do you want to see?")
        accumulations = None
        averages = None

        user_choice = get_element_from_choice(choice(options), options)
        if user_choice == "metric_averages":
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
        
        elif user_choice == "metric_graphs":
            cls()

            accumulations = get_accumulation(chosen_file) if accumulations == None else accumulations

            print("Showing Metric graphs.... close one to see the next one")
            for metric, accs in accumulations["metric"].items():
                plt.title(metric.title())
                plot_values(accs)
                plt.show()
            queue_exit()
        elif user_choice == "input_graphs":
            cls()
            filename = chosen_file.split("/")[-1]
            filename = re.sub(r'[\\/*?:"<>|]',"",filename)

            try:
                os.mkdir(f"output/graphs/{filename}")

                accumulations = get_accumulation(chosen_file) if accumulations == None else accumulations
                averages = get_averages(accumulations) if averages == None else averages

                for i, (_input, metrics) in enumerate(averages["input_averages"].items()):
                    #print_progress_bar(i / len(averages["input_averages"]))
                    plt.title(_input.title())
                    print("---------------------")
                    print(metrics.keys())
                    print(metrics.values())
                    plt.bar(metrics.keys(), metrics.values())
                    plt.savefig(f"output/graphs/{filename}/{_input}.svg")

            except FileExistsError:
                print(f"Graphs for file {filename} already exist in \"output/graphs/{filename}\"")
            queue_exit()
                



def get_accumulation(data_file):
    acc = {
        "total": [],
        "metric": {},
        "input": {}
    }
    with open(data_file, "r") as f:
        for original, metrics in json.load(f).items():
            acc["input"][original] = {}
            for metric, judgements in metrics.items():                
                metric_key = metric.removesuffix("_prompt_scores")
                if not metric_key in acc["metric"].items():
                    acc["metric"][metric_key] = []
                if not metric_key in acc["input"][original]:
                    acc["input"][original][metric_key] = []
                for judgement in judgements:
                    acc["metric"][metric_key].append(judgement["score"])
                    acc["input"][original][metric_key].append(judgement["score"])
    return acc
    
def _get_average(li):
    if len(li) == 0:
        return "Not implemented"
    return sum(li) / len(li)

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

def plot_values(vals):
    val_amnts = [0] * 5
    for val in vals:
        val_amnts[val] += 1

    plt.bar(range(5), val_amnts)
