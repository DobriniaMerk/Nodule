import os
import traceback
from importlib import util


# Generously hacked from https://gist.github.com/dorneanu/cce1cd6711969d581873a88e0257e312
class ModuleBase:
    """Basic module class. All modules will inherit from this one
    """
    modules = []

    # For every class that inherits from the current,
    # the class name will be added to modules list
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.modules.append(cls)


# Small utility to automatically load modules
def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Get current path
path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for module in os.listdir(dirpath):
    # Load only "real modules"
    if not module.startswith('.') and \
       not module.startswith('_') and \
       module + '.py' in os.listdir(os.path.join(dirpath, module)):
        try:
            load_module(os.path.join(os.path.join(dirpath, module), module + '.py'))
        except Exception:
            traceback.print_exc()
