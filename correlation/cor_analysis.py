from todloop.routines import Logger, DataLoader
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from routines import CRCorrelationFilter, FRBCorrelationFilter, SlowCorrelationFilter, DurationFilter, PixelFilter,ScatterPlot
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

#LOAD TOD DATA 
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))


#FILTER ROUTINES 

#loop.add_routine(PixelFilter(input_key="cuts",output_key="frb_cuts"))
#loop.add_routine(FRBCorrelationFilter(tod_key="tod_data", cosig_key="frb_cuts", output_key ="frb_events",all_coeff_output_key="frb_coeff"))

#loop.add_routine(PixelFilter(max_pixels=10, input_key="cuts", output_key="cr_cuts"))
#loop.add_routine(CRCorrelationFilter(tod_key="tod_data", cosig_key="cr_cuts", output_key= "cr_events",all_coeff_output_key="cr_coeff"))


loop.add_routine(DurationFilter(input_key ="cuts",output_key="slow_cuts"))
loop.add_routine(SlowCorrelationFilter(tod_key="tod_data", cosig_key="slow_cuts", output_key= "slow_events",all_coeff_output_key="slow_coeff"))


#loop.add_routine(ScatterPlot(frb_input_key="frb_coeff",cr_input_key="cr_coeff",slow_input_key="slow_coeff"))

#PLOT A GLITCH (modify plotter.py to plot the specific event)
loop.add_routine(PlotGlitches(tod_key="tod_data", cosig_key="cuts"))


loop.run(1705, 1706)










