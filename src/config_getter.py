import json
import os

config_json_file_name = "config.json"
config_dir_path = "config"

def get_config_json():
    with open(config_json_file_name) as json_data:
        return json.load(json_data)

def get_txt_config(path):
    with open(path, 'r') as txt_data:
        return txt_data.read()

def get_config():
    config = get_config_json()
    for filename in os.listdir(config_dir_path):
        key = filename.removesuffix(".txt")
        value = get_txt_config(os.path.join(config_dir_path, filename))
        config[key] = value
    return config

