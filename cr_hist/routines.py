from todloop.base import Routine
import matplotlib
from todloop.utils.hist import Hist1D
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt


class NPixelHist(Routine):
    def __init__(self, event_key="events"):
        Routine.__init__(self)
        self._event_key = event_key
        self._hist = None

    def initialize(self):
        self._hist = Hist1D(0, 200, 50)

    def execute(self):
        events = self.get_store().get(self._event_key)
        if not events:  # sometimes there is no events
            return  # do nothing
        for event in events:
            self._hist.fill(event['pixels_affected'])

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
        if not events:
            print '[WARNING] Events empty'
            return
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
        if not events:
            return

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


class GlitchAzStudy(Routine):
    """A study of glitches vs AZ"""
    def __init__(self):
        Routine.__init__(self)
        self._glitches_hist = None
        self._tods_hist = None

    def initialize(self):
        self._glitches_hist = Hist1D(0, 360, 360)
        self._tods_hist = Hist1D(0, 360, 360)
        
    def execute(self):
        # get tod info and coincident signals
        tod_info = self.get_store().get("tod_info")
        cosig = self.get_store().get("cosig")

        # get the total number of glitches
        n_glitches = len(cosig['peaks'])

        self._glitches_hist.fill(float(tod_info['azimuth']), n_glitches)
        self._tods_hist.fill(float(tod_info['azimuth']))

    def finalize(self):
        plt.subplot(131)
        plt.step(*self._glitches_hist.data)
        plt.subplot(132)
        plt.step(*self._tods_hist.data)
        plt.subplot(133)
        plt.step(self._glitches_hist.data[0], self._glitches_hist.data[1]/self._tods_hist.data[1])
        plt.tight_layout()
        plt.show()

