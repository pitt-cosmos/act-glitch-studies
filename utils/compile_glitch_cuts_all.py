""" This script is used to extract cuts """
import sys
from moby2.scripting import get_filebase
import cPickle as pickle
import moby2

# define glitch cut parameters
glitchp ={ 'nSig': 10, 'tGlitch' : 0.007, 'minSeparation': 30, 'maxGlitch': 50000, 'highPassFc': 6.0, 'buffer': 0 }

# load pickled tod list
with open("data/tods.pickle", "r") as f:
    tods_all = pickle.load(f)

array = 'AR3'
tods = [tod for tod in tods_all if tod.array==array]
# define starting tod and ending tod
start = int(sys.argv[1])
end = int(sys.argv[2])

# get file base
fb = get_filebase()

print '[INFO] Total number of TODs: %d' % len(tods)
# loop over the tods
for n in range(start, end):
    try:
        tod_name = tods[n].basename
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
            "cuts": cuts # save the cuts
        }
        pickle.dump(meta, open("outputs/cuts_all/" + str(n) + ".cut", "wb"), pickle.HIGHEST_PROTOCOL)
        print "Cut for TOD " + str(n) + " written successfully"
    except Exception as e:
        print "[ERROR] Exception caught on", tod_name
