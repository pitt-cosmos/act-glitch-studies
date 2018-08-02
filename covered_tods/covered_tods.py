from todloop.routines import DataLoader
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from routines import PlotGlitches
from calibration.routines import FixOpticalSign, CalibrateTOD

tod_id = 1300
loop = TODLoop()
loop.add_tod_list("../data/covered_tods.txt")

loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))
loop.add_routine(PlotGlitches(tag=tod_id,tod_key="tod_data", cosig_key="cuts"))
loop.run(tod_id,tod_id + 1)


