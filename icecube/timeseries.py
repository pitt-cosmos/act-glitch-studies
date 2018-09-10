from todloop.base import TODLoop
from todloop.routines import DataLoader, Logger
from todloop.tod import TODLoader
from routines import ExtractRaDec
from calibration.routines import FixOpticalSign, CalibrateTOD


loop = TODLoop()
loop.add_tod_list("../data/s17_icecube_list.txt")

# Load TODs
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

# A routine that loads tod data associated with a specific ra / dec ranges
loop.add_routine(ExtractRaDec(input_key="tod_data", output_key="snippets", \
                              ra_range=[1.29, 1.40], dec_range=[0.082, 0.118]))

#loop.add_routine(Logger(input_key="snippets"))
loop.run(0, 100)
