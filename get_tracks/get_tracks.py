from eventloop.base import EventLoop, SampleHandler
#from routines import GetTrack
from routines import GetTrackWithSpread

loop = EventLoop()
loop.add_routine(GetTrackWithSpread(output_dir="outputs/get_track/"))
loop.add_handler(SampleHandler(depot="outputs/coincident_signals_subset/"))

loop.run(0, 2)
