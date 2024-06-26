import Modules
import requests


class GetHTML(Modules.ModuleBase):
    blueprint = [
        "Get HTML",
        [("str", "", "Proxy")],
        [("str", "", "Address")],
        [("str", "HTML")]
    ]

    def run(self, data, settings, stamp, result_clb):
        proxies = {}

        if settings[0] != "":
            proxies = {"http": settings[0], "https": settings[0]}

        res = requests.get(data[0], proxies=proxies)
        result_clb([res.text], True, stamp)
