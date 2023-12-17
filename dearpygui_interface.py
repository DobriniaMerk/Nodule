import dearpygui.dearpygui as dpg
from utility import NodeBlueprint

DEBUG = True


class GUI:

    def __init__(self, blueprints, link_clb, delink_clb, add_clb, run_clb, set_clb):
        self.blueprints = blueprints
        self.links = {}

        self.inside_to_outside_uuid = {}
        self.outside_to_inside_uuid = {}

        self.output_uuid_convert = {}
        self.input_uuid_convert = {}
        self.param_uuid_convert = {}

        self.main_link_callback = link_clb
        self.main_delink_callback = delink_clb
        self.main_add_node_callback = add_clb
        self.main_run_callback = run_clb
        self.main_setting_callback = set_clb

    def create_node_callback(self, sender, app_data, user_data):
        outer_uuid = self.main_add_node_callback(self, user_data[0])
        self.create_node(NodeBlueprint(user_data[0], user_data[1], user_data[2], user_data[3]), outer_uuid)

    def create_node(self, node: NodeBlueprint, outer_uuid):
        parent = "node_editor"

        node_uuid = dpg.generate_uuid()

        self.inside_to_outside_uuid[node_uuid] = outer_uuid
        self.outside_to_inside_uuid[outer_uuid] = node_uuid

        with dpg.node(label=node.name, parent=parent, tag=node_uuid):

            i = 0
            for inp in node.inputs:
                input_uuid = dpg.generate_uuid()
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, user_data=inp[0], tag=input_uuid):
                    dpg.add_text(inp[1])
                    self.input_uuid_convert[input_uuid] = (outer_uuid, i)
                    i += 1

            i = 0
            for outp in node.outputs:
                output_uuid = dpg.generate_uuid()
                with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, user_data=outp[0], tag=output_uuid):
                    dpg.add_text(outp[1])
                    self.output_uuid_convert[output_uuid] = (outer_uuid, i)
                    i += 1

            i = 0
            with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Static):
                for param in node.parameters:
                    param_uuid = dpg.generate_uuid()
                    match param[0]:
                        case 'int':
                            dpg.add_input_int(default_value=param[1], tag=param_uuid)
                        case 'float':
                            dpg.add_input_float(default_value=param[1], tag=param_uuid)
                        case 'str':
                            dpg.add_input_text(hint=param[1], tag=param_uuid)
                    self.param_uuid_convert[param_uuid] = (outer_uuid, i)
                    i += 1

    def link_callback(self, sender, app_data):
        # app_data -> (link_id1, link_id2)

        # in user_data type is stored
        if dpg.get_item_user_data(app_data[0]) != dpg.get_item_user_data(app_data[1]):
            return

        uuid = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        self.links[uuid] = (app_data[0], app_data[1])
        self.main_link_callback(self, self.output_uuid_convert[app_data[0]], self.input_uuid_convert[app_data[1]])

    def delink_callback(self, sender, app_data):
        # app_data -> link_id

        self.main_delink_callback(
            self,
            self.output_uuid_convert[self.links[app_data][0]],
            self.input_uuid_convert[self.links[app_data][1]]
        )

        dpg.delete_item(app_data)
        self.links.pop(app_data)

    def run_set_callback(self, sender, app_data):
        dpg.configure_item("run", show=True)
        for key, value in self.param_uuid_convert.items():
            outer_uuid, ind = value
            self.main_setting_callback(outer_uuid, ind, dpg.get_value(key))

    def run_callback(self, sender, app_data):
        dpg.configure_item("run", show=False)
        self.main_run_callback(dpg.get_value("iters"))

    def run(self):

        dpg.create_context()
        dpg.create_viewport(title="Merk's Scanner", width=600, height=300)

        with dpg.window(label="Node editor", tag="main"):
            with dpg.node_editor(callback=self.link_callback, delink_callback=self.delink_callback, tag="node_editor"):
                pass
            with dpg.menu_bar():
                with dpg.menu(label="Node"):
                    for node in self.blueprints:
                        dpg.add_menu_item(label=node[0], callback=self.create_node_callback, user_data=node)
                dpg.add_spacer()
                dpg.add_button(label="RUN!", callback=self.run_set_callback)

        with dpg.window(label="Run settings", modal=True, show=False, tag="run", no_title_bar=True):
            with dpg.group(horizontal=True):
                dpg.add_text("Number of iterations to run")
                dpg.add_input_int(label="Iterations", default_value=5, min_value=1, tag="iters")
            dpg.add_button(label="Ok", callback=self.run_callback)

        dpg.setup_dearpygui()

        if DEBUG:
            dpg.show_item_registry()
            dpg.show_debug()

        dpg.show_viewport()

        dpg.set_primary_window("main", True)
        dpg.start_dearpygui()
        dpg.destroy_context()
