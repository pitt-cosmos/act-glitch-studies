from todloop.base import DataLoader
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from routines import Correlation
from calibration.routines import FixOpticalSign, CalibrateTOD
from plotter import PlotGlitches

loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")

#will load the data stored in the folder specified one by one
#and store the loaded data in the shared date store under a key called data
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))
loop.add_routine(TODLoader(output_key="tod_data"))
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))

loop.add_routine(Correlation(tod_key="tod_data", cosig_key="cuts"))

loop.add_routine(PlotGlitches(tod_key="tod_data", cosig_key="cuts"))


loop.run(1393, 1394)




