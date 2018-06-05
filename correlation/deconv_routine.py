import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy as np
import moby2
from todloop.base import Routine 
from moby2.instruments import actpol
from moby2.scripting import get_filebase
from moby2.detectors.stuff import TimeConstants

class Deconvolution(Routine):
    def __init__(self,input_key,output_key):
        Routine.__init__(self)
        self._input_key= input_key
        self._output_key = output_key
        
    def execute(self):
        def tconst_filter(freq,tau):
            """
            Return the fourier space representation of the effect of 
            detector time constants, for the given frequencies
            """
            return 1/(2*np.pi*1j*freq*tau+1)
        tid = self._input_key
        db = actpol.TODDatabase()
        ids = db.select_tods()
        deconv_time = []
        for i in range(1015):
            tod_name = ids[tid].basename
            tod_string = str(tod_name)
            fb = get_filebase()
            tod_dir = fb.filename_from_name(tod_name,single=True)
            data = moby2.scripting.get_tod({'filename': tod_dir, 'repair_pointing':True})
            tc = TimeConstants.read_from_path('/mnt/act3/users/spho/2016/TimeConstantsperTOD_170718/pa2/' + tod_string[:5] + '/' + tod_string + '.tau')
            tod = moby2.tod.detrend_tod(data)
            ftod = np.fft.rfft(d_tod)
            nsamp = len(d_tod)
            srate = 400 #Hz
            freqs = np.arange(nsamp//2 + 1) * srate/nsamp
            tau = tc.get_property('tau')[1][i]
            resp = tconst_filter(freqs,tau)
            ftod /= resp
            deconv_tod = np.fft.irfft(ftod)
            deconv_data = {
                'tod' = tid,
                'id' = i,
                'data' = deconv_tod
                }
            deconv_time.append(deconv_data)
        
        self.get_store().set(self._output_key,deconv_time)
