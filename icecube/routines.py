from todloop.base import Routine
import moby2
import numpy as np
import cPickle
from utils import get_cuts_tag, get_pointing_par
from moby2.scripting import products

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
        # Obtain tod_data from memory store
        tod_data = self.get_store().get(self._input_key)
        
        # Reference ra and dec: reference values are used to select
        # a reasonably sized chunk instead of the whole time stream
        # which takes a long time to process
        
        # Set reference range to 2 times the search range
        ref_ra_lo = 1.5*self._ra_range[0] - 0.5*self._ra_range[1]
        ref_ra_up = 1.5*self._ra_range[1] - 0.5*self._ra_range[0]
        ref_dec_lo = 1.5*self._dec_range[0] - 0.5*self._dec_range[1]
        ref_dec_up = 1.5*self._dec_range[1] - 0.5*self._dec_range[0]
        print "Ref ra: [%.2f, %.2f]" % (ref_ra_lo, ref_ra_up)
        print "Ref dec: [%.2f, %.2f]" % (ref_dec_lo, ref_dec_up)
        
        # Set physical range
        ra_lower, ra_upper = self._ra_range
        dec_lower, dec_upper = self._dec_range
        print "ra: [%.2f, %.2f]" % (ra_lower, ra_upper)
        print "dec: [%.2f, %.2f]" % (dec_lower, dec_upper)

        # Retrieve ra, dec in reference range
        ref_ra, ref_dec = moby2.pointing.get_coords(tod_data.ctime, tod_data.az, tod_data.alt)
        
        # Reduce data to the reference range only
        ref_sel = np.all((ref_ra>ref_ra_lo, ref_ra<ref_ra_up, \
                          ref_dec>ref_dec_lo, ref_dec<ref_dec_up), axis=0)
        ctime = tod_data.ctime[ref_sel]
        az = tod_data.az[ref_sel]
        alt = tod_data.alt[ref_sel]
        print 'Ref region reduction: %d/%d' % (len(ctime), len(tod_data.ctime))

        # Calculate physical ra and dec in reference region
        pointpar = get_pointing_par(tod_data)
        print 'Getting focal plane'
        fplane = products.get_focal_plane(pointpar,\
                                          det_uid=tod_data.det_uid, \
                                          tod_info=tod_data.info, \
                                          tod=tod_data)
        
        phy_ra, phy_dec = moby2.pointing.get_coords(ctime, az, alt, \
                                                    focal_plane=fplane)
        print "ra.shape: ", phy_ra.shape
        print "dec.shape: ", phy_dec.shape

        # Reduction in size by detector analysis (cuts, freq,
        # det_type, etc.)  First load tag to locate the cuts depot.
        # This part has been commented off, because I couldn't figure
        # out which depot to use -> will need to ask from Loic
        
        # tag = get_cuts_tag(tod_data)
        
        # print "[INFO] Trying cut depot: ", tag
        # cuts = moby2.scripting.get_cuts({'depot': '/mnt/act3/users/lmaurin/depot',\
        #                                  'tag':  tag}, tod=tod_data)
                        
        # Find the live detectors
        # ld = cuts.get_uncut()
        # print "# of live detectors: ", len(ld)

        # Find only TES detectors and only look at 150GHz dets
        tod_info = tod_data.info 
        tes_mask = tod_info.array_data['det_type'] == 'tes'
        f150_mask = tod_info.array_data['nom_freq'] == 150.0
        
        mask = np.all((tes_mask, f150_mask), axis=0) 

        all_dets = tod_info.det_uid 
        sel_dets = all_dets[mask]
        print '# of all dets:', len(all_dets)
        print '# of sel dets:', len(sel_dets)
                                    
        # Reduce ra, dec to only good detectors
        ra = phy_ra[sel_dets, :]
        dec = phy_dec[sel_dets, :]
        _tod = tod_data.data[sel_dets, :]
        tod = _tod[:, ref_sel]
        
        # Restrict to only physical range
        mask_ra = np.logical_and(ra>ra_lower, ra<ra_upper)
        mask_dec = np.logical_and(dec>dec_lower, dec<dec_upper)
        mask = np.logical_and(mask_ra, mask_dec) 

        print '[INFO] mask obtained: mask.shape', mask.shape

        # Simplest calculation -> get all data points that pass our 
        # selection and plot the average temperature of all det and
        # all data points. The assumption that I am making here is 
        # that the time scale of variation that we are looking at 
        # here is on the order of days, so the variation on the 
        # scale of 10 mins is irrelevant
        
        snippets = tod[mask]
        
        print '[INFO] snippet obtained'
        print '[DEBUG] snippets.shape: ', snippets.shape
        

        # Next find the mean temperature and error
        t_mean = snippets.mean()  
        t_std = snippets.std()  
        ctime_mean = ctime.mean()  # find mean time

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

        
        

