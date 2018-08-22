from todloop.base import TODLoop
from todloop.routines import Logger, SaveData, DataLoader
from routines import RemoveMCE, TrimEdges, FindCosigs, FindEvents

tod_index = 152
loop = TODLoop()
loop.add_tod_list("../data/covered_tods.txt")
loop.add_routine(DataLoader(input_dir="../compile_cuts/outputs/covered_tods/", output_key="cut"))
loop.add_routine(RemoveMCE(input_key="cut", output_key="cut"))
loop.add_routine(TrimEdges(input_key="cut", output_key="cut"))
loop.add_routine(FindCosigs(input_key="cut", output_key="cosig", season='2017', array='AR4'))
loop.add_routine(FindEvents(input_key="cosig", output_key="data"))
loop.add_routine(Logger(input_key="data"))
loop.add_routine(SaveData(input_key="data", output_dir="../outputs/covered_tods_cosig/"))

loop.run(tod_index, tod_index + 1)
