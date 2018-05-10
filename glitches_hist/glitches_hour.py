from todloop.base import EventLoop
from todloop.tod import TODInfoLoader
from todloop.base import DataLoader
from todloop.filters import PixelFilter, DurationFilter
from routines import GlitchHourStudy, GlitchPWVStudy, GlitchAzStudy


loop = EventLoop()
loop.add_tod_list("data/s16_pa3_list.txt")
loop.add_routine(TODInfoLoader(output_key="tod_info"))
loop.add_routine(DataLoader(input_dir="outputs/coincident_signals_subset/", output_key="cosig"))
#loop.add_routine(PixelFilter(input_key="cosig", output_key="cosig", max_pixels=7))
#loop.add_routine(DurationFilter(input_key="cosig", output_key="cosig", max_duration=10))
#loop.add_routine(GlitchHourStudy())
#loop.add_routine(GlitchPWVStudy())
loop.add_routine(GlitchAzStudy())
loop.run(0,14000)
