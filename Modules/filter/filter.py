import re
import Modules


class Extract:
    blueprint = [
        "Extract by Regex",
        [("str", "")],
        [("str", "Input")],
        [("str", "Extracted")]
    ]

    def run(self, data, settings, stamp, result_clb):
        res = re.findall(settings[0], data[0])
        result_clb([res], True, stamp)


class Filter:
    blueprint = [

    ]