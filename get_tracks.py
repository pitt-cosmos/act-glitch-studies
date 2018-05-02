from eventloop.base import EventLoop, SampleHandler
from eventloop.filters import DurationFilter, PixelFilter, SpreadFilter
from routines import TestRoutine

#create an event loop		
loop = EventLoop()

#Load coincident signals in folder outputs/coincident_signals/
# add sample handler
loop.add_handler(SampleHandler(depot="outputs/coincident_signals_subset/"))

#Add PixelFilter Routine
loop.add_routine(TestRoutine())


# specify range of tods of interests
#loop.run(0,2) will run the pipeline for the first 10 datasets  
loop.run(0, 2)

# for slurm
# import sys
# start = int(sys.argv[1])
# end = int(sys.argv[2])
# loop.run(start, end)
# To run it use python slurm_submit program.py
