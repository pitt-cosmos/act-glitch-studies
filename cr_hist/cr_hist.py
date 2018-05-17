from todloop.base import TODLoop
from todloop.tod import TODInfoLoader
from todloop.base import DataLoader
from routines import CRHourStudy, CRPWVStudy


loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(TODInfoLoader(output_key="tod_info"))
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/", output_key="events"))
loop.add_routine(CRPWVStudy())
loop.run(0,10000)
