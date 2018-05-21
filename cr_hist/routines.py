from todloop.base import Routine
import matplotlib
from todloop.utils.hist import Hist1D
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
from todloop.utils.pixels import PixelReader


class NPixelStudy(Routine):
    def __init__(self, event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None

    def initialize(self):
        self._hist = Hist1D(1, 50, 48)

    def execute(self):
        events = self.get_store().get(self._event_key)
        for event in events:
            self._hist.fill(event['number_of_pixels'])

    def finalize(self):
        plt.step(*self._hist.data)
        plt.show()


class CRHourStudy(Routine):
    """A study of glitches vs hour"""
    def __init__(self, tod_info_key="tod_info", event_key="events"):
        Routine.__init__(self)
        self._glitches_hour_hist = None
        self._tods_hour_hist = None
        self._tod_info_key = tod_info_key
        self._event_key = event_key

    def initialize(self):
        self._glitches_hour_hist = Hist1D(0, 24, 23)
        self._tods_hour_hist = Hist1D(0, 24, 23)
        
    def execute(self):
        # get tod info and coincident signals
        tod_info = self.get_store().get(self._tod_info_key)
        events = self.get_store().get(self._event_key)

        # get the total number of glitches
        n_glitches = len(events)

        self._glitches_hour_hist.fill(float(tod_info['hour']), n_glitches)
        self._tods_hour_hist.fill(float(tod_info['hour']))

    def finalize(self):
        print '[INFO] Glitch vs Hour: ', self._glitches_hour_hist
        print '[INFO] TOD vs Hour: ', self._tods_hour_hist
        plt.subplot(131)
        plt.step(*self._glitches_hour_hist.data)
        plt.subplot(132)
        plt.step(*self._tods_hour_hist.data)
        plt.subplot(133)
        plt.step(self._glitches_hour_hist.data[0], self._glitches_hour_hist.data[1]/self._tods_hour_hist.data[1])
        plt.tight_layout()
        plt.show()


class CRPWVStudy(Routine):
    """A study of glitches vs PWV"""
    def __init__(self, tod_info_key="tod_info", event_key="events"):
        Routine.__init__(self)
        self._glitches_hour_hist = None
        self._tods_hour_hist = None
        self._tod_info_key = tod_info_key
        self._event_key = event_key

    def initialize(self):
        self._glitches_pwv_hist = Hist1D(0, 7, 6)
        self._tods_pwv_hist = Hist1D(0, 7, 6)
        
    def execute(self):
        # get tod info and coincident signals
        tod_info = self.get_store().get(self._tod_info_key)
        events = self.get_store().get(self._event_key)

        # get the total number of glitches
        n_glitches = len(events)

        if tod_info['PWV']=='-':
            self.veto()
        else:
            self._glitches_pwv_hist.fill(float(tod_info['PWV']), n_glitches)
            self._tods_pwv_hist.fill(float(tod_info['PWV']))

    def finalize(self):
        plt.subplot(131)
        plt.step(*self._glitches_pwv_hist.data)
        plt.subplot(132)
        plt.step(*self._tods_pwv_hist.data)
        plt.subplot(133)
        plt.step(self._glitches_pwv_hist.data[0], self._glitches_pwv_hist.data[1]/self._tods_pwv_hist.data[1])
        plt.tight_layout()
        plt.show()


class RaDecStudy(Routine):
    def __init__(self, input_key):
        """Scripts that run during initialization of the routine"""
        Routine.__init__(self)
        self._input_key = input_key
        self._ras = []
        self._decs = []

    def execute(self):
        """Scripts that run for each TOD"""
        events = self.get_store().get(self._input_key)
        for event in events:
            self._ras.append(event['ra'])
            self._decs.append(event['dec'])
        

    def finalize(self):
        """Scripts that run after processing all TODs"""
        plt.scatter(self._ras, self._decs, alpha=0.2)
        plt.xlabel("RA")
        plt.ylabel("DEC")
        plt.show()

        
class SpatialStudy(Routine):
    def __init__(self, input_key):
        """Study the spatial histogram for events"""
        Routine.__init__(self)
        self._input_key = input_key
        self._rows = []
        self._cols = []

    def initialize(self):
        self._pr = PixelReader()

    def execute(self):
        """Scripts that run for each TOD"""
        events = self.get_store().get(self._input_key)  # get events
        for event in events:
            # find the pixels affected
            pixels_affected = event['pixels_affected']
            rows, cols = self._pr.get_row_col(pixels_affected)

            # store row / col 
            self._rows.extend(rows)  
            self._cols.extend(cols)


    def finalize(self):
        """Scripts that run after processing all TODs"""
        all_rows, all_cols = self._pr.get_row_col_array()
        # plt.plot(all_rows, all_cols, 'r.')  # plot all rows as background
        plt.plot(self._rows, self._cols, 'b.', alpha=0.1)  # plot affected row / col
        plt.xlabel("Row")
        plt.ylabel("Col")
        plt.show()
