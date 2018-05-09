import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
from eventloop.routines import Routine
from eventloop.utils.pixels import PixelReader
import numpy as np
from eventloop.utils.cuts import pixels_affected


class PlotGlitches(Routine):
    """A routine that plot glitches"""
    def __init__(self, cosig_key, tod_key):
        Routine.__init__(self)
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._pr = None

    def initialize(self):
        self._pr = PixelReader()

    def execute(self):
        print '[INFO] Plotting glitches ...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data
        # moby2.tod.remove_mean(tod_data)
        print ('[INFO] cuts: ', cuts)
        pixels = pixels_affected(cuts['coincident_signals'], 256317)
        print('[INFO] pixels affected: ',pixels)

        def timeseries(pixel_id, s_time,e_time, buffer=10):
            #start_time = cuts['coincident_signals'][str(pixel_id)][cut_num][0]
            start_time = s_time
            start_time -= buffer
            #end_time = cuts['coincident_signals'][str(pixel_id)][cut_num][1]
            end_time = e_time
            end_time += buffer
            a1, a2 = self._pr.get_f1(pixel_id)
            b1, b2 = self._pr.get_f2(pixel_id)
            d1, d2 = tod_data.data[a1], tod_data.data[a2]
            d3, d4 = tod_data.data[b1], tod_data.data[b2]

            # try to remove the mean from start_time to end_time
            d1 -= np.mean(d1[start_time:end_time])
            d2 -= np.mean(d2[start_time:end_time])
            d3 -= np.mean(d3[start_time:end_time])
            d4 -= np.mean(d4[start_time:end_time])
            
            # plot the running average over 5 points
            d1 = [np.sum(d1[i:i+5]/5) for i in range(len(d1)-5)]
            d2 = [np.sum(d2[i:i+5]/5) for i in range(len(d2)-5)]
            d3 = [np.sum(d3[i:i+5]/5) for i in range(len(d3)-5)]
            d4 = [np.sum(d4[i:i+5]/5) for i in range(len(d4)-5)]
            
            time = tod_data.ctime - tod_data.ctime[0]
            time = time[start_time:end_time]


            plt.plot(time, d1[start_time:end_time], '.-', label=str(a1) + ' 90 Hz')
            plt.plot(time, d2[start_time:end_time], '.-', label=str(a2) + ' 90 Hz')
            plt.plot(time, d3[start_time:end_time], '.-', label=str(b1) + ' 150 Hz')
            plt.plot(time, d4[start_time:end_time], '.-', label=str(b2) + ' 150 Hz')
            plt.legend(title='Detector UID')
            plt.show()


        timeseries(271,256302, 256332,100)
