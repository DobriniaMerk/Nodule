import os
import importlib
from utility import NodeBlueprint, ModuleManager

from Modules import ModuleBase

import dearpygui_interface

managers = []
generator = None
stamp = 0


def set_setting(manager, setting, value):
    managers[manager].settings[setting] = value


def new_link(sender, outgoing, ingoing):
    managers[outgoing[0]].linked(managers[ingoing[0]], outgoing[1], ingoing[1])
    pass


def deleted_link(sender, outgoing, ingoing):
    managers[outgoing[0]].delinked(managers[ingoing[0]], outgoing[1], ingoing[1])
    pass


def new_node(sender, name) -> int:
    module = None

    for mdl in ModuleBase.modules:
        if mdl.blueprint[0] == name:
            module = mdl

    if module is None:
        raise Exception

    managers.append(ModuleManager(module))

    global generator
    if len(module.blueprint[2]) == 0:
        generator = managers[-1]

    return len(managers) - 1


def run(iterations):
    global stamp
    if generator is None:
        return
    for _ in range(iterations):
        generator.generate(stamp)
        stamp += 1


def main():
    gui = dearpygui_interface.GUI([module.blueprint for module in ModuleBase.modules], new_link, deleted_link, new_node, run, set_setting)
    gui.run()


if __name__ == '__main__':
    main()
