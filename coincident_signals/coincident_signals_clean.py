import moby2
import math
import cPickle
import numpy as np
from pixels import PixelReader
from cuts import *
#from matplotlib import pyplot as plt
import sys

def find_peaks(hist):
    nsamps = len(hist)
    last = 0
    peaks = []
    for i in range(nsamps):
        if hist[i] > 0 and last == 0:
            peak_start = i    
        if hist[i] == 0 and last > 0:
            peak_end = i
            peak_amp = max(hist[peak_start:peak_end])
            peak_duration = peak_end - peak_start
            peaks.append([peak_start, peak_end, peak_duration, peak_amp])
        last = hist[i]
    return peaks

ardata = moby2.scripting.get_array_data({'season':'2016', 'array_name':'AR3'})
start = int(sys.argv[1])
end = int(sys.argv[2])
loose = True # loose means we merge across polarization instead find overlap
remove_mce = True
trim_edge = True

for cut_no in range(start, end):
    try:
        print 'Loading cut:', cut_no
        #cuts_data = cPickle.load(open("outputs/cuts/"+str(cut_no)+".cut","rb"))
        cuts_data = cPickle.load(open("outputs/cuts/"+str(cut_no)+".cut","rb"))
        cuts = cuts_data['cuts']
        if remove_mce:
            cuts = remove_overlap_tod(cuts, cuts_data['mce'])
        if trim_edge:
            cuts = trim_edge_cuts(cuts, cuts_data['nsamps'])
        coincident_signals = {}
        npix = 0

        # Get a unique list of lixels
        # pr = PixelReader(mask=cuts_data['sel'])
        pr = PixelReader() # test without selection mask
        pixels = pr.get_pixels()

        # Get nsamples
        # nsamps = cuts_data['nsamps']
        nsamps = max([cut[-1][1] for cut in cuts.cuts if len(cut)!=0])
        hist = [0]*nsamps

        for p in pixels:
            det_f90 = []
            det_f150 = []
            has_f90 = True
            has_f150 = True
            for det in pr.get_f1(p):
                if ardata['det_type'][det] == 'tes':
                    det_f90.append(det)

            for det in pr.get_f2(p):
                if ardata['det_type'][det] == 'tes':
                    det_f150.append(det)

            # Merge cuts at two polarization detectors of f90
            if len(det_f90) == 2:
                cuts_A = cuts.cuts[det_f90[0]]
                cuts_B = cuts.cuts[det_f90[1]]
                if loose:
                    cuts_f90 = merge_cuts(cuts_A, cuts_B) #Look at polarized spike that may appera at either pol
                else:
                    cuts_f90 = common_cuts(cuts_A, cuts_B) #Only look at unpolarized spike that appear at both pols

            elif len(det_f90) == 1:
                cuts_f90 = cuts.cuts[det_f90[0]]

            else:
                cuts_f90 = None
                has_f90 = False

            # Merge cuts at two polarization detectors of f150
            if len(det_f150) == 2:
                cuts_A = cuts.cuts[det_f150[0]]
                cuts_B = cuts.cuts[det_f150[1]]
                if loose:
                    cuts_f150 = merge_cuts(cuts_A, cuts_B) #Look at polarized spike that may appera at either pol
                else:
                    cuts_f150 = common_cuts(cuts_A, cuts_B) #Only look at unpolarized spike that appear at both pols

            elif len(det_f150) == 1:
                cuts_f150 = cuts.cuts[det_f150[0]]

            else:
                cuts_f150 = None
                has_f150 = False
            # Loose mode -> Each frequency has to have at least one working det.
            '''
            if has_f90 and has_f150:
                cc = common_cuts(cuts_f90, cuts_f150)
                hist += cc.get_mask(nsamps=nsamps)
                npix += 1
                coincident_signals[str(p)] = cc
            '''
            # Strict mode -> Each frequency has to have two working det.
            if len(det_f90) ==2 and len(det_f150) == 2:
                cc = common_cuts(cuts_f90, cuts_f150)
                npix += 1
                hist += cc.get_mask(nsamps=nsamps)
                coincident_signals[str(p)] = cc

        # cPickle.dump(find_peaks(hist), open("outputs/coincident_signals_peaks/"+str(cut_no)+".tmp", "wb"), cPickle.HIGHEST_PROTOCOL) # save peaks
        output = {
            'coincident_signals': coincident_signals,
            'peaks': find_peaks(hist) 
        }
        cPickle.dump(output, open("outputs/coincident_signals/"+str(cut_no)+".pickle", "wb"), cPickle.HIGHEST_PROTOCOL) # save coincident signals only
        print 'Total number of pixel of interests is:', npix 

        # if you are interested in how the plot looks like
        #plt.figure()
        #plt.plot(hist) 
        #plt.show()
        #plt.savefig('outputs/coincident_signals_hist/%d.png' % cut_no)
    except Exception as e:
        print '[ERROR] Exception caught!'
        print e
