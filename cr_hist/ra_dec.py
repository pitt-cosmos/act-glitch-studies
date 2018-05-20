from todloop.event import LoadRaDec
from todloop.base import TODLoop
from todloop.routines import DataLoader, Logger


loop = TODLoop()
loop.add_tod_list("../data/s16_pa3_list.txt")

loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events_v2", output_key="events"))
loop.add_routine(LoadRaDec(input_key="events", output_key="events"))
loop.add_routine(Logger(input_key="events"))
loop.run(0, 1)
