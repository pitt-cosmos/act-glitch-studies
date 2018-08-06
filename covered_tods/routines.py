import matplotlib
matplotlib.use("TKAgg")
import json
import numpy as np
import matplotlib.pyplot as plt
from todloop.routines import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event


class PlotGlitches(Routine):
    """A routine that plot glitches"""
    def __init__(self, tag, cosig_key, tod_key):
        Routine.__init__(self)
        self._tag = tag
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._pr = None


    def execute(self):
        print '[INFO] Loading Glitch Data ...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data                                                    
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data                                                    
        array_name = raw_input("Name of array? ")
        peaks = cuts['peaks']
        print('[INFO] peaks: ', peaks)
        self._pr = PixelReader(season='2017',array = str(array_name))        
               
        plot = raw_input("Do you want to plot an event? Enter y/n: ")
        if plot == "y":
            tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data     
            cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data
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
                
                
                return time, d_1, d_2, d_3, d_4


            """
            PLOTTING FUNCTION
            Plot all pixels affected given an array of pixel ids
            and a starting time and ending time
            
            """
            def plotter(pixels,start_time,end_time):
                        
                for pid in pixels:
               
                    x = timeseries(pid,start_time,end_time)[0]
                    y1 = timeseries(pid,start_time,end_time)[1]
                    y2 = timeseries(pid,start_time,end_time)[2]
                    y3 = timeseries(pid,start_time,end_time)[3]
                    y4 = timeseries(pid,start_time,end_time)[4]
                    
                    
                    plt.title('Pixel affected from ' +str(start_time)+ '-' + str(end_time)+ ', Pixel ' + str(pid))
                    plt.xlabel('TOD track:' + str(self._tag))  # CHANGE TOD TRACK NAME
                    plt.plot(x,y1,'.-',label='90 GHz')
                    plt.plot(x,y2,'.-',label='90 GHz')
                    plt.plot(x,y3,'.-',label='150 GHz')
                    plt.plot(x,y4,'.-',label='150 GHz')
                    
                    plt.legend()
                    plt.show()


                
            """
            SPECIFIC EVENT
            To plot specific event, copy event from peaks below 
            """
            cs = cuts['coincident_signals']            
            e = raw_input('Please copy the event list to plot 4 freq channels:')
            event = json.loads(e)
            stime = event[0]
            etime = event[1]
            pixels = pixels_affected_in_event(cs, event)
            plotter(pixels, stime, etime)
            
            self._pr.plot(pixels)
            plt.show()
                
            y_n = ' '
                
            while y_n != 'n':
                y_n = raw_input ("Would you like to plot another event? Enter y/n...")
                if y_n == 'y':
                    e= raw_input('Please copy the event list to plot 4 freq channels:')
                    event = json.loads(e)
                    stime = event[0]
                    etime = event[1]
                    pixels = pixels_affected_in_event(cs, event)
                    print '[INFO] Plotting Glitch...'
                    plotter(pixels, stime, etime)
                    self._pr.plot(pixels)
                    plt.show()
                        
        else:
            print 'No plot will be displayed!'      


