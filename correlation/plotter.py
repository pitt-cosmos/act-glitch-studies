import matplotlib
matplotlib.use("TKAgg")
import json
import numpy as np
import scipy.stats as ss
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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

    def initialize(self):
        self._pr = PixelReader()

    def execute(self):
        plot = raw_input("Do you want to plot an event? Enter y/n: ")
        if plot == "y":
            #print '[INFO] Plotting glitch ...'
            tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data
            cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data
            peaks = cuts['peaks']
            #print('[INFO] peaks: ', peaks)
        
            def timeseries(pixel_id, s_time, e_time, buffer=10):

                start_time = s_time - buffer
                end_time = e_time + buffer
                
                a1, a2 = self._pr.get_f1(pixel_id)
                d1, d2 = tod_data.data[a1], tod_data.data[a2]

                # try to remove the mean from start_time to end_time
                d1 -= np.mean(d1[start_time:end_time])
                
                time = tod_data.ctime - tod_data.ctime[0]
                time = time[start_time:end_time]
            
                d_1 = d1[start_time:end_time]
            
                return time, d_1


            def energyseries(pixel_id, s_time, e_time, buffer=0):

                start_time = s_time - buffer
                end_time = e_time + buffer

                a1, a2 = self._pr.get_f1(pixel_id)
                b1, b2 = self._pr.get_f2(pixel_id)
                d1, d2 = tod_data.data[a1], tod_data.data[a2]
                d3, d4 = tod_data.data[b1], tod_data.data[b2]

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
            Plot all pixels affected given an array of pixel id
            and a starting time and ending time
           
            """

            def plotter(pixels,start_time,end_time):

                plt.figure(figsize = (8,8))
                gridspec.GridSpec(11,11)

                plt.subplot2grid((11,11), (0,0), colspan=11, rowspan=3)                
                for pid in pixels:
               
                    x = timeseries(pid,start_time,end_time)[0]
                    y = timeseries(pid,start_time,end_time)[1]
                
                    plt.plot(x,y,'.-')
                    plt.title('Pixels affected from ' +str(start_time)+ '-' + str(end_time)+ ' at 90 GHz')
                    plt.xlabel('TOD track:' + str(self._tag))  # CHANGE TOD TRACK NAME

                pix_max_amps = []
                pix_max_x = []
                pix_max_y = []
                pix_location_row = []
                pix_location_col = []
                                                
                x1, y1 = self._pr.get_x_y_array()
                plt.subplot2grid((11,11), (4,0), colspan=7, rowspan=7)
                plt.plot(x1,y1,'r.')


                def total_energy(pid,start_time,end_time):

                    pix_id_lat = []
                    pix_all_amps = []
                    freq_list = []                
                                    
                    pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[1])
                    pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[2])
                    pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[3])
                    pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[4])
                    
                    pix_id_lat.extend((pid, pid, pid, pid))
                    freq_list.extend((90,90,150,150))

                    
                    Det_pWatts_90_a = []
                    Det_pWatts_90_b = []
                    Det_pWatts_150_a = []
                    Det_pWatts_150_b = []
                    
                    Det_pJoules_90_a = []
                    Det_pJoules_90_b = []
                    Det_pJoules_150_a = []
                    Det_pJoules_150_b = []
                    
                    for i in range(0, len(pix_all_amps),4):
                        ampid_1 = pix_all_amps[i]
                        array_min_1 = np.amin(ampid_1)
                        new_pix_amps_1 = ampid_1-array_min_1
                        pWatts_1 = np.sum(new_pix_amps_1)*10**(12)/(400.)
                        Det_pWatts_90_a.append(pWatts_1)
                        Det_pJoules_90_a.append(pWatts_1*(end_time-start_time))
                        
                        ampid_2 = pix_all_amps[i+1]
                        array_min_2 = np.amin(ampid_2)
                        new_pix_amps_2 = ampid_2-array_min_2
                        pWatts_2 = np.sum(new_pix_amps_2)*10**(12)/(400.)
                        Det_pWatts_90_b.append(pWatts_2)
                        Det_pJoules_90_b.append(pWatts_2*(end_time-start_time))
                        
                        ampid_3 = pix_all_amps[i+2]
                        array_min_3 = np.amin(ampid_3)
                        new_pix_amps_3 = ampid_3-array_min_3
                        pWatts_3 = np.sum(new_pix_amps_3)*10**(12)/(400.)
                        Det_pWatts_150_a.append(pWatts_3)
                        Det_pJoules_150_a.append(pWatts_3*(end_time-start_time))
                        
                        ampid_4 = pix_all_amps[i+3]
                        array_min_4 = np.amin(ampid_4)
                        new_pix_amps_4 = ampid_4-array_min_4
                        pWatts_4 = np.sum(new_pix_amps_4)*10**(12)/(400.)
                        Det_pWatts_150_b.append(pWatts_4)
                        Det_pJoules_150_b.append(pWatts_4*(end_time-start_time))


                        Tot_pW_90a = np.sum(Det_pWatts_90_a)
                        Tot_pW_90b = np.sum(Det_pWatts_90_b)
                        Tot_pW_150a = np.sum(Det_pWatts_150_a)
                        Tot_pW_150b = np.sum(Det_pWatts_150_b)
                        
                        Tot_pJ_90a = np.sum(Det_pJoules_90_a)
                        Tot_pJ_90b = np.sum(Det_pJoules_90_b)
                        Tot_pJ_150a = np.sum(Det_pJoules_150_a)
                        Tot_pJ_150b = np.sum(Det_pJoules_150_b)
                        
                        #print '[INFO] Total Power, 90a is', Tot_pW_90a, 'pWatts'                                                                                                            
                        print '[INFO] Total Energy, 90a is', Tot_pJ_90a, 'pJoules'
                        
                        #print '[INFO] Total Power, 90b is', Tot_pW_90b, 'pWatts'                                                                                                            
                        print '[INFO] Total Energy, 90b is', Tot_pJ_90b, 'pJoules'
                        
                        #print '[INFO] Total Power, 150a is', Tot_pW_150a, 'pWatts'                                                                                                          
                        print '[INFO] Total Energy, 150a is', Tot_pJ_150a, 'pJoules'
                        
                        #print '[INFO] Total Power, 150b  is', Tot_pW_150b, 'pWatts'                                                                                                         
                        print '[INFO] Total Energy, 150b is', Tot_pJ_150b, 'pJoules'

                for pid in pixels:

                    pixel_max_amp_1 = np.amax(timeseries(pid,start_time,end_time)[1])
                    x, y = self._pr.get_x_y(pid)
                    pix_max_amps.append(pixel_max_amp_1)

                    pix_max_x.append(x)
                    pix_max_y.append(y)
                    a1, a2 = self._pr.get_f1(pid)
                    b1, b2 = self._pr.get_f2(pid)    
                    pix_location_row.append(np.float(self._pr.get_row_col(a1)[0])) 
                    pix_location_col.append(np.float(self._pr.get_row_col(a1)[1]))
                    pix_location_row.append(np.float(self._pr.get_row_col(a2)[0]))             
                    pix_location_col.append(np.float(self._pr.get_row_col(a2)[1]))
                    pix_location_row.append(np.float(self._pr.get_row_col(b1)[0]))             
                    pix_location_col.append(np.float(self._pr.get_row_col(b1)[1]))
                    pix_location_row.append(np.float(self._pr.get_row_col(b2)[0]))             
                    pix_location_col.append(np.float(self._pr.get_row_col(b2)[1]))  
                    
                    print 'Detector UID: ', pid
                    total_energy(pid,start_time,end_time)
                    
                    #print 'get row of a1 is', np.float(self._pr.get_row_col(a1)[0]),'Row - Cornell', np.floor(pid/32.)
                    #print 'get col of a1 is', np.float(self._pr.get_row_col(a1)[1]),'Col - Cornell method', pid - np.floor(pid/32.)*32. 
               
                
                max_alpha = np.amax(pix_max_amps)
                for n in np.arange(0,len(pix_max_amps)):
                    plt.plot(pix_max_x[n],pix_max_y[n], 'b.', alpha=0.8*(pix_max_amps[n]/max_alpha), markersize=20)
                 
                plt.subplot2grid((11,11), (6,8), colspan=4, rowspan=4)
                plt.plot(pix_location_col,pix_location_row, 'b.', alpha = 1, markersize=10)
                plt.title('Location of Affected Pixels',fontsize=10)
                plt.xticks(np.arange(min(pix_location_col)-1, max(pix_location_col)+2, 1.0))
                plt.xlabel('Column', fontsize=8)
                plt.yticks(np.arange(min(pix_location_row)-1, max(pix_location_row)+2, 1.0))
                plt.ylabel('Row', fontsize=8)
                plt.xticks(fontsize=5)
                plt.yticks(fontsize=5)
                plt.grid(color='k', linewidth=1)
                plt.show() 
              
                    

            """
            SPECIFIC EVENT
            To plot specific event, copy event from peaks below 
            """
            cs = cuts['coincident_signals']
            e = raw_input('Please copy the event list you would like to plot:')
            event = json.loads(e)
            #event = [260584, 260589, 5, 2]
            stime = event[0]
            etime = event[1]
            pixels = pixels_affected_in_event(cs, event)
            print '[INFO] Plotting Glitch...'
            plotter(pixels, stime, etime)

            y_n = ' '
            
            while y_n != 'n':
                y_n = raw_input ("Would you like to plot another event? Enter y/n...")
                if y_n == 'y':
                    e= raw_input('Please copy the event list you would like to plot:')
                    event = json.loads(e)
                    stime = event[0]
                    etime = event[1]
                    pixels = pixels_affected_in_event(cs, event)
                    print '[INFO] Plotting Glitch...'
                    plotter(pixels, stime, etime)
        else:
            print 'No plot will be displayed!'
