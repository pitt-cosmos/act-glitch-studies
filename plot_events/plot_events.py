from todloop.base import TODLoop
from todloop.tod import TODLoader
from todloop.routines import Logger
from todloop.base import DataLoader
from routines import PlotEvents, NPixelFilter, LoadRaDec
from calibration.routines import FixOpticalSign, CalibrateTOD

loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/", output_key="events"))
loop.add_routine(NPixelFilter(min_pixels=50, max_pixels=100, input_key="events", output_key="events"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data", output_key="tod_data"))
#loop.add_routine(PlotEvents(tod_key="tod_data", event_key="events"))
loop.add_routine(LoadRaDec(tod_key="tod_data", event_key="events", output_key="events"))
loop.add_routine(Logger(input_key="events"))

loop.run(0,5000)
