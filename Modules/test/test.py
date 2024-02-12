import random
import Modules


class RNG(Modules.ModuleBase):
    blueprint = [
        "test_RNG",
        [("int", 0), ("int", 100)],
        [],
        [("int", "Random number")]
    ]

    def run(self, settings, stamp, result_clb) -> []:
        res = random.randint(settings[0], settings[1])
        result_clb([res], True, stamp)


class Add(Modules.ModuleBase):
    blueprint = [
        "test_Add",
        [],
        [("int", "A"), ("int", "B")],
        [("int", "Sum")]
    ]

    def run(self, data, settings, stamp, result_clb):
        res = data[0] + data[1]
        result_clb([res], True, stamp)


class Print(Modules.ModuleBase):
    blueprint = [
        "test_Print",
        [],
        [("any", "Input")],
        []
    ]

    def run(self, data, settings, stamp, result_clb):
        print(data[0])
        result_clb([], True, stamp)
