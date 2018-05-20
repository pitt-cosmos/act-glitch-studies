import matplotlib
matplotlib.use("TKAgg")
import numpy as np
import matplotlib.pyplot as plt
from todloop.routines import Routine
from todloop.utils.pixels import PixelReader
import moby2
# import moby2.scripting.products as products



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
        def plotter(pixels,start_time,end_time):
                        
            for pid in pixels:
               
                x = timeseries(pid,start_time,end_time)[0]
                y = timeseries(pid,start_time,end_time)[1]

                plt.title('Pixels affected from ' +str(start_time)+ '-' + str(end_time)+ ' at 90 GHz')
                plt.xlabel('TOD_ID: %d    TOD_NAME: %s' % (self.get_id(), self.get_name()))  # CHANGE TOD TRACK NAME
                plt.plot(x,y,'.-')
            
            plt.show()

            
        """
        ALL EVENTS
        Plot all pixels affected in a event one by one for all events
        """
        
        for event in events:
            pixels_affected = event['pixels_affected']
            start_time = event['start']
            end_time = event['end']
            print '[INFO] Number of pixels affected: %d' % event['number_of_pixels']
            plotter(pixels_affected, start_time, end_time)



class NPixelFilter(Routine):
    def __init__(self, min_pixels=0, max_pixels=100, input_key="events", output_key="events"):
        """Scripts that run during initialization of the routine"""
        Routine.__init__(self)
        self._min_pixels = min_pixels
        self._max_pixels = max_pixels
        self._input_key = input_key
        self._output_key = output_key

    def execute(self):
        """Scripts that run for each TOD"""
        events = self.get_store().get(self._input_key)
        events_filtered = [event for event in events if self._min_pixels <= event['number_of_pixels'] < self._max_pixels]
        
        # if no events left, skip TOD
        if len(events_filtered) == 0:
            self.veto()  # skip subsequent routines
            return
        else:
            print '[INFO] Events passed %d / %d' % (len(events_filtered), len(events))
            self.get_store().set(self._output_key, events_filtered)

            
class CoeffFilter(Routine):
    def __init__(self, min_coeff=0.8, max_coeff=1, input_key="events", output_key="events"):
        """Filter events based on coefficient"""
        Routine.__init__(self)
        self._min_coeff = min_coeff
        self._max_coeff = max_coeff
        self._input_key = input_key
        self._output_key = output_key

    def execute(self):
        """Scripts that run for each TOD"""
        events = self.get_store().get(self._input_key)
        events_filtered = [event for event in events if self._min_coeff <= event['coefficient'] < self._max_coeff]
        
        # if no events left, skip TOD
        if len(events_filtered) == 0:
            self.veto()  # skip subsequent routines
            return
        else:
            print '[INFO] Events passed: %d / %d' % (len(events_filtered), len(events))
            self.get_store().set(self._output_key, events_filtered)
        

            
class LoadRaDec(Routine):
    """A routine that loads the information about RA and DEC for each events"""
    def __init__(self, event_key="events", tod_key="tod_data", output_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._tod_key = tod_key
        self._output_key = output_key

    def initialize(self):
        """Scripts that run before processing the first TOD"""
        user_config = moby2.util.get_user_config()
        moby2.pointing.set_bulletin_A(params=user_config.get('bulletin_A_settings'))

    def execute(self):
        """Scripts that run for each TOD"""
        events = self.get_store().get(self._event_key)
        tod_data = self.get_store().get(self._tod_key)  # retrieve tod_data

        # get focal plane (removed as no need such precision now)
        # fp_file = "/mnt/act3/users/mhasse/depots/shared/RelativeOffsets/template_ar3_s16_170131.txt"  # TODO: Adapt to more seasons
        # focal_plane = products.get_focal_plane({'source': 'fp_file', \
        #                                         'filename': fp_file}, 
        #                                        tod_data.info)
        
        new_events = []
        for event in events:  # loop over each event
            # start = event['start']
            # end = event['end']
            # ra, dec = moby2.pointing.get_coords(tod_data.ctime[start:end], tod_data.az[start:end], tod_data.alt[start:end], focal_plane=focal_plane)
            # ra, dec = moby2.pointing.get_coords(tod_data.ctime[start:end], tod_data.az[start:end], tod_data.alt[start:end])
            ra, dec = moby2.pointing.get_coords([event['ctime']], [event['az']], [event['alt']])
            # ref_index = int(len(ra)/2)  # use the middle index as a reference
            event['ra'] = ra[0]  # ra / dec is a vector with one element
            event['dec'] = dec[0]
            new_events.append(event)
        self.get_store().set(self._output_key, new_events)
