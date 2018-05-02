from eventloop.base import Routine
from eventloop.utils.cuts import remove_overlap_tod, trim_edge_cuts


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



