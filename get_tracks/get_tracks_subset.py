import sys
import cPickle
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from pixels import PixelReader
import numpy as np


# Auxilary functions
def cut_contains(cv, v):
    for c in cv:
        if c[0]<=v and c[1]>=v:
            return True
    return False

def pixels_affected(cs, v):
    return [int(p) for p in cs if cut_contains(cs[p], v)]

def affected_pos(cs, v):
    pixels = pixels_affected(cs, v)
    pos = np.array([pr.getXY(p) for p in pixels])
    return np.mean(pos, 0)

def get_track(cs, time_range):
    start_v = time_range[0]
    end_v = time_range[1]
    return np.vstack([affected_pos(cs, v) for v in range(start_v, end_v)])

if __name__ == "__main__":
    pr = PixelReader()
    start = int(sys.argv[1])
    end = int(sys.argv[2])

    for cut_id in range(start, end):
        try: 
            print '[INFO] Working on', cut_id
            cut_data = cPickle.load(open("outputs/coincident_signals_subset/%d.pickle" % cut_id, "r"))
            cs = cut_data['coincident_signals']
            signals = [p[0:2] for p in cut_data['peaks']]
            plt.figure(figsize=(10,10))
            pr.plot()
            for s in signals:
                pos = get_track(cs, s)
                plt.scatter(pos[:,0], pos[:,1], alpha=0.7)
                plt.plot(pos[:,0],pos[:,1])
            plt.savefig("outputs/tracks_subset/%d.png" % cut_id)
        except Exception as e:
            print "[ERROR] Exception caught!"
            print e
