from todloop.routines import DataLoader
from todloop.tod import TODLoader
from todloop.base import TODLoop
from routines import TimeSeries, PlotGlitches, Energy,SaveEvents, NPixelStudy, EnergyStudy,CRCorrelationFilter
from calibration.routines import FixOpticalSign, CalibrateTOD


"""
INITIALIZE TODLoop
"""
loop = TODLoop()
tod_id = 0
"""
ICECUBE

loop.add_tod_list("../data/s17_icecube_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s17_icecube_list/cosig/", output_key="cuts"))
"""

"""
UNCOVERED
"""
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))

"""
COVERED
loop.add_tod_list("../data/covered_tods.txt")
loop.add_routine(DataLoader(input_dir="../outputs/covered_tods_cosig/", output_key="cuts"))
"""

"""
LOAD TOD DATA
"""
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

"""
ROUTINES
"""
loop.add_routine(TimeSeries(tod_key="tod_data",output_key="timeseries"))
loop.add_routine(Energy(timeseries_key="timeseries",output_key="energy_calculator"))
#loop.add_routine(CRCorrelationFilter(timeseries_key="timeseries",cosig_key = "cuts",tod_key="tod_data", output_key= "cr_cuts"))
#loop.add_routine(PlotGlitches(tag=tod_id,cosig_key="cuts",tod_key="tod_data",timeseries_key = "timeseries"))
loop.add_routine(SaveEvents(tag=tod_id,cosig_key ="cuts",tod_key="tod_data",energy_key="energy_calculator",output_key="events"))
loop.add_routine(NPixelStudy(event_key="events"))
#loop.add_routine(EnergyStudy(event_key="events"))

loop.run(tod_id, tod_id + 150)
