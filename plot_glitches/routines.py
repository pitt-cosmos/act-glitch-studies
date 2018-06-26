import matplotlib
matplotlib.use("TKAgg")
import numpy as np
import matplotlib.pyplot as plt
from todloop.routines import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event


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
        print(pixels_affected_in_event(cuts['coincident_signals'], [88373, 88378, 5, 3]))
        # print('[INFO] pixels affected: ',pixels)
        peaks = cuts['peaks']
        print('[INFO] peaks: ', peaks)

        def cs_cuts():
            cuts = self.get_store().get(self._cosig_key) 
            return cuts['coincident_signals']

        def timeseries(pixel_id, s_time, e_time, buffer=10):

            start_time = s_time - buffer
            end_time = e_time + buffer

            a1, a2 = self._pr.get_f1(pixel_id)
            b1, b2 = self._pr.get_f2(pixel_id)
            d1, d2 = tod_data.data[a1], tod_data.data[a2]
            d3, d4 = tod_data.data[b1], tod_data.data[b2]

            # try to remove the mean from start_time to end_time
            d1 -= np.mean(d1[start_time:end_time])
            d2 -= np.mean(d2[start_time:end_time])
            d3 -= np.mean(d3[start_time:end_time])
            d4 -= np.mean(d4[start_time:end_time])
            
            time = tod_data.ctime - tod_data.ctime[0]
            time = time[start_time:end_time]
            
            d_1 = d1[start_time:end_time]
            d_2 = d2[start_time:end_time]
            d_3 = d3[start_time:end_time]
            d_4 = d4[start_time:end_time]

            """
            UNCOMMENT TO PLOT FOUR CORRESPONDING PIXELS WITH HI-LO FREQ
            plt.plot(time,d_1, '.-', label=str(a1) + ' 90 GHz')
            plt.plot(time, d_2, '.-', label=str(a2) + ' 90 GHz')
            plt.plot(time, d_3, '.-', label=str(b1) + ' 150 GHz')
            plt.plot(time, d_4, '.-', label=str(b2) + ' 150 GHz')
            plt.legend(title='Detector UID')
            plt.show()
            """

            return time, d_1


        """
        PLOTTING FUNCTION
        Plot all pixels affected given an array of pixel ids
        and a starting time and ending time
      
        """
        def plotter(pixels,start_time,end_time):
                        
            for pid in pixels:
               
                x = timeseries(pid,start_time,end_time)[0]
                y = timeseries(pid,start_time,end_time)[1]
                
                plt.title('Pixels affected from ' +str(start_time)+ '-' + str(end_time)+ ' at 90 GHz')
                plt.xlabel('TOD track: 1641')  # CHANGE TOD TRACK NAME
                plt.plot(x,y,'.-')
            
            plt.show()





            
        """
        ALL EVENTS
        From peaks, find cs, then use cs to find all pixels affected
        then plot all pixels affected in all events in peak one by one
        """
        
        cs = cuts['coincident_signals']
        """
        for event in peaks:
            all_pixels = pixels_affected_in_event(cs,event)
            plotter(all_pixels, event[0], event[1])
        """
        
        """
        SPECIFIC EVENT
        To plot specific event, copy event from peaks below 
        """
        #"""
        event = [88373, 88378, 5, 3]
        stime = event[0]
        etime = event[1]
        pixels = pixels_affected_in_event(cs, event)
        plotter(pixels, stime, etime)
        
        self._pr.plot(pixels)
        plt.show()
        #"""


        """
        print(self._pr.get_x_y(24))
        print(self._pr.get_x_y(537))
        print(self._pr.get_x_y(712))

        print(self._pr.get_x_y(199))
        print(self._pr.get_x_y(64))
        print(self._pr.get_x_y(462))
        print(self._pr.get_x_y(322))
        """

