import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from todloop.base import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event

class Filter(Routine):
    def __init__(self, input_key, output_key):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key

class DurationFilter(Filter):
    """An event filter based on the duration of events (set max duration)"""
    def __init__(self, min_duration=0,max_duration=10000, input_key='data', output_key='data'):
        Filter.__init__(self, input_key=input_key, output_key=output_key)
        self._min_duration = min_duration
        self._max_duration = max_duration

    def execute(self):
        cosig = self.get_context().get_store().get(self._input_key)
        peaks = cosig['peaks']
        print '[INFO] Before: n_tracks = %d' % len(cosig['peaks'])
        peaks_filtered = [peak for peak in peaks if self._min_duration < peak[2] <= self._max_duration]
        cosig['peaks'] = peaks_filtered
        print '[INFO] After: n_tracks = %d' % len(cosig['peaks'])
        self.get_context().get_store().set(self._output_key, cosig)

class PixelFilter(Filter):
    """An event filter based on the number of pixels affected (set max n_pixels)"""
    def __init__(self,min_pixels=0, max_pixels=5, input_key='data', output_key='data'):
        Filter.__init__(self, input_key, output_key)
        self._min_pixels = min_pixels
        self._max_pixels = max_pixels
        
    def execute(self):
        cosig = self.get_context().get_store().get(self._input_key)
        peaks = cosig['peaks']
        print '[INFO] Before: n_tracks = %d' % len(cosig['peaks'])
        peaks_filtered = [peak for peak in peaks if self._min_pixels < peak[3] <= self._max_pixels]
        cosig['peaks'] = peaks_filtered
        print '[INFO] After: n_tracks = %d' % len(cosig['peaks'])
        self.get_context().get_store().set(self._output_key, cosig)

class CorrelationFilter(Routine):
    """A base routine for correlation filter"""
    def __init__(self, cosig_key, tod_key, output_key, all_coeff_output_key,coeff=0.8):
        Routine.__init__(self)
        self._cosig_key = cosig_key
        self._tod_key = tod_key
        self._pr = None
        self._template = None
        self._output_key = output_key
        self._all_coeff_output_key = all_coeff_output_key
        self._coeff = coeff
        self._tag = None

    def initialize(self):
        self._pr = PixelReader()

    def execute(self):
        print '[INFO] Checking for correlation ...'
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data
        cuts = self.get_store().get(self._cosig_key)  # retrieve tod_data
        peaks = cuts['peaks']

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

            return time, d_1

        def avg_signal(pixels, start_time, end_time):

            for pid in pixels:

                # x = timeseries(pid,start_time,end_time)[0]
                # y = timeseries(pid,start_time,end_time)[1]
                x, y = timeseries(pid,start_time,end_time)

                avg_y = np.zeros(len(y))

                avg_x = x
                avg_y += y

            x = avg_x
            y = avg_y/len(avg_y)
            return x, y

        def correlation(x1,x2,y1,y2):
            """
            f1 = interp1d(x1,y1)
            f2 = interp1d(x2,y2)

            points = 100
            # points = 2*max(len(x1), len(x2))  # double precision

            x1new = np.linspace(min(x1), max(x1), points)
            x2new = np.linspace(min(x2), max(x2), points)

            y1new = f1(x1new)
            y2new = f2(x2new)
            """
            """
            NUMPY CORRELATION ROUTINE
            """
            #m_coeff = np.corrcoef(y1new,y2new)[0][1]
            """
            a = y1new
            b = y2new
            a = (a - np.mean(a)) / (np.std(a) * len(a))
            b = (b - np.mean(b)) / (np.std(b))
            c = np.correlate(a, b, 'full')
            m_coeff = np.max(abs(c))

            return m_coeff
            """

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
            else:  # l1 == l2
                return np.corrcoef(ts1[i:n+i], ts2)[0][1]


            
            """
            plt.subplot(211)
            plt.plot( x1new,y1new,'g--')
            plt.title('Two Signals to Check for Correlation')
            plt.subplot(212)
            plt.plot(x2new,y2new,'r--')
            plt.xlabel('Cor. Matrix Coeff: ' + str(m_coeff))
            plt.show()
            """

        """
        CHECK CORRELATION BETWEEN SIGNALS FROM TWO EVENTS
        Find avgerage signal from an peak, copy events from peaks data below
        To check correlation, call correlation function with peak data
        """

        cs = cuts['coincident_signals']

        """
        FOR TWO SPECIFIC EVENTS
        """
        """
        event1 = [101980, 101985, 5, 2]
        stime1 = event1[0]
        etime1 = event1[1]
        pixels1 = pixels_affected_in_event(cs, event1)
        avg_x1, avg_y1 = avg_signal(pixels1, stime1, etime1)
        np.savetxt('frb_template.txt',(avg_x1,avg_y1))
        
#        event2 = [205344, 205375, 31, 35]
        event2 = [9300,9303,3,2]
        stime2 = event2[0]
        etime2 = event2[1]
        pixels2 = pixels_affected_in_event(cs, event2)
        avg_x2, avg_y2 = avg_signal(pixels2, stime2, etime2)
        
        correlation(avg_x1,avg_x2, avg_y1, avg_y2)
        """


        """
        TEMPLATE FRB or CR  AS EVENT 1
        change name of .txt file to frb_template or cr_template 
        to check correlation for either signal 
        """
        avg_x1, avg_y1 = self._template[0], self._template[1]
        
        """
        ALL EVENTS
        To compare all events in track to template, 
        initiate this loop
        """

        # Save outputs to a dictionary, here we initialize an empty dictionary
        events = []
        all_coeffs = []
        lower_threshold = 0.6
        upper_threshold = self._coeff

        for peak in peaks:
            all_pixels = pixels_affected_in_event(cs, peak)
            avg_x2, avg_y2 = avg_signal(all_pixels, peak[0], peak[1])
            coeff = correlation(avg_x1, avg_x2, avg_y1, avg_y2)

            if lower_threshold <= coeff < upper_threshold:
                print '[INFO] Possible %s' % self._tag, peak, 'Coeff = ', coeff
                all_coeffs.append(coeff)
            elif coeff >= upper_threshold:
                print '[INFO] Highly Likely %s' % self._tag, peak, 'Coeff = ', coeff
                all_coeffs.append(coeff)
                start = peak[0]
                end = peak[1]
                duration = peak[2]
                number_of_pixels = peak[3]
                ref_index = int((start + end)/2)  # use as reference point
                id = "%d.%d" % (self.get_id(), start)
                event = {
                    'id': id,
                    'start': start,  # start index
                    'end': end,  # end index
                    'duration': duration,
                    'ctime': tod_data.ctime[ref_index],  # ref time
                    'alt': tod_data.alt[ref_index],  # ref alt
                    'az': tod_data.az[ref_index],  # ref az
                    'number_of_pixels': number_of_pixels,
                    'pixels_affected': all_pixels,
                    'coefficient': coeff,
                    'tag': self._tag
                }
                events.append(event)

        print '[INFO] Events passed: %d / %d' % (len(events), len(peaks))
        self.get_store().set(self._output_key, events)
        self.get_store().set(self._all_coeff_output_key,all_coeffs)
        

