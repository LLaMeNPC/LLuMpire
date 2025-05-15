# LLuMpire: Large Language Model umpire

# Table of contents

* [Setup (linux)](#setup-linux)
  * [Set up a virtual enviorenment for python packages (optional)](#set-up-a-virtual-enviorenment-for-python-packages-optional)
  * [Download requirements](#download-requirements)
  * [Setup automatic venv switching (optional)](#setup-automatic-venv-switching-optional)
* [Set up API](#set-up-api)
* [Run LLM-as-a-judge](#run-llm-as-a-judge)
* [Run stats](#run-stats)
* [Config](#config)

# Setup (linux)

## Set up a virtual enviorenment for python packages (optional)

Run the following in root of project. (You might need to install something before it works...)
```
$ python -m venv .venv
```

Activate it by running:
```
$ source .venv/bin/activate
```

Deactivate it by running:
```
$ deactivate
```

Check out [python docs venv](https://docs.python.org/3/library/venv.html) for more info.

## Download requirements

Go to the root directory of the project, enable virtual enviorenment (optinal) and run the following.
```
$ pip install -r requirements.txt
```

## Setup automatic venv switching (optional)

Make a file somewhere and call it something like `cdmod.sh`:
```bash
function cd() {
  builtin cd "$@"

  if [[ -z "$VIRTUAL_ENV" ]] ; then
    ## If env folder is found then activate the vitualenv
      if [[ -d ./.venv ]] ; then
        source ./.venv/bin/activate
      fi
  else
    ## check the current folder belong to earlier VIRTUAL_ENV folder
    # if yes then do nothing
    # else deactivate
      parentdir="$(dirname "$VIRTUAL_ENV")"
      if [[ "$PWD"/ != "$parentdir"/* ]] ; then
        deactivate
      fi
  fi
}
```

Run
```
$ chmod +x cdmod.sh
```

Add this line to your `.bashrc` or `.zshrc`:
```bash
...
source <path>/cdmod.sh
```

# Set up API

LLuMpire is current only implemented with API calls to `gemini-2.0-flash`. To implement another model, take inspiration from how the `Gemini` class found in `src/api/gemini.py` implements the `Api` class in `src/api/api.py`.

Using the Gemini API requires a key, which has to be added to the environment variable `GEMINI_KEY`. We recommend trying the free tier first.

# Run LLM-as-a-judge

Run LLuMpire and provide an output file from SLalter as an argument e.g.:
```
$ python src/main.py '../SLalter/output/file-name.json'
```

It might take a while for it to start. Once the judgement process has started a progress bar will be shown.

The evaluations will be saved to the `output/` directory.

# Run stats

Run LLuMpire without any arguments using:
```
$ python src/main.py
```

You will then be asked if you want to view stats. You will then be asked to select a file from `shared_output/` directory. Evaluations are by default saved to the `output/` directory, make sure to move the ones you want to view stats on to the `shared_output/` directory.

You will then be given the following options
```
What stats do you want to see?
  0) metric_averages
  1) input_averages
  2) metric_graphs
  3) input_averages_graphs
  4) input_values_graphs
Please select an option:
```

# Config

Settings can be changed in `config.json`.
* `rpm` stands for requests per minute and should be set an amount which fits the rate limit of the API used.
* Metrics can be added, changed or removed and their respective judge prompts can be altered by editing the file at their path.
* `max_request_retries` controls how many times it will retry a request when the API fails and `request_retry_delay` is how long it will wait before retrying each API request.
```json
{
  "rpm": 15,
  "metrics": {
    "attitude": {"min_value": 1, "max_value": 3, "prompt_path": "prompts/attitude_prompt.txt"},
    "intent": {"min_value": 1, "max_value": 4, "prompt_path": "prompts/intent_prompt.txt"},
    "validity": {"min_value": 0, "max_value": 1, "prompt_path": "prompts/validity_simple_prompt.txt"}
  },
  "ignore": {
  },
  "max_request_retries": 100,
  "request_retry_delay": 2
}
```
