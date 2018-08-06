from todloop.routines import DataLoader
from todloop.tod import TODLoader
from todloop.base import TODLoop
from routines import PlotGlitches
from calibration.routines import FixOpticalSign, CalibrateTOD


loop = TODLoop()
tod_id = 10
loop.add_tod_list("../data/covered_tods.txt")
loop.add_routine(DataLoader(input_dir="../outputs/covered_tods_cosig/", output_key="cuts"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))
loop.add_routine(PlotGlitches(tag=tod_id,tod_key="tod_data", cosig_key="cuts"))

loop.run(tod_id, tod_id + 1)
