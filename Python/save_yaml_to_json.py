#import
import yaml
import json


#def
def save_yaml_to_json(filepath, obj):
    with open(filepath, 'w') as f:
        json.dump(obj=obj, fp=f)


if __name__ == '__main__':
    #parameters
    filepath_yaml = 'config.yml'
    filepath_json = 'config.json'

    #load yaml
    config_yaml = yaml.safe_load(open(filepath_yaml))

    #save_yaml_to_json
    save_yaml_to_json(filepath=filepath_json, obj=config_yaml)
