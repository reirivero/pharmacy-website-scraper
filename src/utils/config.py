import yaml
import os

def load_config(config_path=os.path.abspath('./src/utils/config.yaml')):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
