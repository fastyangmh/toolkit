#import
import pkgutil
import os
import importlib


#def
def get_imported_modules():
    modules = {}

    for _, module_name, _ in pkgutil.walk_packages([os.getcwd()]):
        root_module_name = module_name.split('.', 1)[0]
        if root_module_name not in modules:
            try:
                modules[root_module_name] = importlib.import_module(
                    name=root_module_name)
            except:
                print(f'import {root_module_name} failed')

    return list(modules.values())


if __name__ == '__main__':
    #parameters

    #get imported modules
    modules = get_imported_modules()
    print(modules)