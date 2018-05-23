from todloop.event import LoadRaDec, NPixelFilter, CoeffFilter, DurationFilter
from todloop.base import TODLoop
from calibration.routines import FixOpticalSign
from todloop.routines import DataLoader, Logger
from todloop.tod import TODLoader
from plot_events.routines import PlotEvents
from routines import RaDecStudy


loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_skip([340, 956, 1041, 1066, 1099, 1609, 3791, 4389,4451, 5259,6978])  # problematic ones
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/", output_key="events"))
loop.add_routine(NPixelFilter(min_pixels=0, max_pixels=3, input_key="events", output_key="events"))
loop.add_routine(DurationFilter(min_duration=10, max_duration=60, input_key="events", output_key="events"))
loop.add_routine(CoeffFilter(min_coeff=0.8, input_key="events", output_key="events"))
# loop.add_routine(TODLoader(output_key="tod-data"))
# loop.add_routine(FixOpticalSign(input_key="tod-data", output_key="tod-data"))
# loop.add_routine(Logger(input_key="events"))
# loop.add_routine(PlotEvents(event_key="events", tod_key="tod-data"))
loop.add_routine(LoadRaDec(input_key="events", output_key="events"))
loop.add_routine(RaDecStudy(input_key="events"))
loop.run(0, 10000)
