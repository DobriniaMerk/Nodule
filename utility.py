class NodeBlueprint:
    def __init__(self, name: str = "", parameters: list[(str, ...)] = None, inputs: list[(str, str)] = None,
                 outputs: list[(str, str)] = None):
        self.parameters = parameters
        self.inputs = inputs
        self.outputs = outputs
        self.name = name


class ModuleManager:
    def __init__(self, module):
        self.module = module()
        self.inputs = [{} for _ in range(len(module.blueprint[2]))]
        self.next = []
        self.log = []
        self.settings = [x[1] for x in module.blueprint[1]]

    def result_callback(self, result, successful, stamp):
        if successful:
            for n in self.next:
                to, out_pin, in_pin = n
                to.give((stamp, result[out_pin]), in_pin)
        else:
            print(f"Error occurred in {self.module}: {result[0]}")
            self.log.append(result)

    def generate(self, stamp):
        if len(self.inputs) > 0:
            raise Exception
        else:
            self.module.run(self.settings, stamp, self.result_callback)

    def give(self, data, pin):
        self.inputs[pin][data[0]] = data[1]
        self.check_inputs(data[0])

    def check_inputs(self, stamp):
        for inp in self.inputs:
            if stamp not in inp.keys():
                return

        data = []
        for inp in self.inputs:
            data.append(inp.pop(stamp))

        self.module.run(data, self.settings, stamp, self.result_callback)

    def linked(self, to, out_pin, in_pin):
        self.next.append((to, out_pin, in_pin))

    def delinked(self, to, out_pin, in_pin):
        self.next.remove((to, out_pin, in_pin))
