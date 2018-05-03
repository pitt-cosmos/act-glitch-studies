from eventloop.base import EventLoop
from eventloop.tod import TODInfoLoader
from eventloop.base import DataLoader
from routines import GlitchHourStudy


loop = EventLoop()
loop.add_tod_list("data/s16_pa3_list.txt")
loop.add_routine(TODInfoLoader(output_key="tod_info"))
loop.add_routine(DataLoader(input_dir="outputs/coincident_signals_subset/", output_key="cosig"))
loop.add_routine(GlitchHourStudy())
