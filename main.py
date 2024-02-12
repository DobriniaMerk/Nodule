import dearpygui.dearpygui as dpg
from utility import NodeBlueprint, ModuleManager
from Modules import ModuleBase


DEBUG = True


managers = {}
generator = None
stamp = 0  # not needed?


blueprints = []
links = {}

output_uuid_convert = {}
input_uuid_convert = {}
param_uuid_convert = {}


def create_node_callback(sender, app_data, user_data):
    # DPG stuff
    node = NodeBlueprint(user_data[0], user_data[1], user_data[2], user_data[3])
    parent = "node_editor"
    node_uuid = dpg.generate_uuid()

    with dpg.node(label=node.name, parent=parent, tag=node_uuid):
        i = 0
        for inp in node.inputs:
            input_uuid = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data=inp[0], tag=input_uuid):
                dpg.add_text(inp[1])
                input_uuid_convert[input_uuid] = (node_uuid, i)
                i += 1

        i = 0
        for outp in node.outputs:
            output_uuid = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data=outp[0], tag=output_uuid):
                dpg.add_text(outp[1])
                output_uuid_convert[output_uuid] = (node_uuid, i)
                i += 1

        i = 0
        for param in node.parameters:
            param_uuid = dpg.generate_uuid()
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                match param[0]:
                    case 'int':
                        dpg.add_input_int(default_value=param[1], tag=param_uuid)
                    case 'float':
                        dpg.add_input_float(default_value=param[1], tag=param_uuid)
                    case 'str':
                        dpg.add_input_text(hint=param[1], tag=param_uuid)
            param_uuid_convert[param_uuid] = (node_uuid, i)
            i += 1

    # Manager stuff

    module = None

    for mdl in ModuleBase.modules:
        if mdl.blueprint[0] == node.name:
            module = mdl

    if module is None:
        raise Exception

    managers[node_uuid] = ModuleManager(module)

    global generator
    if len(module.blueprint[2]) == 0:
        generator = managers[node_uuid]


def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2) ids of pins, not nodes

    # in user_data type is stored
    if dpg.get_item_user_data(app_data[0]) == dpg.get_item_user_data(app_data[1]) or dpg.get_item_user_data(app_data[0]) == "any" or dpg.get_item_user_data(app_data[1]) == "any":
        uuid = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        links[uuid] = (app_data[0], app_data[1])

        outgoing = output_uuid_convert[app_data[0]]  # (node_id, output_index)
        ingoing = input_uuid_convert[app_data[1]]  # (node_id, input_index)

        managers[outgoing[0]].linked(managers[ingoing[0]], outgoing[1], ingoing[1])  # tell managers to connect


def delink_callback(sender, app_data):
    # app_data -> link_id
    outgoing = output_uuid_convert[links[app_data][0]]  # (node_id, output_index)
    ingoing = input_uuid_convert[links[app_data][1]]  # (node_id, input_index)

    managers[outgoing[0]].delinked(managers[ingoing[0]], outgoing[1], ingoing[1])

    dpg.delete_item(app_data)
    links.pop(app_data)


def run_set_callback(sender, app_data):
    dpg.configure_item("run_param", show=True)
    for key, value in param_uuid_convert.items():
        uuid, ind = value
        managers[uuid].settings[ind] = dpg.get_value(key)


def run_callback(sender, app_data):
    dpg.configure_item("run_param", show=False)
    global stamp
    if generator is None:
        return
    for _ in range(dpg.get_value("iters")):
        generator.generate(stamp)
        stamp += 1


def create_interface():
    dpg.create_context()
    dpg.create_viewport(title="Merk's Scanner", width=600, height=300)

    with dpg.window(label="Node editor", tag="main"):
        with dpg.node_editor(callback=link_callback, delink_callback=delink_callback, tag="node_editor"):
            pass
        with dpg.menu_bar():
            with dpg.menu(label="Node"):
                for node in blueprints:
                    dpg.add_menu_item(label=node[0], callback=create_node_callback, user_data=node)
            dpg.add_spacer()
            dpg.add_button(label="RUN!", callback=run_set_callback)

    with dpg.window(label="Run settings", modal=True, show=False, tag="run_param", no_title_bar=True):
        with dpg.group(horizontal=True):
            dpg.add_text("Number of iterations to run")
            dpg.add_input_int(label="Iterations", default_value=5, min_value=1, tag="iters")
        dpg.add_button(label="Ok", callback=run_callback)

    dpg.setup_dearpygui()

    if DEBUG:
        dpg.show_item_registry()
        dpg.show_debug()

    dpg.show_viewport()

    dpg.set_primary_window("main", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


def main():
    global blueprints
    blueprints = [module.blueprint for module in ModuleBase.modules]
    create_interface()


if __name__ == '__main__':
    main()
