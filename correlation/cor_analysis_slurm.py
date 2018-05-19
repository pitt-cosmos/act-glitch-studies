from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from todloop.routines import SaveData, DataLoader
from routines import FRBCorrelationFilter
from calibration.routines import FixOpticalSign, CalibrateTOD
from plotter import PlotGlitches
import sys


loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")

#will load the data stored in the folder specified one by one
#and store the loaded data in the shared date store under a key called data
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))
loop.add_routine(FRBCorrelationFilter(tod_key="tod_data", cosig_key="cuts", output_key ="events"))
loop.add_routine(SaveData(input_key="events", output_dir="../outputs/s16_pa3_list/events_v2/"))

start = int(sys.argv[1])
end = int(sys.argv[2])
loop.run(start,end)




