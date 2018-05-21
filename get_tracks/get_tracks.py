from todloop.base import TODLoop
from todloop.routines import DataLoader
from todloop.filters import DurationFilter, PixelFilter, SpreadFilter
from routines import GetTracks, PlotTracks

loop = TODLoop()
loop.add_tod_list("data/s17_pa4_sublist.txt")

# add sample handler
loop.add_routine(DataLoader(input_dir="outputs/s17_pa4_sublist_cosig/"))
#loop.add_routine(DataLoader(input_dir="outputs/coincident_signals_subset/"))

# add filters
#loop.add_routine(DurationFilter(max_duration=10))
#loop.add_routine(PixelFilter(max_pixels=5))

# add main routine
loop.add_routine(GetTracks(season='2017', array='AR4'))
#loop.add_routine(SpreadFilter(max_spread=1))

# add plot routine
#loop.add_routine(PlotTracks(output_dir="outputs/get_tracks_filtered/", season='2017', array='AR4'))
loop.add_routine(PlotTracks(output_dir="outputs/s17_pa4_sublist_tracks/", season='2017', array='AR4'))

# specify range of tods of interests 
loop.run(0, 2)
