from todloop.base import TODLoop
from todloop.tod import TODLoader
from routines import FixOpticalSign


loop = TODLoop()
loop.add_tod_list("data/s16_pa3_list.txt")

loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data"))
