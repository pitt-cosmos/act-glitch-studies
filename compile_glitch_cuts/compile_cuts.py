from eventloop.tod import TODLoop
from routines import CompileCuts

loop = TODLoop()
loop.add_tod_list("data/tod_test.txt")

glitchp = {
    'nSig': 10, 
    'tGlitch' : 0.007, 
    'minSeparation': 30, 
    'maxGlitch': 50000, 
    'highPassFc': 6.0, 
    'buffer': 0
}

loop.add_routine(CompileCuts(glitchp=glitchp, output_dir="output/test_compile_glitch/"))

loop.run(0,5)
