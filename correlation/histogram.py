import matplotlib
matplotlib.use("TKAgg")
import numpy as np
import matplotlib.pyplot as plt
from todloop.routines import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event
from todloop.utils.hist import Hist1D
from todloop.utils.pixels import PixelReader


class PlotHistogram(Routine):
    
    def __init__(self,events_key):
        Routine.__init__(self)
        self._events_key = events_key 

    def execute(self):
        print '[INFO] Plotting histogram..,'
        event_data = self.get_store().get(self._events_key)
        
        number_of_pixels=[]
        for event in event_data:
            num_pix  = event['number_of_pixels']
            number_of_pixels.append(num_pix)

        plt.hist(number_of_pixels,30)
        plt.grid()
        plt.title("Number of Pixels Affected in Events")
        plt.show()


class CreateHistogram(Routine):
 
    def __init__(self, cosig_key,tod_key, event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None 
        self._tod_key = tod_key
        self._cosig_key = cosig_key
        self._pr = None
    
    def initialize(self):
        self._pr = PixelReader()
        self._hist = Hist1D(0, 8, 100) #change max


    def execute(self):
        cuts = self.get_store().get(self._cosig_key)
        peaks = cuts['peaks']
        cosig = cuts['coincident_signals']
        tod_data = self.get_store().get(self._tod_key)    
        
        def energyseries(pixel, s_time, e_time, buffer=0):

            start_time = s_time - buffer
            end_time = e_time + buffer

            a1, a2 = self._pr.get_f1(pixel)
            b1, b2 = self._pr.get_f2(pixel)
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



        def total_energy(pid,start_time,end_time):


            pix_all_amps = []

            pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[1])
            pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[2])
            pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[3])
            pix_all_amps.append(energyseries(pid,start_time,end_time,buffer=0)[4])

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
                                                                                                                                                                 

                Tot_pW_90a = np.sum(Det_pWatts_90_a)
                Tot_pW_90b = np.sum(Det_pWatts_90_b)
                Tot_pW_150a = np.sum(Det_pWatts_150_a)
                Tot_pW_150b = np.sum(Det_pWatts_150_b)

                Tot_pJ_90a = np.sum(Det_pJoules_90_a)
                Tot_pJ_90b = np.sum(Det_pJoules_90_b)
                Tot_pJ_150a = np.sum(Det_pJoules_150_a)
                Tot_pJ_150b = np.sum(Det_pJoules_150_b)

                values = [Tot_pJ_90a,Tot_pJ_90b,Tot_pJ_150a,Tot_pJ_150b]
                val_sum = np.sum(values)
                min_value = np.amin(values)
                max_value = np.amax(values)

                return val_sum #,values

        event_list=[]
        for event in peaks:
            pixels = pixels_affected_in_event(cosig, event)
            s_time = event[0]
            e_time = event[1]
            event_total_energy = 0
            for pixel in pixels:
                event_total_energy += total_energy(pixel,s_time,e_time) #* 6.241509 # to convert to GeV         
            self._hist.fill(event_total_energy)
            event_list.append(event_total_energy)
    
        e_min = np.min(event_list)    
        e_max = np.max(event_list)
        
        print "Min energy of event:", e_min,'pJoules. Max energy of event:', e_max,'pJoules' 
    
    def finalize(self):
        plt.step(*self._hist.data)
        #plt.xlabel('TOD track:', + str(self._tag))
        plt.ylabel('Events')
        plt.xlabel('in peV')
        #plt.title(
        plt.show()

''' 
OLD CODE FOR REFERENCE

                                         
    def execute(self):
        cuts = self.get_store().get(self._cosig_key)
        peaks = cuts['peaks']
        cosig = cuts['coincident_signals']
        for event in peaks:
            pixels = pixels_affected_in_event(cosig, event)
            s_time = event[0]
            e_time = event[1]
            event_total_energy = 0
            for pixel in pixels:
                event_total_energy += self._te.total_energy(pixel,s_time,e_time)
        energy_hist.fill(event_total_energy)
    def finalize(self):
        plt.step(*self._hist.data)
        plt.show()
                                 
'''
