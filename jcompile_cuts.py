from eventloop.base import DataLoader
from eventloop.tod import TODLoader
from eventloop.base import EventLoop
from jroutines import CompileCuts
from jpixels import PixelReader


loop = EventLoop()
loop.add_tod_list("data/s16_pa3_list.txt")

glitchp = {
    'nSig': 10, 
    'tGlitch' : 0.007, 
    'minSeparation': 30, 
    'maxGlitch': 50000, 
    'highPassFc': 6.0, 
    'buffer': 0
}

#will load the data stored in the folder specified one by one 
#and store the loaded data in the shared date store under a key called data
loop.add_routine(DataLoader(input_dir="outputs/coincident_signals_subset/",output_key="cuts"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(CompileCuts(input_key="tod_data", glitchp=glitchp, output_dir="outputs/s17_pa4_sublist/"))

loop.run(10000, 10001)
