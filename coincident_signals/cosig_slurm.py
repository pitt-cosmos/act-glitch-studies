from todloop.base import TODLoop, DataLoader
from todloop.routines import Logger, SaveData
from routines import RemoveMCE, TrimEdges, FindCosigs, FindEvents
import sys

loop = TODLoop()
loop.add_tod_list("data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="outputs/s16_pa3_list/cuts/", output_key="cuts"))
loop.add_routine(RemoveMCE(input_key="cuts", output_key="cuts"))
loop.add_routine(TrimEdges(input_key="cuts", output_key="cuts"))
loop.add_routine(FindCosigs(input_key="cuts", output_key="cosig"))
loop.add_routine(FindEvents(input_key="cosig", output_key="data"))
loop.add_routine(Logger(input_key="data"))
loop.add_routine(SaveData(input_key="data", output_dir="outputs/s16_pa3_list/cosig/"))

start = int(sys.argv[1])
end = int(sys.argv[2])

loop.run(start, end)
