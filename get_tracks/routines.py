import os
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
from eventloop.utils.pixels import PixelReader
from eventloop.base import Routine
from eventloop.utils.cuts import *
mpl.use('Agg')


class GetTracks(Routine):
    def __init__(self, season='2016', array='AR3', downsample=1):
        Routine.__init__(self)
        self._pr = None  # pixel reader
        self._downsample = downsample
        self._season = season
        self._array = array

    def affected_pos_with_spread(self, cs, v):
        pixels = pixels_affected(cs, v)
        pos = np.array([self._pr.get_xy(p) for p in pixels])
        std = np.std(pos, 0)
        spread = np.sqrt(std[0]**2+std[1]**2)
        return np.hstack([np.mean(pos, 0), [spread]])

    def get_tracks_with_spread(self, cs, time_range):
        start_v = time_range[0]
        end_v = time_range[1]
        return np.vstack([self.affected_pos_with_spread(cs, v) for v in range(start_v, end_v)])   

    def initialize(self):
        self._pr = PixelReader(season=self._season, array=self._array)
    
    def execute(self):
        cosig = self.get_context().get_store().get("data")
        cs = cosig['coincident_signals']
        signals = [p[0:2] for p in cosig['peaks']]
        tracks = []
        for s in signals:
            pos = self.get_tracks_with_spread(cs, s)
            pos_downsample = pos[::self._downsample]
            tracks.append(pos_downsample)
            
        # save to data store
        self.get_context().get_store().set("tracks", tracks)

            
class PlotTracks(Routine):
    """A routine that plots the tracks and save to file, it is to be used with GetTracks"""
    def __init__(self, output_dir, season='2016', array='AR3', spreads=True):
        Routine.__init__(self)
        self._output_dir = output_dir
        self._spreads = spreads  # whether to plot spreads
        self._pr = None
        self._season = season
        self._array = array
    
    def initialize(self):
        self._pr = PixelReader(season=self._season, array=self._array)

    def execute(self):
        print self.get_context().get_name()
        tod_id = self.get_context().get_id()
        tracks = self.get_context().get_store().get("tracks")
        print '[INFO] n_tracks = %d' % len(tracks)
        
        plt.figure(figsize=(10, 10))
        self._pr.plot()  # plot the array
        for track in tracks:
            if self._spreads:
                plt.scatter(track[:, 0], track[:, 1], marker='o', s=3000*track[:, 2]**2, alpha=0.1)
                plt.plot(track[:, 0], track[:, 1])
            else:
                plt.scatter(track[:, 0], track[:, 1], alpha=0.7)
        # save image
        print '[INFO] Saving image ...'
        plt.savefig(self._output_dir+"%d.png" % tod_id)
