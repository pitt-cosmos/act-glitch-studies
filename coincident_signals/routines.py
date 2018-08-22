from todloop.base import Routine
from todloop.utils.cuts import remove_overlap_tod, trim_edge_cuts, merge_cuts, common_cuts
from todloop.utils.pixels import PixelReader
import numpy as np


class RemoveMCE(Routine):
    """A routine that removes mce glitches from all glitches"""
    def __init__(self, input_key="cuts", output_key="cuts"):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key

    def execute(self):
        cuts_data = self.get_store().get(self._input_key)  # get saved cut data
        glitch_cuts = cuts_data['cuts']  # retrieve glitch cuts from cut_data
        mce_cuts = cuts_data['mce']  # retrieve mce cuts

        # remove the glitch cuts that overlap with mce glitches
        clean_cuts = remove_overlap_tod(glitch_cuts, mce_cuts)

        # save cleaned cuts to data store
        cuts_data['cuts'] = clean_cuts
        self.get_store().set(self._output_key, cuts_data)


class TrimEdges(Routine):
    """A routine that that removes the glitches near the edges of TODs"""
    def __init__(self, input_key="cuts", output_key="cuts"):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key

    def execute(self):
        cuts_data = self.get_store().get(self._input_key)  # get saved cut data
        glitch_cuts = cuts_data['cuts']  # retrieve glitch cuts from cut_data
        nsamps = cuts_data['nsamps']  # get the number of sampling points

        clean_cuts = trim_edge_cuts(glitch_cuts, nsamps)

        # save cleaned cuts to data store
        cuts_data['cuts'] = clean_cuts
        self.get_store().set(self._output_key, cuts_data)


class FindCosigs(Routine):
    """A routine that compiles the coincident signals from cuts"""
    def __init__(self, season="2017", array="AR5", input_key="cuts", output_key="cosig", strict=True, polarized=False):
        """
        :param input_key: string
        :param output_key: string
        :param strict: boolean - Strict mode means each pixel must have 4 TES
                       detectors. Loose mode means that each frequency has at
                       least one TES detectors.
        :param polarized: boolean - True means that we are looking for potentially
                        polarized signals. False means that we only look for
                        un-polarized signals.
        """
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key
        self._pr = None
        self._strict = strict
        self._polarized = polarized
        self._season = season
        self._array = array

    def initialize(self):
        self._pr = PixelReader(season=self._season, array=self._array)
        if (not self._strict) and (not self._polarized):  # give a warning
            print '[WARNING] Using loose mode for unpolarized signals may not be accurate'

    def execute(self):
        # retrieve all cuts
        cuts_data = self.get_store().get(self._input_key)  # get saved cut data
        cuts = cuts_data['cuts']
        nsamps = cuts_data['nsamps']

        # get all pixels
        pixels = self._pr.get_pixels()

        # initialize dictionary to store coincident signals
        cosig = {}

        # loop through pixels and find cosig for each pixel
        for p in pixels:
            dets_f1 = self._pr.get_f1(p)
            dets_f2 = self._pr.get_f2(p)

            if self._strict:  # strict mode, 4 TES have to be present
                if len(dets_f1) == 2 and len(dets_f2) == 2:
                    cuts_f1_A = cuts.cuts[dets_f1[0]]  # low freq, polarization A
                    cuts_f1_B = cuts.cuts[dets_f1[1]]  # low freq, polarization B

                    cuts_f2_A = cuts.cuts[dets_f2[0]]  # high freq, polarization A
                    cuts_f2_B = cuts.cuts[dets_f2[1]]  # high freq, polarization B

                    if self._polarized:  # if looking for polarized, glitch may occur in either polarization
                        cuts_f1 = merge_cuts(cuts_f1_A, cuts_f1_B)  # polarized spikes may appear at either pol
                        cuts_f2 = merge_cuts(cuts_f2_A, cuts_f2_B)

                    else:  # if looking for unpolarized, glitch must occur in both polarizations
                        cuts_f1 = common_cuts(cuts_f1_A, cuts_f1_B)  # unpolarized spikes appear in both pols
                        cuts_f2 = common_cuts(cuts_f2_A, cuts_f2_B)

                    cosig[str(p)] = common_cuts(cuts_f1, cuts_f2)  # store coincident signals by pixel id

            else:  # loose mode, at least one TES has to be present each freq
                if len(dets_f1) == 2 and len(dets_f2) == 2:
                    cuts_f1_A = cuts.cuts[dets_f1[0]]  # low freq, polarization A
                    cuts_f1_B = cuts.cuts[dets_f1[1]]  # low freq, polarization B

                    cuts_f2_A = cuts.cuts[dets_f2[0]]  # high freq, polarization A
                    cuts_f2_B = cuts.cuts[dets_f2[1]]  # high freq, polarization B

                    if self._polarized:  # if looking for polarized, glitch may occur in either polarization
                        cuts_f1 = merge_cuts(cuts_f1_A, cuts_f1_B)  # polarized spikes may appear at either pol
                        cuts_f2 = merge_cuts(cuts_f2_A, cuts_f2_B)

                    else:  # if looking for unpolarized, glitch must occur in both polarizations
                        cuts_f1 = common_cuts(cuts_f1_A, cuts_f1_B)  # unpolarized spikes appear in both pols
                        cuts_f2 = common_cuts(cuts_f2_A, cuts_f2_B)

                    cosig[str(p)] = common_cuts(cuts_f1, cuts_f2)  # store coincident signals by pixel id

                elif len(dets_f1) == 1 and len(dets_f2) == 2:
                    cuts_f1 = cuts.cuts[dets_f1[0]]  # low freq, polarization A

                    cuts_f2_A = cuts.cuts[dets_f2[0]]  # high freq, polarization A
                    cuts_f2_B = cuts.cuts[dets_f2[1]]  # high freq, polarization B

                    if self._polarized:  # if looking for polarized, glitch may occur in either polarization
                        cuts_f2 = merge_cuts(cuts_f2_A, cuts_f2_B)

                    else:  # if looking for unpolarized, glitch must occur in both polarizations
                        cuts_f2 = common_cuts(cuts_f2_A, cuts_f2_B)

                    cosig[str(p)] = common_cuts(cuts_f1, cuts_f2)  # store coincident signals by pixel id

                elif len(dets_f1) == 2 and len(dets_f2) == 1:
                    cuts_f1_A = cuts.cuts[dets_f1[0]]  # low freq, polarization A
                    cuts_f1_B = cuts.cuts[dets_f1[1]]  # low freq, polarization B

                    cuts_f2 = cuts.cuts[dets_f2[0]]  # high freq, polarization A

                    if self._polarized:  # if looking for polarized, glitch may occur in either polarization
                        cuts_f1 = merge_cuts(cuts_f1_A, cuts_f1_B)

                    else:  # if looking for unpolarized, glitch must occur in both polarizations
                        cuts_f1 = common_cuts(cuts_f1_A, cuts_f1_B)

                    cosig[str(p)] = common_cuts(cuts_f1, cuts_f2)  # store coincident signals by pixel id

                elif len(dets_f1) == 1 and len(dets_f2) == 1:
                    cuts_f1 = cuts.cuts[dets_f1[0]]  # low freq, polarization A
                    cuts_f2 = cuts.cuts[dets_f2[0]]  # high freq, polarization A

                    cosig[str(p)] = common_cuts(cuts_f1, cuts_f2)  # store coincident signals by pixel id

        # cosig may contain empty cut vectors because we didn't enforce it, filter them out now
        cosig_filtered = {}
        for pixel in cosig:
            cuts = cosig[pixel]
            if len(cuts) != 0:
                cosig_filtered[pixel] = cuts

        # save cosig for further processing
        self.get_store().set(self._output_key, cosig_filtered)  # save the coincident signals under the output_key
        self.get_store().set("nsamps", nsamps)  # save the number of sampling points, not graceful


