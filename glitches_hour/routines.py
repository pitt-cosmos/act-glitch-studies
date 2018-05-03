from eventloop.base import Routine
import numpy as np


class GlitchHourStudy(Routine):
    """A study of glitches vs hour"""
    def __init__(self):
        Routine.__init__(self)
        self._hour_dict = {}

    def execute(self):
        # get tod info and coincident signals
        tod_info = self.get_store().get("tod_info")
        cosig = self.get_store().get("cosig")

        # get the total number of glitches
        n_glitches = len(cosig['peaks'])
        hour = np.floor(tod_info['hour'])

        if str(hour) not in self._hour_dict:  # if first
            self._hour_dict[str(hour)] = n_glitches

        else:  # not first
            self._hour_dict[str(hour)] += n_glitches

    def finalize(self):
        print '[INFO] Glitch vs Hour: ', self._hour_dict

