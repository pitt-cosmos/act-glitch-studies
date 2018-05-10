from todloop.tod import TODLoader
from todloop.base import TODLoop
from routines import CompileCuts
import sys

loop = TODLoop()
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

start = int(sys.argv[1])
end = int(sys.argv[2])
loop.run(start, end)


