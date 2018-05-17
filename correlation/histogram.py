import matplotlib
matplotlib.use("TKAgg")
import numpy as np
import matplotlib.pyplot as plt
from todloop.routines import Routine

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
