from matplotlib import pyplot as plt
import cPickle
with open("temp_data.dat", "r") as f:
    data = cPickle.load(f)

plt.errorbar(data['c_means'], data['t_means'], yerr=data['t_stds'], fmt='o-')
plt.xlabel('Unix_time / s')
plt.ylabel('Temperature / K')
plt.show()
