from eventloop.tod import TODLoader
from eventloop.base import EventLoop
from routines import CompileCuts

loop = EventLoop()
loop.add_tod_list("data/s17_pa4_sublist.txt")

glitchp = {
    'nSig': 10, 
    'tGlitch' : 0.007, 
    'minSeparation': 30, 
    'maxGlitch': 50000, 
    'highPassFc': 6.0, 
    'buffer': 0
}

loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(CompileCuts(input_key="tod_data", glitchp=glitchp, output_dir="outputs/s17_pa4_sublist/"))

loop.run(0, 2)
