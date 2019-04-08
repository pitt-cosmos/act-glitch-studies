from todloop.routines import DataLoader
from todloop.tod import TODLoader
from todloop.base import TODLoop
from routines import TimeSeries, PlotGlitches, Energy,SaveEvents, NPixelStudy, EnergyStudy,CRCorrelationFilter, FRBCorrelationFilter,EdgeFilter, Deconvolution, Convolution, NEventsStudy, TimeConstant,PlotDetectorGlitches
from calibration.routines import FixOpticalSign, CalibrateTOD


"""
INITIALIZE TODLoop
"""
loop = TODLoop()
tod_id = 10000
"""
ICECUBE
"""
"""
loop.add_tod_list("../data/s17_icecube_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s17_icecube_list/cosig/", output_key="cuts"))
"""

"""
UNCOVERED
"""

#"""
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))
#"""

"""
COVERED
"""

"""
loop.add_tod_list("../data/covered_tods.txt")
loop.add_routine(DataLoader(input_dir="../outputs/covered_tods_cosig/", output_key="cuts"))
"""

"""
LOAD TOD DATA
"""
loop.add_routine(TODLoader(output_key="tod_data"))
#loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
#loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

"""
ROUTINES
"""
#loop.add_routine(Convolution(data="act_frb180110.txt",tau=0.0007))
#loop.add_routine(Convolution(data='deltafunc.txt',tau=0.0007))
#loop.add_routine(Deconvolution(input_key="tod_data",output_key="tod_data"))
loop.add_routine(TimeConstant(input_key='tod_data',output_key='time_constants'))
loop.add_routine(TimeSeries(tod_key="tod_data",output_key="timeseries"))
#loop.add_routine(Energy(timeseries_key="timeseries",output_key="energy_calculator"))
#loop.add_routine(FRBCorrelationFilter(timeseries_key="timeseries",cosig_key="cuts",tod_key="tod_data",output_key="frb_cuts"))
#loop.add_routine(CRCorrelationFilter(timeseries_key="timeseries",cosig_key = "cuts",tod_key="tod_data", output_key= "cr_cuts"))
#loop.add_routine(PlotGlitches(tag=tod_id,cosig_key="frb_cuts",tod_key="tod_data",timeseries_key = "timeseries"))
loop.add_routine(PlotDetectorGlitches(detuid=796,tag=tod_id,cosig_key="cuts",tod_key="tod_data",timeseries_key="timeseries",time_constants="time_constants"))
#loop.add_routine(SaveEvents(tag=tod_id,cosig_key ="frb_cuts",tod_key="tod_data",energy_key="energy_calculator",output_key="events"))
#loop.add_routine(EdgeFilter(input_key="events",output_key="events"))
#loop.add_routine(NPixelStudy(event_key="events"))
#loop.add_routine(EnergyStudy(event_key="events"))
#loop.add_routine(NEventsStudy(allevents_key="peaks",event_key="frb_cuts"))

loop.run(tod_id, tod_id + 1)
