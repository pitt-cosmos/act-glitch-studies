from eventloop.base import EventLoop, SampleHandler
from eventloop.filters import DurationFilter, PixelFilter
from routines import GetTrackWithSpread

loop = EventLoop()

# add sample handler
loop.add_handler(SampleHandler(depot="outputs/coincident_signals_subset/"))

# add filters
loop.add_routine(DurationFilter(max_duration = 10))
loop.add_routine(PixelFilter(max_pixels = 5))

# add main routine
loop.add_routine(GetTrackWithSpread(output_dir="outputs/get_track_filtered/"))

# specify range of tods of interests 
loop.run(0, 2)

# for slurm
# import sys
# start = int(sys.argv[1])
# end = int(sys.argv[2])
# loop.run(start, end)
# To run it use python slurm_submit program.py
