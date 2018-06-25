import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from todloop.base import Routine
from todloop.utils.pixels import PixelReader
from todloop.utils.cuts import pixels_affected_in_event

class CosigToEvent(Routine):
    def __init__(self, input_key="cosig", output_key="events"):
        """A routine that converts cuts to events"""
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key
        self._tag = "RAW"

    def initialize(self):
        """Scripts that run before processing the first TOD"""
        pass

    def execute(self):
        # Retrieve cut data
        cuts = self.get_store().get(self._input_key)
        cosig = cuts['coincident_signals']
        peaks = cuts['peaks']
        events = []
        for peak in peaks:
            event_id = "%d.%d" % (self.get_id(), peak[0])
            event = {
                'id': event_id,
                'start': peak[0],  # start index
                'end': peak[1],  # end index
                'duration': peak[2],
                'number_of_pixels': peak[3],
                'pixels_affected': pixels_affected_in_event(cosig, peak),
                'tag': self._tag
            }
            events.append(event)
        print '[INFO] Events generated: %d' % len(events)
        self.get_store().set(self._output_key, events)

    def finalize(self):
        """Scripts that run after processing all TODs"""
        pass
       

