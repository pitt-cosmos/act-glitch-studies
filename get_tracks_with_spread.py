import sys
import cPickle
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from pixels import PixelReader
import numpy as np
import traceback


# Auxilary functions
def cut_contains(cv, v):
    for c in cv:
        if c[0]<=v and c[1]>=v:
            return True
    return False

def pixels_affected(cs, v):
    return [int(p) for p in cs if cut_contains(cs[p], v)]

def affected_pos_with_spread(cs, v):
    pixels = pixels_affected(cs, v)
    pos = np.array([pr.getXY(p) for p in pixels])
    std = np.std(pos, 0)
    spread = np.sqrt(std[0]**2+std[1]**2)
    return np.hstack([np.mean(pos, 0), [spread]])

def get_track_with_spread(cs, time_range):
    start_v = time_range[0]
    end_v = time_range[1]
    return np.vstack([affected_pos_with_spread(cs, v) for v in range(start_v, end_v)])

if __name__ == "__main__":
    input_dir = "outputs/coincident_signals_subset/"
    output_dir = "outputs/tracks_with_spread/"
    downsample = 1
    pr = PixelReader()
    start = int(sys.argv[1])
    end = int(sys.argv[2])

    for cut_id in range(start, end):
        try: 
            print '[INFO] Working on', cut_id
            cut_data = cPickle.load(open(input_dir+"%d.pickle" % cut_id, "r"))
            cs = cut_data['coincident_signals']
            signals = [p[0:2] for p in cut_data['peaks']]
            plt.figure(figsize=(10,10))
            pr.plot()
            for s in signals:
                pos = get_track_with_spread(cs, s)
                pos_downsample = pos[::downsample]
                plt.scatter(pos_downsample[:,0], pos_downsample[:,1], marker='o', s=3000*pos_downsample[:,2]**2, alpha=0.1)
                plt.plot(pos[:,0],pos[:,1])
            plt.savefig(output_dir+"%d.png" % cut_id)
        except Exception as e:
            print "[ERROR] Exception caught!"
            print e
            traceback.print_exc(file=sys.stdout)
