from eventloop.base import EventLoop, SampleHandler
from routines import GetTrack

loop = EventLoop()
loop.add_routine(GetTrack(output_dir="outputs/get_track/"))
loop.add_handler(SampleHandler(depot="outputs/coincident_signals_subset/"))

loop.run(0, 2)
