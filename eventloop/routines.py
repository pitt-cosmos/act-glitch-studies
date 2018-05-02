import os
from eventloop.base import Routine
import cPickle


class OutputRoutine(Routine):
    """A base routine that has output functionality"""
    def __init__(self, output_dir):
        Routine.__init__(self)
        self._output_dir = output_dir

    def initialize(self):
        if not os.path.exists(self._output_dir):
            print '[INFO] Path %s does not exist, creating ...' % self._output_dir
            os.makedirs(self._output_dir)

    def save_data(self, data):
        tod_id = self.get_context().get_id()
        with open(self._output_dir+str(tod_id)+".pickle", "w") as f:
            cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL)

    def save_figure(self, fig):
        tod_id = self.get_context().get_id()
        fig.savefig(self._output_dir+str(tod_id)+".png")

    def finalize(self):
        # write metadata to the directory
        metadata = self.get_context().get_metadata()
        if metadata:  # if metadata exists
            with open(self._output_dir+".metadata", "w") as f:
                cPickle.dump(metadata, f, cPickle.HIGHEST_PROTOCOL)


class DataDump(OutputRoutine):
    """A routine to save data in data store"""
    def __init__(self, key, output_dir):
        OutputRoutine.__init__(self, output_dir)
        self._key = key

    def execute(self):
        data = self.get_context().get_store().get(self._key)
        self.save_data(data)

