import sys
import os
import cPickle
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from pixels import PixelReader
from eventloop.base import Routine


class GetTrack(Routine):
    def __init__(self, output_dir):
        Routine.__init__(self)
        self.pr = None
        self.output_dir = output_dir
    
    # utility functions
    def cut_contains(self, cv, v):
        for c in cv:
            if c[0]<=v and c[1]>=v:
                return True
        return False

    def pixels_affected(self, cs, v):
        return [int(p) for p in cs if self.cut_contains(cs[p], v)]

    def affected_pos(self, cs, v):
        pixels = self.pixels_affected(cs, v)
        pos = np.array([self.pr.getXY(p) for p in pixels])
        return np.mean(pos, 0)

    def get_track(self, cs, time_range):
        start_v = time_range[0]
        end_v = time_range[1]
        return np.vstack([self.affected_pos(cs, v) for v in range(start_v, end_v)])
    
    # event loop functions
    def initialize(self):
        self.pr = PixelReader()
        if not os.path.exists(self.output_dir):
            print '[INFO] Path %s does not exist, creating ...' % self.output_dir
            os.makedirs(self.output_dir)
        
    def execute(self):
        cosig = self.get_context().get_store().get("cosig")
        tod_id = self.get_context().get_id()
        
        cs = cosig['coincident_signals']
        signals = [p[0:2] for p in cosig['peaks']]
        plt.figure(figsize=(10,10))
        self.pr.plot()
        for s in signals:
            pos = self.get_track(cs, s)
            plt.scatter(pos[:,0], pos[:,1], alpha=0.7)
            plt.plot(pos[:,0],pos[:,1])
            plt.savefig(self.output_dir + "%d.png" % tod_id)


class GetTrackWithSpread(GetTrack):
    def __init__(self, output_dir):
        GetTrack.__init__(self, output_dir, downsample = 1)
        self.downsample = 1

    def affected_pos_with_spread(self, cs, v):
        pixels = self.pixels_affected(cs, v)
        pos = np.array([pr.getXY(p) for p in pixels])
        std = np.std(pos, 0)
        spread = np.sqrt(std[0]**2+std[1]**2)
        return np.hstack([np.mean(pos, 0), [spread]])

    def get_track_with_spread(self, cs, time_range):
        start_v = time_range[0]
        end_v = time_range[1]
        return np.vstack([self.affected_pos_with_spread(cs, v) for v in range(start_v, end_v)])   
    
    def execute(self):
        cosig = self.get_context().get_store().get("cosig")
        tod_id = self.get_context().get_id()
 
        cs = cosig['coincident_signals']
        signals = [p[0:2] for p in cosig['peaks']]
        plt.figure(figsize=(10,10))
        self.pr.plot()
        for s in signals:
            pos = self.get_track_with_spread(cs, s)
            pos_downsample = pos[::self.downsample]
            plt.scatter(pos_downsample[:,0], pos_downsample[:,1], marker='o', s=3000*pos_downsample[:,2]**2, alpha=0.1)
            plt.plot(pos[:,0],pos[:,1])
            plt.savefig(output_dir+"%d.png" % tod_id)


class GetTrackDB(GetTrackWithSpread):
    def __init(self, output_dir, downsample):
        GetTrackWithSpread.__init__(self, output_dir, downsample)
        
    def execute(self):
        cosig = self.get_context().get_store().get("cosig")
        tod_id = self.get_context().get_id()
 
        cs = cosig['coincident_signals']
        signals = [p[0:2] for p in cosig['peaks']]
        tracks_db = []
        for s in signals:
            pos = self.get_track_with_spread(cs, s)
            pos_downsample = pos[::self.downsample]
            tracks_db.append(pos_downsample)

        with open(output_dir+str(tod_id)+".pickle", "w") as f:
            cPickle.dump(tracks_db, f, cPickle.HIGHEST_PROTOCOL)
