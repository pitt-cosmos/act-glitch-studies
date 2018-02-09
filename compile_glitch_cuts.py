""" This script is used to extract cuts """
import sys
from moby2.scripting import get_filebase
import cPickle as pickle
import moby2

# define glitch cut parameters
glitchp ={ 'nSig': 10, 'tGlitch' : 0.007, 'minSeparation': 30, 'maxGlitch': 50000, 'highPassFc': 6.0, 'buffer': 0 }

# load cut results from loic
with open("data/mr3_pa3_s16_results.pickle", "r") as f:
    cut_results = pickle.load(f)

# get all tod names
tod_names = cut_results['name']
tod_sel = cut_results['sel']

# define starting tod and ending tod
start = int(sys.argv[1])
end = int(sys.argv[2])

# get file base
fb = get_filebase()

# loop over the tods
for n in range(start, end):
    tod_name = tod_names[n]
    tod_filename = fb.filename_from_name(tod_name, single=True)
    print '[INFO] Looking at TOD:', tod_name # TODO: better logs
    tod_data = moby2.scripting.get_tod({'filename': tod_filename, 'repair_pointing': True})
    print '[INFO] Get TOD successfully'

    print '[INFO] Finding glitches'
    cuts = moby2.tod.get_glitch_cuts(tod=tod_data, params=glitchp)
    print "[INFO] Finding glitches done"

    # Save into pickle file
    meta = {
        "TOD": tod_name,
        "glitch_param": glitchp, # save the parameters used to generate
        "sel": tod_sel[:,n], # save the detector mask (indicating which one is good or bad)
        "cuts": cuts # save the cuts
    }
    pickle.dump(meta, open("outputs/cuts/" + str(n) + ".cut", "wb"), pickle.HIGHEST_PROTOCOL)
    print("Cut for TOD " + str(n) + " written successfully")
