import cPickle
from matplotlib.colors import LogNorm
import glob
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
import numpy as np

scatter = []

files =glob.glob("outputs/coincident_signals_subset/*.pickle")
fCounter = 0
for f in files:
    fCounter += 1
    with open(f, "rb") as _f:
        scatter.extend(cPickle.load(_f)['peaks'])
    print '[INFO] Number of files processed:', fCounter
        
#print scatter
x = [item[2] for item in scatter]
y = [item[3] for item in scatter]

#plt.scatter(np.log(x), y)
plt.hist2d(np.log(x)/np.log(10), y, bins=[50,50], norm=LogNorm())
#plt.hist2d(x, y, bins=[10.0**np.linspace(0,4,40), np.linspace(0, 140, 40)], norm=LogNorm())
#plt.hist2d(np.log(x)/np.log(10), y, bins=[40,40])
plt.colorbar()
#plt.xscale('log')
plt.xlabel("Coincident Signal Duration (sampling points) 10^x")
plt.ylabel("Number of Pixels Affected")
plt.show()
