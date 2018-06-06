import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy as np
import moby2
from todloop.base import Routine, TODLoop
from moby2.instruments import actpol
from moby2.scripting import get_filebase
from moby2.detectors.stuff import TimeConstants

class Deconvolution(Routine):
    def __init__(self,tod_key,output_key):
        Routine.__init__(self)
        TODLoop.__init__(self)
        self._tod_key = tod_key 
        self._output_key = output_key
        
    def execute(self):
        
        def tconst_filter(freq,tau):
            """
            Return the fourier space representation of the effect of 
            detector time constants, for the given frequencies
            """
            return 1/(2*np.pi*1j*freq*tau+1)
        tod_name = self.get_name()
        tod_string = str(tod_name)
        data = self.get_store().get(self._tod_key)
        tc = TimeConstants.read_from_path('/mnt/act3/users/spho/2016/TimeCo\
nstantsperTOD_170718/pa2/' + tod_string[:5] + '/' + tod_string + '.tau')####array2/3
        tod = moby2.tod.detrend_tod(data)####

        for i in range(1015):
            d_tod = data.data[i] ####
            ftod = np.fft.rfft(d_tod)
            nsamp = len(d_tod)
            srate = 400 #Hz
            freqs = np.arange(nsamp//2 + 1) * srate/nsamp
            tau = tc.get_property('tau')[1][i]
            resp = tconst_filter(freqs,tau)
            ftod /= resp
            deconv_tod = np.fft.irfft(ftod)
            deconv_data = {
                'tod' = tod_name,
                'id' = i,
                'data' = deconv_tod
                }
            deconv_time.append(deconv_data)
        
        self.get_store().set(self._output_key,deconv_time)
