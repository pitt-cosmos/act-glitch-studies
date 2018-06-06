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
    def __init__(self,output_key="tod_data",abspath=False):
        Routine.__init__(self)
        self._fb = None
        self._abspath = abspath
        self._output_key = output_key
    
    def initialize(self):
        self._fb = get_filebase()

    def execute(self):

        if self._abspath:  # if absolute path is given
            tod_filename = self.get_name()
        else:
            tod_name = self.get_name()
            tod_filename = self._fb.filename_from_name(tod_name, single=True)  # get file path
        print '[INFO] Loading TOD: %s ...' % tod_filename
        data = moby2.scripting.get_tod({'filename': tod_filename, 'repair_pointing': True})
        print '[INFO] TOD loaded'

        
        def tconst_filter(freq,tau):
            """
            Return the fourier space representation of the effect of 
            detector time constants, for the given frequencies
            """
            return 1/(2*np.pi*1j*freq*tau+1)
 
        tod_string = str(tod_name)
        tc = TimeConstants.read_from_path('/mnt/act3/users/spho/2016/TimeCo\
nstantsperTOD_170718/pa3/' + tod_string[:5] + '/' + tod_string + '.tau')
        tod = moby2.tod.detrend_tod(data)

        for i in range(1015):
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
        
        self.get_store().set(self._output_key,data)
    
