from todloop.event import LoadRaDec, NPixelFilter, CoeffFilter, DurationFilter
from todloop.routines import DataLoader
from todloop.tod import TODLoader
from todloop.base import TODLoop
from routines import TimeSeries, PlotGlitches, Energy,SaveEvents, NPixelStudy, EnergyStudy,CRCorrelationFilter, RaDecFilter,Timer
from calibration.routines import FixOpticalSign, CalibrateTOD


"""
INITIALIZE TODLoop
"""
loop = TODLoop()
tod_id = 15
loop.add_routine(Timer())
"""
ICECUBE
"""
#"""
loop.add_tod_list("../data/s17_icecube_list.txt")
loop.add_skip([128,129,130,131])
loop.add_routine(DataLoader(input_dir="../outputs/s17_icecube_list/cosig/", output_key="cuts"))
#"""



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
loop.add_routine(SaveEvents(tag=tod_id,cosig_key ="cuts",tod_key="tod_data",energy_key="energy_calculator",output_key="events")) 
loop.add_routine(LoadRaDec(input_key="events", output_key="events"))
loop.add_routine(RaDecFilter(input_key="events", ra_range=[1.2, 1.4], dec_range=[0.08, 0.11],output_key="events"))
loop.add_routine(NPixelFilter(min_pixels=0, max_pixels=3, input_key="events", output_key="events"))
#loop.add_routine(CRCorrelationFilter(timeseries_key="timeseries",input_key="events",tod_key="tod_data", output_key= "events"))          
loop.add_routine(PlotGlitches(tag=tod_id,input_key="events",tod_key="tod_data",timeseries_key = "timeseries"))
#loop.add_routine(NPixelStudy(event_key="events"))
loop.add_routine(EnergyStudy(event_key="events"))

loop.run(tod_id, tod_id + 1)
