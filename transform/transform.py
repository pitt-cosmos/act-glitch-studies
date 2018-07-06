from todloop.routines import Logger, DataLoader, SaveData
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from routines import CosigToEvent


loop = TODLoop()
tod_id = 3731
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cosig"))
loop.add_routine(CosigToEvent(input_key="cosig", output_key="events"))
loop.add_routine(SaveData(input_key="events", output_dir="../outputs/s16_pa3_list/events_raw/"))
loop.run(tod_id, tod_id + 1)









