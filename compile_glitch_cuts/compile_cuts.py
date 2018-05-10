from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from todloop.routines import Logger
from routines import CompileCuts

loop = TODLoop()
loop.add_tod_list("data/s16_pa3_list.txt")

glitchp = {
    'nSig': 10, 
    'tGlitch' : 0.007, 
    'minSeparation': 30, 
    'maxGlitch': 50000, 
    'highPassFc': 6.0, 
    'buffer': 0
}

loop.add_routine(TODLoader(output_key="tod_data", abspath=True))
loop.add_routine(TODInfoLoader(output_key="tod_info"))
loop.add_routine(CompileCuts(input_key="tod_data", glitchp=glitchp, output_dir="outputs/s17_pa4_sublist/"))

loop.run(0, 10)
