from todloop.base import DataLoader
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from routines import PlotGlitches


loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")

#will load the data stored in the folder specified one by one
#and store the loaded data in the shared date store under a key called data
loop.add_routine(DataLoader(input_dir="../outputs/coincident_signals_subset/", output_key="cuts"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(TODInfoLoader())
loop.add_routine(PlotGlitches(tod_key="tod_data", cosig_key="cuts"))
loop.run(1942, 1943)
