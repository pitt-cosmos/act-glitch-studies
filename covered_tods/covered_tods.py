from todloop.routines import DataLoader
from todloop.tod import TODLoader
from todloop.base import TODLoop
from routines import PlotGlitches,SaveEvents,NPixelStudy
from calibration.routines import FixOpticalSign, CalibrateTOD
from correlation.routines import CorrelationFilter, CRCorrelationFilter

"""
INITIALIZE TODLoop
"""
loop = TODLoop()
tod_id = 91
loop.add_tod_list("../data/covered_tods.txt")
loop.add_routine(DataLoader(input_dir="../outputs/covered_tods_cosig/", output_key="cuts"))

"""
LOAD TOD DATA
"""
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

"""
ROUTINES
"""
#loop.add_routine(PlotGlitches(tag=tod_id,tod_key="tod_data", cosig_key="cuts"))
loop.add_routine(SaveEvents(tod_key="tod_data",cosig_key="cuts",output_key="events"))
loop.add_routine(NPixelStudy(event_key="events"))

loop.run(tod_id, tod_id + 5)
