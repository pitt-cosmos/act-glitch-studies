import moby2
import matplotlib
matplotlib.use("TKAgg")
from eventloop.routines import OutputRoutine
import matplotlib.pyplot as plt
from jpixels import PixelReader

class CompileCuts(OutputRoutine):
    """A routine that compile cuts"""
    def __init__(self, input_key, glitchp, output_dir):
        OutputRoutine.__init__(self, output_dir)
        self._input_key = input_key
        self._glitchp = glitchp

    def initialize(self):
	self._pr = PixelReader()

    def execute(self):
        print '[INFO] Finding glitches'
        tod_data = self.get_context().get_store().get(self._input_key)  # retrieve tod_data
	moby2.tod.remove_mean(tod_data)
	cuts = self.get_context().get_store().get("cuts")
	cosig_data = self.get_context().get_store().get("data")
	print(cuts)
	
	def timeseries(pixel_id,cut_num):
		start_time = cuts['coincident_signals'][str(pixel_id)][cut_num][0]
		start_time -= 50
		end_time = cuts['coincident_signals'][str(pixel_id)][cut_num][1]
		end_time += 50
		a1,a2 = self._pr.get_f1(pixel_id)
   		b1,b2= self._pr.get_f2(pixel_id)
    		d1,d2 = tod_data.data[a1],tod_data.data[a2]
    		d3,d4 = tod_data.data[b1],tod_data.data[b2]
    		time = tod_data.ctime - tod_data.ctime[0]
    		time = time[start_time:end_time]
    		plt.plot(time,d1[start_time:end_time],'.-',label=str(a1) + ' 90 Hz')
    		plt.plot(time,d2[start_time:end_time],'.-',label=str(a2) + ' 90 Hz')
    		plt.plot(time,d3[start_time:end_time],'.-', label = str(b1)+' 150 Hz')
    		plt.plot(time,d4[start_time:end_time],'.-', label = str(b2)+' 150 Hz')
    		plt.legend(title='Detector UID')
		plt.show()
	#print(cuts['coincident_signals']['23'])
	timeseries(73,14)

