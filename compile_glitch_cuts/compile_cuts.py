from eventloop.tod import TODLoop
from routines import CompileCuts

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

loop.add_routine(CompileCuts(glitchp=glitchp, output_dir="outputs/s17_pa4_sublist"))

loop.run(0,5)
