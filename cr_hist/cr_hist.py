from todloop.base import TODLoop
from todloop.tod import TODInfoLoader
from todloop.routines import DataLoader
from routines import NPixelStudy, CRHourStudy, CRPWVStudy
from todloop.event import NPixelFilter, CoeffFilter

loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/", output_key="events"))

# loop.add_routine(NPixelFilter(min_pixels=30, max_pixels=100, input_key="events", output_key="events"))
loop.add_routine(CoeffFilter(min_coeff=0.9, input_key="events", output_key="events"))
loop.add_routine(NPixelStudy())
loop.add_routine(TODInfoLoader(output_key="tod_info"))
loop.add_routine(CRHourStudy())
loop.add_routine(CRPWVStudy())
loop.run(0,3000)
