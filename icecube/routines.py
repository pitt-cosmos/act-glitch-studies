from todloop.base import Routine
import moby2
import numpy as np
import cPickle

class ExtractRaDec(Routine):
    def __init__(self, input_key, output_key, ra_range, dec_range):
        """Scripts that run during initialization of the routine"""
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key
        self._ra_range = ra_range
        self._dec_range = dec_range

        # Initialize arrays to store temperature info
        self._t_means = []  # mean temperature
        self._c_means = []  # temperature fluctuation
        self._t_stds = []   # mean time affected
        
    def initialize(self):
        """Scripts that run before processing the first TOD"""
        user_config = moby2.util.get_user_config()
        moby2.pointing.set_bulletin_A(params=user_config.get('bulletin_A_settings'))

    def execute(self):
        """Scripts that run for each TOD"""
        tod_data = self.get_store().get(self._input_key)
        ra, dec = moby2.pointing.get_coords(tod_data.ctime, tod_data.az, tod_data.alt)

        ra_lower = self._ra_range[0]
        ra_upper = self._ra_range[1]
        dec_lower = self._dec_range[0]
        dec_upper = self._dec_range[1]

        # Select the elements that fall into the range
        sel = np.all((ra>ra_lower, ra<ra_upper, dec>dec_lower, dec<dec_upper), axis=0)

        # Simplest calculation -> get all data points that pass our 
        # selection and plot the average temperature of all det and
        # all data points. The assumption that I am making here is 
        # that the time scale of variation that we are looking at 
        # here is on the order of days, so the variation on the 
        # scale of 10 mins is irrelevant
        snippets = tod_data.data[:, sel]

        # Next find only TES detectors and only look at 150GHz dets
        tod_info = tod_data.info
        tes_mask = tod_info.array_data['det_type'] == 'tes'
        f150_mask = tod_info.array_data['fcode'] == 'f150'

        mask = np.all((tes_mask, f150_mask), axis=0)

        all_detectors = tod_info.det_uid
        sel_detectors = all_detectors[mask]
        print "Good detector: ", sel_detectors
        print "# good det: ", len(sel_detectors)
        print "# all det: ", len(all_detectors)

        # Next find the mean temperature and error
        t_mean = snippets[sel_detectors, :].mean()  
        t_std = snippets[sel_detectors, :].std()  
        ctime_mean = tod_data.ctime[sel].mean()  # find mean time

        print "Mean temperature: ", t_mean
        print "Temperature stddev: ", t_std
        print "Occured at: ", ctime_mean

        # Save to array
        self._t_means.append(t_mean)
        self._c_means.append(ctime_mean)
        self._t_stds.append(t_std)
                        
        # Removed for simplicity
        #
        # output = {
        #     "mask": sel,  
        #     "t_mean": t_mean,
        #     "t_std": t_std,
        #     "ctime_mean": ctime_mean
        # }
        # self.get_store().set(self._output_key, output)
                
    def finalize(self):
        """Scripts that run after processing all TODs"""
        # Dump data for furthur processing
        temp_data = {
            "t_means": self._t_means,
            "t_stds": self._t_stds,
            "c_means": self._c_means
        }
        with open("temp_data.dat", "w") as f:
            cPickle.dump(temp_data, f)

        
        

