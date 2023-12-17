import os, sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Modules


class Example(Modules.ModuleBase):
	blueprint = [
		"example",     # display name
		[('int', 0)],  # parameters (type, default value)
		[],            # inputs (type, name)
		[]   		   # outputs (type, name)
	]

	def run(self, data, settings, stamp, result_clb) -> []:
		result_clb(stamp)
		pass
