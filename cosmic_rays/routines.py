import matplotlib
matplotlib.use("TKAgg")
import json
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from  todloop import Routine
#from todloop.routines import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event
from todloop.utils.hist import Hist1D 
import moby2
from moby2.instruments import actpol
from moby2.scripting import get_filebase
from moby2.detectors.stuff import TimeConstants

"""
#######################
ROUTINES IN THIS FILE #
#######################

1. Filter - Routine
   Can be applied to make new filters

2. Timeseries - Routine
   Returns function of timeseries

3. PlotGlitches - Routine
   User input event gets plotted, for every pixel affected
   then the location of pixels affected on detector plane is plotted

4. Energy - Routine
   Returns the total energy of a pixel (four detectors) 
   This info can be saved in events dictionary

5. SaveEvents - Routine
   Takes initial cuts data and generates a dictionary 
   with various well defined parameters

6. EnergyStudy - Routine
   Generates histogram data about the energy associated with an event
   Saves data to a text file

7. NPixelStudy - Routine
   Generates histogram data about the number of pixels affected in an event 
   Saves data to a text file

8. CorrelationFilter - Routine
   Routine that takes timeseries and compares it to a template and returns a 
   coffecient of correlation. If coeff > 0.8, it gets passed further down pipeline
 
  a.CRCorrelationFilter - Instance of CorrelationFilter
    Applies cosmic ray template to correlation filter routine
 
  b.FRBCorrelationFilter - Instance of CorrelationFilter
    Applies FRB template to correlation filter routine

9. Duration Filter - Filter
   Filters out cuts based on how many timesamples the glitch spans
   WIP not well incorporated in timeline yet!!

10. Pixel Filter - Filter
    Filters out events that affect more than a specified number of pixels

11. EdgeFilter - Filter
   Filters out events that take place on the edge of the detector plane
   WIP not well incorporated in timeline yet!!

12. RADecStudy - Routine
   Filters out events that take place outside of a specified RA and Dec range

13. Deconvolution - Routine
    Deconvolves the effects of the detector time constant

14. TimeConstant - Routine
    Generates a dictionary of time constants and corresponding detector uids for a TOD

15. PlotDetectorGlitches - Routine
    Provide a Detector UID to plot all of the events that take place on that detector, 
    *also includes the time constant associated with the detector

"""



class Filter(Routine):
    def __init__(self, input_key, output_key):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key


class TimeSeries(Routine):
    """ A routine that returns a function to find the timeseries of a pixel in 4 frequencies """
    def __init__(self,tod_key,output_key):
        Routine.__init__(self)
        self._tod_key = tod_key
        self._pr = None
        self._output_key = output_key
    
    """
    def initialize(self):
        self._pr = PixelReader()
    """
    
    def execute(self,store):

        #array_name = self.get_array()
        #self._pr = PixelReader(season = '2017', array=str(array_name)) #use this for covered TODs
        self._pr = PixelReader() #use this for uncovered TODs
        print '[INFO] Getting timeseries...'
        tod_data = store.get(self._tod_key)  # retrieve tod_data                                                                                                     

    
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

        store.set(self._output_key,timeseries)

class PlotGlitches(Routine):
    """A routine that plots glitches """
    def __init__(self, tag, cosig_key, tod_key,timeseries_key):
        Routine.__init__(self)
        self._tag = tag
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._timeseries_key = timeseries_key
        self._pr = None
    
    
    """
    def initialize(self):
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data                                                                        
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data                                                                          
    """


    def execute(self,store):
        print '[INFO] Loading Glitch Data ...'
        tod_data = store.get(self._tod_key)  # retrieve tod_data                                                    
        cuts = store.get(self._cosig_key)  # retrieve tod_data                                                    
        array_name = self.get_array()
        peaks = cuts['peaks']
        #print('[INFO] All glitches, unfiltered...')
        #print('[INFO] peaks: ', peaks)
        #self._pr = PixelReader(season= '2017', array=self.get_context().get_array()) #for covered
        self._pr = PixelReader() #for uncovered
        #self._pr = PixelReader(season='2017',array = str(array_name))        
        #self._pr = PixelReader(season='2017', array=self.get_context().get_array())
      
        plot = raw_input("Do you want to plot an event? Enter y/n: ")
        if plot == "y":
            tod_data = store.get(self._tod_key)  # retrieve tod_data     
            cuts = store.get(self._cosig_key)  # retrieve tod_data
            peaks = cuts['peaks']
          
          
        
            def cs_cuts():
                cuts = store.get(self._cosig_key) 
                return cuts['coincident_signals']
            
        
            timeseries = store.get(self._timeseries_key)
            

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


    def execute(self,store):
        print '[INFO] Running energy analysis...'
        timeseries = store.get(self._timeseries_key)
    
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
                
            """Returns the total energy of the pixel (sum of 4 detectors)"""
            return np.sum(pJ_90a) + np.sum(pJ_90b) + np.sum(pJ_150a) + np.sum(pJ_150b)

        store.set(self._output_key,energy_calculator)






