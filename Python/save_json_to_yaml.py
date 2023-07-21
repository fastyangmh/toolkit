#import
import json
import yaml


#def
def save_json_to_yaml(filepath, data):
    with open(filepath, 'w') as f:
        yaml.dump(data=data, stream=f)


if __name__ == '__main__':
    #parameters
    filepath_json = 'config.json'
    filepath_yaml = 'config.yml'

    #load json
    config_json = json.load(open(filepath_json))

    #save_json_to_yaml
    save_json_to_yaml(filepath=filepath_yaml, data=config_json)
