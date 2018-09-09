from todloop.event import LoadRaDec, NPixelFilter, CoeffFilter, DurationFilter
from todloop.base import TODLoop
from calibration.routines import FixOpticalSign
from todloop.routines import DataLoader, Logger
from todloop.tod import TODLoader
from plot_events.routines import PlotEvents
from cr_hist.routines import RaDecStudy


loop = TODLoop()
loop.add_tod_list("../data/s17_icecube_list.txt")
loop.add_skip([128,129,130,131])  # problematic ones
loop.add_routine(DataLoader(input_dir="../outputs/s17_icecube_list/events/", output_key="events"))
#loop.add_routine(NPixelFilter(min_pixels=0, max_pixels=3, input_key="events", output_key="events"))
#loop.add_routine(DurationFilter(min_duration=10, max_duration=60, input_key="events", output_key="events"))
loop.add_routine(CoeffFilter(min_coeff=0.0, input_key="events", output_key="events"))
# loop.add_routine(TODLoader(output_key="tod-data"))
# loop.add_routine(FixOpticalSign(input_key="tod-data", output_key="tod-data"))
# loop.add_routine(Logger(input_key="events"))
# loop.add_routine(PlotEvents(event_key="events", tod_key="tod-data"))
loop.add_routine(LoadRaDec(input_key="events", output_key="events"))
loop.add_routine(RaDecStudy(input_key="events", ra_range=[1.2, 1.4], dec_range=[0.08, 0.11]))
loop.run(0, 127)