class CRCorrelationFilter(CorrelationFilter):
    """A routine that checks for correlation between two signals"""
    def __init__(self, cosig_key, tod_key, output_key, all_coeff_output_key, coeff=0.8):
        CorrelationFilter.__init__(self, cosig_key, tod_key, output_key, all_coeff_output_key,coeff)
        self._template = np.genfromtxt('cr_template.txt')
        self._tag = "CR"


class FRBCorrelationFilter(CorrelationFilter):
    """A routine that checks for correlation between two signals"""
    def __init__(self, cosig_key, tod_key, output_key, all_coeff_output_key, coeff=0.8):
        CorrelationFilter.__init__(self, cosig_key, tod_key, output_key, all_coeff_output_key, coeff)
        self._template = np.genfromtxt('frb_template.txt')
        self._tag = "FRB"


class SlowCorrelationFilter(CorrelationFilter):
    """A routine that checks for correlation between two signals"""
    def __init__(self, cosig_key, tod_key, output_key, all_coeff_output_key, coeff=0.8):
        CorrelationFilter.__init__(self, cosig_key, tod_key, output_key, all_coeff_output_key, coeff)
        self._template = np.genfromtxt('slow_template.txt')
        self._tag = "SLOW_DECAY"

class ScatterPlot(Routine):
    
    def __init__(self,frb_input_key, cr_input_key, slow_input_key):
        Routine.__init__(self)
        self._frb_input_key = frb_input_key
        self._cr_input_key = cr_input_key
        self._slow_input_key = slow_input_key
        self._frb_coeff = []
        self._cr_coeff = []
        self._slow_coeff = []

    def execute(self,num=10):
        print '[INFO] Plotting scatter plots...'
        
        frb_coeff = self.get_store().get(self._frb_input_key)
        frb_coeff = frb_coeff[:num]
        self._frb_coeff.append(frb_coeff)

        cr_coeff = self.get_store().get(self._cr_input_key)
        cr_coeff = cr_coeff[:num]        
        self._cr_coeff.append(cr_coeff)

        slow_coeff = self.get_store().get(self._slow_input_key)
        slow_coeff = slow_coeff[:num]
        self._slow_coeff.append(slow_coeff)


    def finalize(self):
        plt.scatter(self._frb_coeff, self._cr_coeff,alpha=0.7)
        plt.xlabel('FRB Coefficients')
        plt.ylabel('CR Coefficients')
        plt.title('FRB vs. CR Coefficients')
        plt.show()

        plt.scatter(self._frb_coeff, self._slow_coeff, alpha = 0.7)
        plt.xlabel('FRB Coefficients')
        plt.ylabel('Slow Coefficients')
        plt.title('FRB vs Slow Correlation Coeff')
        plt.show()

        plt.scatter(self._slow_coeff, self._cr_coeff, alpha = 0.7)
        plt.xlabel('Slow Coefficients')
        plt.ylabel('CR Coefficients')
        plt.title('Slow Decay vs CR Correlation Coeff')
        plt.show()
