import matplotlib
matplotlib.use("TKAgg")
import numpy as np
import matplotlib.pyplot as plt
from todloop.routines import Routine
from todloop.utils.pixels import PixelReader


class PlotEvents(Routine):
    """A routine that plot events"""
    def __init__(self, event_key, tod_key):
        Routine.__init__(self)
        self._event_key = event_key
        self._tod_key = tod_key
        self._pr = None

    def initialize(self):
        self._pr = PixelReader()

    def execute(self):
        print '[INFO] Plotting glitches ...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data
        events = self.get_store().get(self._event_key)  # retrieve tod_data
        
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
        def plotter(axes, pixels,start_time,end_time):
                        
            for pid in pixels:
               
                x = timeseries(pid,start_time,end_time)[0]
                y = timeseries(pid,start_time,end_time)[1]

                fig.title('Pixels affected from ' +str(start_time)+ '-' + str(end_time)+ ' at 90 GHz')
                plt.xlabel('TOD_ID: %d    TOD_NAME: %s' % (self.get_id(), self.get_name()))  # CHANGE TOD TRACK NAME
                plt.plot(x,y,'.-')
            
            plt.show()

            
        """
        ALL EVENTS
        Plot all pixels affected in a event one by one for all events
        """

        # old
        for event in events:
            pixels_affected = event['pixels_affected']
            start_time = event['start']
            end_time = event['end']
            
            plt.subplot(121)
            print '[INFO] Number of pixels affected: %d' % event['number_of_pixels']
            for pid in pixels_affected:
               
                x = timeseries(pid,start_time,end_time)[0]
                y = timeseries(pid,start_time,end_time)[1]

                plt.title('Pixels affected from ' +str(start_time)+ '-' + str(end_time)+ ' at 90 GHz')
                plt.xlabel('TOD_ID: %d    TOD_NAME: %s' % (self.get_id(), self.get_name()))  # CHANGE TOD TRACK NAME
                plt.plot(x,y,'.-')
            
            # plt.show()
            plt.subplot(122)
            # new
            print '[INFO] Pixel Location in Row and Col Space:'
            pix_max_amps = []
            pix_max_x = []
            pix_max_y = []
            x, y = self._pr.get_x_y_array()
            plt.plot(x, y, 'r.')

            for pid in pixels_affected:
                print '[INFO] Pixel #', pid, 'at', self._pr.get_row_col(pid)
                pixel_max_amp = np.amax(timeseries(pid, start_time, end_time)[1])
                # print '[INFO] Maximum Amplitude of Pixel #', pid, 'is', pixel_max_amp
                x, y = self._pr.get_x_y(pid)
                pix_max_amps.append(pixel_max_amp)
                pix_max_x.append(x)
                pix_max_y.append(y)

            max_alpha = np.amax(pix_max_amps)
            

            for n in np.arange(0, len(pix_max_amps)):
                plt.plot(pix_max_x[n], pix_max_y[n], 'b.', alpha=0.8 * (pix_max_amps[n] / max_alpha), markersize=40)

            plt.show()



