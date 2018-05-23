from todloop.base import TODLoop
from todloop.tod import TODLoader
from todloop.routines import Logger, DataLoader
from routines import PlotEvents
from todloop.event import NPixelFilter, DurationFilter, CoeffFilter
from calibration.routines import FixOpticalSign, CalibrateTOD

loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_skip([1029, 1723])  # problematic ones
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/", output_key="events"))
loop.add_routine(NPixelFilter(min_pixels=1, max_pixels=10, input_key="events", output_key="events"))
loop.add_routine(DurationFilter(min_duration=20, max_duration=40, input_key="events", output_key="events"))
loop.add_routine(CoeffFilter(min_coeff=0.8, max_coeff=1, input_key="events", output_key="events"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data", output_key="tod_data"))
loop.add_routine(PlotEvents(tod_key="tod_data", event_key="events"))

loop.run(0,5000)
