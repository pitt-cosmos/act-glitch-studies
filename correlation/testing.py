import matplotlib
matplotlib.use("TKAgg")
import matplotlib.pyplot as plt
import numpy as np
import moby2
from moby2.instruments import actpol
from moby2.scripting import get_filebase
from moby2.detectors.stuff import TimeConstants

#tc = TimeConstants.read_from_path("/mnt/act3/users/spho/2016/TimeConstantsperTOD_170718/pa3/14754/1475438739.1475455671.ar3.tau")


db = actpol.TODDatabase()
ids = db.select_tods()
tid = 10000 #tod 
did = 127  #detector uid
tod_name = ids[tid].basename
tod_string = str(tod_name)
fb = get_filebase()
tod_dir = fb.filename_from_name(tod_name, single=True)
data = moby2.scripting.get_tod({'filename': tod_dir, 'repair_pointing':True})
o_tod = data.data[did]
tc = TimeConstants.read_from_path('/mnt/act3/users/spho/2016/TimeConstantsperTOD_170718/pa2/' + tod_string[:5] + '/' + tod_string + '.tau')

plt.subplot(311)
plt.plot(data.ctime,o_tod)
plt.title('Original')


def tconst_filter(freq,tau):
    """
    Return the fourier space representation of the effect of 
    detector time constants, for the given frequencies
    """
    return 1/(2*np.pi*1j*freq*tau+1)


tod = moby2.tod.detrend_tod(data)
d_tod = data.data[did]
plt.subplot(312)
plt.plot(data.ctime,d_tod)
plt.title('Desloped')


ftod = np.fft.rfft(d_tod)
nsamp = len(d_tod)
srate = 400 #Hz
freqs = np.arange(nsamp//2 + 1)*srate/nsamp
tau = tc.get_property('tau')[1][did]
resp = tconst_filter(freqs,tau)
ftod /= resp 
deconv_tod = np.fft.irfft(ftod)
plt.subplot(313)
plt.plot(data.ctime,deconv_tod)
plt.title('Deconvoluted')
plt.show()


plt.plot(o_tod,'.-',label="original")
plt.plot(d_tod,'.-',alpha=0.6,label="desloped")
plt.plot(deconv_tod,'.-',alpha=0.5,label="deconvoluted")
plt.legend()
plt.show()