class FindEvents(Routine):
    """A routine to find events that cause multiple cosigs
    dependency: FindCosigs"""
    def __init__(self, input_key="cosig", output_key="events"):
        Routine.__init__(self)
        self._input_key = input_key
        self._output_key = output_key
        self._cosig = None
        self._nsamps = None

    def find_peaks(self, hist):
        """Find peaks in the histogram corresponding to physical events
        :param hist: histogram of coincident signals
        :return: list: [start_time, end_time, duration, n_pixels_affected]
        """
        last = 0
        peaks = []
        for i in range(self._nsamps):
            if hist[i] > 0 and last == 0:
                peak_start = i
            if hist[i] == 0 and last > 0:
                peak_end = i
                peak_amp = max(hist[peak_start:peak_end])
                peak_duration = peak_end - peak_start
                peaks.append([peak_start, peak_end, peak_duration, peak_amp])
            last = hist[i]
        return peaks

    def execute(self):
        self._cosig = self.get_store().get(self._input_key)
        self._nsamps = self.get_store().get("nsamps")  # get nsamps from FindCosigs, not graceful

        # generate a histogram of cosigs
        cosig_hist = np.zeros(self._nsamps)

        for pixel in self._cosig:  # loop through key and value pair in cosig dict
            cuts = self._cosig[pixel]
            mask = cuts.get_mask(nsamps=self._nsamps)
            cosig_hist += mask

        cosig_peaks = self.find_peaks(cosig_hist)

        # export the coincident signals and the peaks found in a combined dictionary
        cosig_combined = {
            'coincident_signals': self._cosig,
            'peaks': cosig_peaks
        }
        self.get_store().set(self._output_key, cosig_combined)