class SaveEvents(Routine):
    """ A routine that saves all events data in a dictionary """
    def __init__(self,tag,cosig_key,tod_key,energy_key,output_key):
        Routine.__init__(self)
        self._tag = tag
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._energy_key = energy_key
        self._output_key = output_key

        

        
    def execute(self,store):
        print '[INFO] Saving events data to dictionary...'
        
        energy_calculator = store.get(self._energy_key)
        tod_data = store.get(self._tod_key)
        cuts = store.get(self._cosig_key)
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
            energy_per_detector = []
            for pid in all_pixels:
                pix_energy = energy_calculator(pid,start,end)
                energy_per_detector.append(pix_energy)
            energy = np.sum(energy_per_detector)
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
        
        store.set(self._output_key,events)


class EnergyStudy(Routine):
    """ A routine to plot a histogram of the energy per detector in a list of peaks in a TOD """

    def __init__(self,event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None

    def initialize(self):
        self._hist = Hist1D(0,50,50)

    def execute(self,store):
        print '[INFO] Adding data to plot histogram...'
        events = store.get(self._event_key)
        for event in events:
            self._hist.fill(event['energy'])

    def finalize(self):
        #plt.step(*self._hist.data)
        hist_data = np.array(self._hist.data)
        ###CHANGE NAME OF TEXT FILE OR IT WILL OVERWRITE
        #np.savetxt('icecube_crf.txt',hist_data)

        
        """
        slope, intercept = np.polyfit(self._hist.data[0],self._hist.data[1],1)
        y = slope*self._hist.data[0] + intercept
        plt.plot(self._hist.data[0],y,'--', label='Slope = ' + str(slope))
        """
        """
        plt.title('Energy per Event')
        plt.ylabel('log(Events)')
        plt.xlabel('log(Energy pJ)')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.autoscale(enable=True)
        plt.show()
        """

class NPixelStudy(Routine):
    def __init__(self,event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None
    
    def initialize(self):
        self._hist = Hist1D(1,200,50)

    def execute(self,store):
        print '[INFO] Adding data to plot histogram...'
        events = store.get(self._event_key)
        for event in events:
            self._hist.fill(event['number_of_pixels'])

    def finalize(self):
        """
        plt.step(*self._hist.data)
        plt.title('Number of Pixels Affected')
        plt.xlabel('Number of Pixels')
        plt.show()
        """
        pixel_data = np.array(self._hist.data)
        np.savetxt('Unf_uncov_pix.txt',pixel_data)

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

    """
    def initialize(self):
        self._pr = PixelReader()
    """

    def execute(self,store):
        print '[INFO] Checking for correlation ...'
        self._pr = PixelReader()
        #self._pr = PixelReader(season = '2017', array=self.get_context().get_array())
        tod_data = store.get(self._tod_key)  # retrieve tod_data
        cuts = store.get(self._cosig_key)  # retrieve tod_data
        peaks = cuts['peaks']
        timeseries = store.get(self._timeseries_key)
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
        print '[INFO] Events passed: %d / %d' % (len(highlylikely_events), len(peaks))
        cuts['peaks'] = highlylikely_events
        store.set(self._output_key,cuts)


class CRCorrelationFilter(CorrelationFilter):
    """A routine that checks for correlation between two signals"""
    def __init__(self, timeseries_key,cosig_key, tod_key, output_key, coeff=0.8):
        CorrelationFilter.__init__(self, timeseries_key,cosig_key, tod_key, output_key,coeff)
        self._template = np.genfromtxt('cr_template.txt')
        self._tag = "CR"


class FRBCorrelationFilter(CorrelationFilter):
    """A routine that checks for correlation between two signals"""
    def __init__(self, timeseries_key,cosig_key, tod_key, output_key, coeff=0.9):
        CorrelationFilter.__init__(self, timeseries_key,cosig_key, tod_key, output_key,coeff=0.9)
        #self._template = np.genfromtxt('frb_nobuff_template.txt')                                                                                                               
        #self._template = np.genfromtxt('frb_template.txt')                                                                                                                      
        self._template = np.genfromtxt('act_frb180110.txt')
        self._tag = "FRB"


class DurationFilter(Filter):
    """An event filter based on the duration of events (set max duration)"""
    def __init__(self, min_duration=0,max_duration=10000, input_key='data', output_key='data'):
        Filter.__init__(self, input_key=input_key, output_key=output_key)
        self._min_duration = min_duration
        self._max_duration = max_duration

    def execute(self,store):
        cosig = store.get(self._input_key)
        peaks = cosig['peaks']
        print '[INFO] Before: n_tracks = %d' % len(cosig['peaks'])
        peaks_filtered = [peak for peak in peaks if self._min_duration < peak[2] <= self._max_duration]
        #dur_cuts = {'peaks': peaks_filtered,'coincident_signal':}
        dur_cuts = cosig.copy()
        dur_cuts['peaks'] = peaks_filtered
        print '[INFO] After: n_tracks = %d' % len(dur_cuts['peaks'])
        store.set(self._output_key, dur_cuts)



class PixelFilter(Filter):
    """An event filter based on the number of pixels affected (set max n_pixels)"""
    def __init__(self,min_pixels=0, max_pixels=3, input_key='data', output_key='data'):
        Filter.__init__(self, input_key, output_key)
        self._min_pixels = min_pixels
        self._max_pixels = max_pixels
        
    def execute(self,store):
        cosig = store.get(self._input_key)
        peaks = cosig['peaks']
        print '[INFO] Before: n_tracks = %d' % len(cosig['peaks'])
        peaks_filtered = [peak for peak in peaks if self._min_pixels < peak[3] <= self._max_pixels]
        pix_cuts = cosig.copy()
        pix_cuts['peaks'] = peaks_filtered
        print '[INFO] After: n_tracks = %d' % len(pix_cuts['peaks'])
        store.set(self._output_key, pix_cuts)


class EdgeFilter(Filter):
    """
    A filter that will go through Highly Likely Events and only return those
    that are not located at the edge of the detector plane.
    """
    
    def __init__(self,input_key = 'data', output_key='data'):
        Filter.__init__(self, input_key, output_key)
    
    def execute(self,store):

        print '[INFO] Filtering out edge pixels...'
        high_events = store.get(self._input_key)

        #Pixel IDs of edge pixels
        edge_pids = [152,664,25,409,665,793,921,26,794,922,592,337,210,147,84,852,725,470,343,283,155,667,28,412,668,796,924,576,321,194,131,68,836,709,454,327,285,157,669,30,414,670,798,926,31,799,927,588,333,206,143,72,840,713,458,714,280]
        #Initialize empty list to hold all events that take do not take place on edge of detector 
        cen_events = []
        
        for event in high_events:
            pids = event['pixels_affected']
            for pid in pids:
                if pid in edge_pids:
                    pass
                else:
                    cen_events.append(event)
        print '[INFO] Events passed: %d /%d' % (len(cen_events),len(high_events))
        
        store.set(self._output_key,cen_events)




class RaDecStudy(Routine):
    def __init__(self, output_key,input_key, ra_range=None, dec_range=None):
        """Scripts that run during initialization of the routine"""
        Routine.__init__(self)
        self._input_key = input_key
        self._ra_range = ra_range
        self._dec_range = dec_range
        self._output_key = output_key 

    def execute(self,store):
        """Scripts that run for each TOD"""
        cuts= store.get(self._input_key)
            
        filtered_events = []

        
        for event in events:
            select = True
            if self._ra_range and self._dec_range:  # select a range of RA / DEC if given
                ra_lower = self._ra_range[0]
                ra_upper = self._ra_range[1]
                dec_lower = self._dec_range[0]
                dec_upper = self._dec_range[1]

                if event['ra'] < ra_lower or event['ra'] > ra_upper or \
                   event['dec'] < dec_lower or event['dec'] > dec_upper :
                    select = False
            if select:
                self._filtered_events.append(event)

        store.set(self._output_key,filtered_events)

    def finalize(self):
        print '[INFO] Total events passed: %d / %d' % (len(filtered_events), len(events))


class Deconvolution(Routine):
    def __init__(self,input_key="tod_data", output_key="tod_data",abspath=False):
        Routine.__init__(self)
        self._fb = None
        self._abspath = abspath
        self._input_key = input_key
        self._output_key = output_key
    
    def initialize(self):
        self._fb = get_filebase()

    def execute(self,store):
        data = store.get("tod_data")
        tod_name = self.get_name()
        
        def tconst_filter(freq,tau):
            """
            Return the fourier space representation of the effect of 
            detector time constants, for the given frequencies
            """
            return 1/(2*np.pi*1j*freq*tau+1)
 
        tod_string = str(tod_name)
        tc = TimeConstants.read_from_path('/mnt/act3/users/spho/2016/TimeCo\
nstantsperTOD_170718/pa3/' + tod_string[:5] + '/' + tod_string + '.tau')
        moby2.tod.detrend_tod(data)
        print '[INFO] Deconvoluting data... '
        for i in range(998):#1015
            d_tod = data.data[i]
            ftod = np.fft.rfft(d_tod)
            nsamp = len(d_tod)
            srate = 400 #Hz
            freqs = np.arange(nsamp//2 + 1) * srate/nsamp
            tau = tc.get_property('tau')[1][i]
            resp = tconst_filter(freqs,tau)
            ftod /= resp
            deconv_tod = np.fft.irfft(ftod)
            data.data[i] = deconv_tod
        
        store.set(self._output_key,data)


class Convolution(Routine):
    """
    Provide this routine with a .txt file with time on the first axis and signal on the second axis, and with a time constant (tau) and it will convolve the signal to show how different detector response times affect the profile of the signal 
    """
    
    def __init__(self,data='frb180110.txt', tau=0.2):
        Routine.__init__(self)
        self._data = data
        self._tau = tau


    def execute(self,store):
        data = np.genfromtxt(self._data)
        raw_x = data[0]
        raw_y = data[1]

        def tconst_filter(freq,tau):
            """
            Return the fourier space representation of the effect of 
            detector time constants, for the given frequencies
            """
            return 1/(2*np.pi*1j*freq*tau+1)

        print '[INFO] Convoluting Data...'

        f_y = np.fft.rfft(raw_y)
        nsamp = len(raw_y)
        srate = 400 #Hz, adjust based on the parameters of the signal you are trying to convolve
        freqs = np.arange(nsamp//2 + 1) * srate/nsamp
        resp = tconst_filter(freqs,self._tau)
        f_y *= resp
        conv_data = np.fft.irfft(f_y)

        """
        Return Output as Plot
        """
        plt.subplot(211)
        plt.plot(raw_x,raw_y,'.-',color='teal')
        plt.title('Raw')

        plt.subplot(212)
        plt.plot(raw_x[:len(conv_data)],conv_data,'.-',color='darkslateblue')
        plt.title('Convolved')
        plt.xlabel('Tau =' + str(self._tau))
        plt.show()
    

class TimeConstant(Routine):
    """ Returns dictionary that maps pixel ids to corresponding time constants"""

    def __init__(self,input_key='tod_data',output_key='time_constants',abspath=False):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key
        self._abspath = abspath
        
    def initialize(self):
        self._fb = get_filebase()

    def execute(self,store):
        data = store.get("tod_data")
        tod_name = self.get_name()
        tod_string = str(tod_name)
        tc = TimeConstants.read_from_path('/mnt/act3/users/spho/2016/TimeConstantsperTOD_170718/pa3/' + tod_string[:5] + '/' + tod_string + '.tau')
        time_constants = []
        for i in range(998):#1015  
            tau = tc.get_property('tau')[1][i]
            pid = tc.get_property('det_uid')[1][i]
            tcs = {
                str(pid): tau, #key is det_uid, and value is time constant 
                'tau': tau,
                'det_uid':pid,
                }
            time_constants.append(tcs)
            #print('Tau = ', tau)
            #print('Det UID =', pid)
        
        
        store.set(self._output_key,time_constants)

#class TauStudy(Routine):
    """ Study which detectors are slow and which are fast for a given TOD"""



class NEventsStudy(Routine):
    def __init__(self,allevents_key="peaks",event_key="frb_cuts"):
        Routine.__init__(self)
        self._allevents_key = allevents_key
        self._event_key = event_key
        self._hist1 = None
        #self._hist2 = None

    def initialize(self):
        self._hist1 = Hist1D(1,100,50)
        #self._hist2 = Hist1D(1,100,50)

    def execute(self,store):
        print '[INFO] Adding data to plot histogram...'
        events = store.get(self._event_key)
        allevents = store.get(self._allevents_key)
        percent = len(events)/len(allevents)

        self._hist1.fill(percent*100)
        #self._hist2.fill(len(allevents))

    def finalize(self):
        #"""                                                                                                                                                                       
        plt.step(*self._hist1.data)
        #plt.step(*self._hist2.data,label='All Events')
        plt.title('Percentage of FRB events per TOD')                                                                                                                                    
        plt.xlabel('Percentage of Events')                                                                                                                                            
        plt.show()                                                                                                                                                                
        #"""
        """
        pixel_data = np.array(self._hist.data)
        np.savetxt('Unf_uncov_pix.txt',pixel_data)
        """


class PlotDetectorGlitches(Routine):
    def __init__(self,detuid,tag,cosig_key,tod_key,timeseries_key,time_constants):
        Routine.__init__(self)
        self._detuid = detuid
        self._tag = tag
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._timeseries_key = timeseries_key
        self._time_constants = time_constants
        self._pr = None


    def execute(self,store):
        print '[INFO] Plotting all glitches affecting detector ...'
        taus = store.get(self._time_constants)
        for tc in taus:
            if tc['det_uid'] == self._detuid:
                tau = tc['tau']
        
        tod_data = store.get(self._tod_key)  # retrieve tod_data                       
        cuts = store.get(self._cosig_key)  # retrieve tod_data           
        array_name = self.get_array()
        peaks = cuts['peaks']
        self._pr = PixelReader()

        def cs_cuts():
            cuts = store.get(self._cosig_key)
            return cuts['coincident_signals']

        timeseries = store.get(self._timeseries_key)

        def plotter(pid,tau,start_time,end_time):
                
            x = timeseries(pid,start_time,end_time)[0]
            y1 = timeseries(pid,start_time,end_time)[1]
            y2 = timeseries(pid,start_time,end_time)[2]
            y3 = timeseries(pid,start_time,end_time)[3]
            y4 = timeseries(pid,start_time,end_time)[4]


            plt.title('Pixel affected from ' +str(start_time)+ '-' + str(end_time)+
', Pixel ' + str(pid))
            plt.xlabel('TOD track:' + str(self._tag) + ' Tau:' + str(tau))
            plt.plot(x,y1,'.-',label='90 GHz')
            plt.plot(x,y2,'.-',label='90 GHz')
            plt.plot(x,y3,'.-',label='150 GHz')
            plt.plot(x,y4,'.-',label='150 GHz')
            
            plt.legend()
            plt.show()
        


        cs = cuts['coincident_signals']
        
        for peak in peaks:

            stime = peak[0]
            etime = peak[1]
            pixels = pixels_affected_in_event(cs,peak)
            for pixel in pixels:
                if pixel == self._detuid:
                    plotter(pixel,tau,stime,etime)
                
                

