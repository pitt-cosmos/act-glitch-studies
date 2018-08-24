import matplotlib
matplotlib.use("TKAgg")
import json
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from todloop.routines import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event
from todloop.utils.hist import Hist1D 


class TimeSeries(Routine):
    """ A routine that returns a function to find the timeseries of a pixel in 4 frequencies """
    def __init__(self,tod_key,output_key):
        Routine.__init__(self)
        self._tod_key = tod_key
        self._pr = None
        self._output_key = output_key

    def initialize(self):
        self._pr = PixelReader()
        
    def execute(self):
        print '[INFO] Getting timeseries...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data                                                                                                     

    
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

        self.get_store().set(self._output_key,timeseries)

class PlotGlitches(Routine):
    """A routine that plots glitches """
    def __init__(self, tag, cosig_key, tod_key,timeseries_key):
        Routine.__init__(self)
        self._tag = tag
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._timeseries_key = timeseries_key
        self._pr = None
    
    def initialize(self):
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data                                                                        
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data                                                                          


    def execute(self):
        print '[INFO] Loading Glitch Data ...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data                                                    
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data                                                    
        array_name = self.get_array()
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
            
        
            timeseries = self.get_store().get(self._timeseries_key)
            

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
                    plt.xlabel('TOD track:' + str(self._tag)) 
                    plt.plot(x,y1,'.-',label='90 GHz')
                    plt.plot(x,y2,'.-',label='90 GHz')
                    plt.plot(x,y3,'.-',label='150 GHz')
                    plt.plot(x,y4,'.-',label='150 GHz')
                    
                    plt.legend()
                    plt.show()


                
            """
            SPECIFIC EVENT
            To plot specific event, this interface will ask you to supply the event list, make sure you 
            manually convert the last string to a float or integer
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

class Energy(Routine):
    """ A routine that returns a function to calculate the energy per detector in a pixel """

    def __init__(self,timeseries_key,output_key):
        Routine.__init__(self)
        self._timeseries_key = timeseries_key
        self._output_key = output_key 


    def execute(self):
        print '[INFO] Running energy analysis...'
        timeseries = self.get_store().get(self._timeseries_key)
    
        """
        Calculate the energy of each detector in an affected pixel
        """

        def energy_calculator(pid,stime,etime):
            all_amps = []
            all_amps.append(timeseries(pid,stime,etime,buffer=0)[1])
            all_amps.append(timeseries(pid,stime,etime,buffer=0)[2])
            all_amps.append(timeseries(pid,stime,etime,buffer=0)[3])
            all_amps.append(timeseries(pid,stime,etime,buffer=0)[4])
        
            pJ_90a, pJ_90b, pJ_150a, pJ_150b = [],[],[],[]
        
            for i in range(0,len(all_amps),4):
                amp_90a,amp_90b,amp_150a,amp_150b = all_amps[i],all_amps[i+1],all_amps[i+2],all_amps[i+3]
                norm_90a,norm_90b,norm_150a,norm_150b = amp_90a-np.amin(amp_90a),amp_90b-np.amin(amp_90b),amp_150a-np.amin(amp_150a),amp_150b-np.amin(amp_150b)
                pJ_90a.append((etime-stime)*np.sum(norm_90a)*10**(12)/(400.))
                pJ_90b.append((etime-stime)*np.sum(norm_90b)*10**(12)/(400.))
                pJ_150a.append((etime-stime)*np.sum(norm_150a)*10**(12)/(400.))
                pJ_150b.append((etime-stime)*np.sum(norm_150b)*10**(12)/(400.))
                
            
            return np.sum(pJ_90a),np.sum(pJ_90b),np.sum(pJ_150a),np.sum(pJ_150b)

        self.get_store().set(self._output_key,energy_calculator)






class SaveEvents(Routine):
    """ A routine that saves all events data in a dictionary """
    def __init__(self,tag,cosig_key,tod_key,energy_key,output_key):
        Routine.__init__(self)
        self._tag = tag
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._energy_key = energy_key
        self._output_key = output_key 
        

        
    def execute(self):
        print '[INFO] Saving events data to dictionary...'
        
        energy_calculator = self.get_store().get(self._energy_key)
        tod_data = self.get_store().get(self._tod_key)
        cuts = self.get_store().get(self._cosig_key)
        peaks = cuts['peaks']
        cs = cuts['coincident_signals']
        
        #Initialize and fill empty dictionary
        events = []
        
        for peak in peaks:
            all_pixels = pixels_affected_in_event(cs, peak)
            start = peak[0]
            end = peak[1]
            duration = peak[2]
            number_of_pixels = peak[3]
            ref_index = int((start + end)/2)
            energy = []
            for pid in all_pixels:
                e1,e2,e3,e4 = energy_calculator(pid,start,end)
                energy_dict = {str(pid): [e1,e2,e3,e4]}
                energy.append(energy_dict)

            id = "%d.%d" % (self.get_id(), start)
            event = {
                'id': id,
                'start': start,
                'end': end,
                'duration': duration,
                'ctime': tod_data.ctime[ref_index],
                'alt': tod_data.alt[ref_index],
                'az': tod_data.az[ref_index],
                'number_of_pixels': float(number_of_pixels),
                'pixels_affected': all_pixels,
                'energy': energy,
            }
            events.append(event)
        
        self.get_store().set(self._output_key,events)


class EnergyStudy(Routine):
    """ A routine to plot a histogram of the energy per detector in a list of peaks in a TOD """

    def __init__(self,event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None

    def initialize(self):
        self._hist = Hist1D(0,50,50)

    def execute(self):
        print '[INFO] Adding data to plot histogram...'
        events = self.get_store().get(self._event_key)
        evals = []
        for event in events:
            energies = event['energy']
            for pixel in energies:
                evals.append(pixel.values())
        self._hist.fill(evals)

    def finalize(self):
        plt.step(*self._hist.data)
        hist_data = np.array(self._hist.data)
        #np.savetxt('0_150_tods_hist.txt',hist_data)
        
        
        slope, intercept = np.polyfit(self._hist.data[0],self._hist.data[1],1)
        y = slope*self._hist.data[0] + intercept
        plt.plot(self._hist.data[0],y,'--', label='Slope = ' + str(slope))
        

        plt.title('Energy per Detector')
        plt.ylabel('log(Events)')
        plt.xlabel('log(Energy pJ)')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.autoscale(enable=True)
        plt.show()


class NPixelStudy(Routine):
    def __init__(self,event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None
    
    def initialize(self):
        self._hist = Hist1D(1,50,48)

    def execute(self):
        print '[INFO] Adding data to plot histogram...'
        events = self.get_store().get(self._event_key)
        for event in events:
            self._hist.fill(event['number_of_pixels'])

    def finalize(self):
        plt.step(*self._hist.data)
        plt.title('Number of Pixels Affected')
        plt.xlabel('Number of Pixels')
        plt.show()


class CorrelationFilter(Routine):
    """ Does the same thing as the CorrelationFilter in correlation directory but returns list of cuts instead of dictionary """
    def __init__(self,timeseries_key,cosig_key,tod_key,output_key,coeff=0.8):
        Routine.__init__(self)
        self._timeseries_key = timeseries_key
        self._cosig_key = cosig_key
        self._tod_key = tod_key 
        self._pr = None
        self._template = None
        self._output_key = output_key 
        self._coeff = coeff 
        self._tag = None


    def initialize(self):
        self._pr = PixelReader()

    def execute(self):
        print '[INFO] Checking for correlation ...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data
        peaks = cuts['peaks']
        timeseries = self.get_store().get(self._timeseries_key)
        cs = cuts['coincident_signals']

        def avg_signal(pixels, start_time, end_time):

            for pid in pixels:
                x, y1, y2, y3, y4 = timeseries(pid,start_time,end_time)
                avg_y1, avg_y2, avg_y3, avg_y4  = np.zeros(len(y1)),np.zeros(len(y2)),np.zeros(len(y3)),np.zeros(len(y4))
                avg_x = x
                avg_y1 += y1
                avg_y2 += y2
                avg_y3 += y3
                avg_y4 += y4

            x = avg_x
            y1 = avg_y1/len(avg_y1)
            y2 = avg_y2/len(avg_y2)
            y3 = avg_y3/len(avg_y3)
            y4 = avg_y4/len(avg_y4)
            return x, y1,y2,y3,y4



        def correlation(x1,x2,y1,y2):

            ts1 = y1
            ts2 = y2 
            l1 = len(ts1)
            l2 = len(ts2)
            if l1 < l2:
                n = l1
                return max([np.corrcoef(ts1, ts2[i:n+i])[0][1] for i in range(0, l2-l1)])
            elif l2 < l1:
                n = l2
                return max([np.corrcoef(ts1[i:n+i], ts2)[0][1] for i in range(0, l1-l2)])
            else: 
                return np.corrcoef(ts1, ts2)[0][1]


        avg_x1, avg_y1 = self._template[0], self._template[1]

        possible_events = []
        highlylikely_events = []
        lower_threshold = 0.6
        upper_threshold = self._coeff
        
        for peak in peaks:
            all_pixels = pixels_affected_in_event(cs, peak)
            avg_x2, avg_y2_1,avg_y2_2,avg_y2_3,avg_y2_4 = avg_signal(all_pixels, peak[0], peak[1])
            coeff1 = correlation(avg_x1, avg_x2, avg_y1, avg_y2_1)
            coeff2 = correlation(avg_x1, avg_x2, avg_y1, avg_y2_2)
            coeff3 = correlation(avg_x1, avg_x2, avg_y1, avg_y2_3)
            coeff4 = correlation(avg_x1, avg_x2, avg_y1, avg_y2_4)

            if (lower_threshold <= coeff1)  & (lower_threshold <=  coeff2 ) & (lower_threshold <= coeff3)  & (lower_threshold <= coeff4) & (coeff1 < upper_threshold) & (coeff2 < upper_threshold) & (coeff3 < upper_threshold) & (coeff4 < upper_threshold):
                possible_events.append(peak)
        
            elif (coeff1 >= upper_threshold) & (coeff2 >= upper_threshold) & (coeff3 >= upper_threshold) & (coeff4 >= upper_threshold):
                highlylikely_events.append(peak)
        print highlylikely_events
        cuts['peaks'] = highlylikely_events

        self.get_store().set(self._output_key,cuts)


class CRCorrelationFilter(CorrelationFilter):
    """A routine that checks for correlation between two signals"""
    def __init__(self, timeseries_key,cosig_key, tod_key, output_key, coeff=0.8):
        CorrelationFilter.__init__(self, timeseries_key,cosig_key, tod_key, output_key,coeff)
        self._template = np.genfromtxt('cr_template.txt')
        self._tag = "CR"
