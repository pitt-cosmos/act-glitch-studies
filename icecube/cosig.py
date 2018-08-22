from todloop.base import TODLoop
from todloop.routines import Logger, SaveData, DataLoader
from coincident_signals.routines import RemoveMCE, TrimEdges, FindCosigs, FindEvents

loop = TODLoop()
loop.add_tod_list("data/s17_icecube_list.txt")
loop.add_routine(DataLoader(input_dir="outputs/s17_icecube_list/cut/", output_key="cut"))
loop.add_routine(RemoveMCE(input_key="cut", output_key="cut"))
loop.add_routine(TrimEdges(input_key="cut", output_key="cut"))
loop.add_routine(FindCosigs(input_key="cut", output_key="cosig", season='2017'))
loop.add_routine(FindEvents(input_key="cosig", output_key="data"))
loop.add_routine(Logger(input_key="data"))
loop.add_routine(SaveData(input_key="data", output_dir="outputs/s17_icecube_list/cosig/"))

loop.run(0, 155)
