from todloop.routines import Logger, DataLoader
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from correlation.routines import FRBCorrelationFilter, SlowCorrelationFilter
from routines import CRCorrelationFilter
from calibration.routines import FixOpticalSign, CalibrateTOD
from plotter import PlotGlitches
from histogram import PlotHistogram 

loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")

#will load the data stored in the folder specified one by one
#and store the loaded data in the shared date store under a key called data
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))

#LOAD FILTERED DATA (UPTO TRACK 5000) AND PLOT A HISTOGRAM OF # OF PIXELS AFFECTED
#loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/",output_key ="events"))
#loop.add_routine(Logger(input_key="events"))
#loop.add_routine(PlotHistogram(events_key="events"))

#LOAD TOD  DATA 
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

#FILTER ROUTINES (frb_routines.py, routines.py, slow_routines.py)
#loop.add_routine(FRBCorrelationFilter(tod_key="tod_data", cosig_key="cuts", output_key ="frb_events"))
#loop.add_routine(CRCorrelationFilter(tod_key="tod_data", cosig_key="cuts", output_key= "cr_events"))
#loop.add_routine(SlowCorrelationFilter(tod_key="tod_data", cosig_key="cuts", output_key= "slow_events"))

#PLOT A GLITCH (modify plotter.py to plot the specific event)
loop.add_routine(PlotGlitches(tod_key="tod_data", cosig_key="cuts"))

loop.run(10000,10001)






