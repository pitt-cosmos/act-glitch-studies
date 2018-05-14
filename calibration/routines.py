from todloop.base import Routine
import numpy as np


class FixOpticalSign(Routine):
    """A routine that corrects for optical sign"""
    def __init__(self, input_key="tod_data", output_key="tod_data"):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key

    def execute(self):
        tod_data = self.get_store().get(self._input_key)  # retrieve TOD
        optical_signs = tod_data.info.array_data['optical_sign']
        tod_data.data = tod_data.data*optical_signs[:, np.newaxis]
        self.get_store().set(self._output_key, tod_data)



class CalibrateTOD(Routine):

    """A routine that calibrates from DAQ to W"""

    def __init__(self, input_key="tod_data", output_key="tod_data"):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key

    def execute(self):
        tod = self.get_store().get(self._input_key)
        cal = moby2.scripting.get_calibration({'type': 'iv', 'source': 'data'}, tod=tod)
        cal_mask, cal_val = cal.get_property('cal', det_uid=tod.det_uid)
        tod.data *= cal_val[:,None]
        self.get_store().set(self._output_key, tod)

