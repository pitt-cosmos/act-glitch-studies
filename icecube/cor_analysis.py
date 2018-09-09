from todloop.routines import Logger, DataLoader, SaveData
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from correlation.routines import CRCorrelationFilter, FRBCorrelationFilter, SlowCorrelationFilter, DurationFilter, PixelFilter, ScatterPlot, EdgeFilter
from calibration.routines import FixOpticalSign, CalibrateTOD

loop = TODLoop()
loop.add_tod_list("../data/s17_icecube_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s17_icecube_list/cosig/", output_key="cuts"))


# LOAD TOD DATA 
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

#loop.add_routine(PixelFilter(input_key="cuts",output_key="frb_cuts"))
#loop.add_routine(DurationFilter(max_duration=5,input_key="frb_cuts",output_key="frb_cuts"))
#loop.add_routine(FRBCorrelationFilter(tod_key="tod_data", cosig_key="frb_cuts", output_key ="frb_events",all_coeff_output_key="frb_coeff"))
#loop.add_routine(EdgeFilter(input_key="frb_events",output_key="frb_events"))

#loop.add_routine(PixelFilter(min_pixels=4,max_pixels=10, input_key="cuts", output_key="cr_cuts"))
loop.add_routine(CRCorrelationFilter(tod_key="tod_data", cosig_key="cuts", output_key= "events", all_coeff_output_key="cr_coeff", season='2017'))
loop.add_routine(SaveData(input_key="events", output_dir="../outputs/s17_icecube_list/events/"))

#loop.add_routine(DurationFilter(min_duration=50,input_key ="cuts",output_key="slow_cuts"))
#loop.add_routine(SlowCorrelationFilter(tod_key="tod_data", cosig_key="slow_cuts", output_key= "slow_events",all_coeff_output_key="slow_coeff"))

loop.run(100, 155)
