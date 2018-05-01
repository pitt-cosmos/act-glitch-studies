from eventloop.base import EventLoop, SampleHandler
from eventloop.filters import DurationFilter, PixelFilter, SpreadFilter
from routines import TestRoutine

loop = EventLoop()

# add sample handler
loop.add_handler(SampleHandler(depot="coincident_signals_subset/"))
loop.add_routine(TestRoutine())


# specify range of tods of interests 
loop.run(0, 2)

# for slurm
# import sys
# start = int(sys.argv[1])
# end = int(sys.argv[2])
# loop.run(start, end)
# To run it use python slurm_submit program.py
