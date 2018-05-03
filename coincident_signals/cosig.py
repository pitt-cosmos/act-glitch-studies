from eventloop.base import EventLoop, DataLoader
from eventloop.routines import Logger
from routines import RemoveMCE, TrimEdges, FindCosigs, FindEvents

loop = EventLoop()
loop.add_tod_list("data/s17_pa4_sublist.txt")
loop.add_routine(DataLoader(input_dir="outputs/s17_pa4_sublist/", output_key="cut"))
loop.add_routine(RemoveMCE(input_key="cut", output_key="cut"))
loop.add_routine(TrimEdges(input_key="cut", output_key="cut"))
loop.add_routine(FindCosigs(input_key="cut", output_key="cosig", season='2017', array='AR4'))
loop.add_routine(FindEvents(input_key="cosig", output_key="data"))
loop.add_routine(Logger(input_key="data"))

loop.run(0, 2)
