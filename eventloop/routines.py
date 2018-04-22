import os
from eventloop.base import Routine
import cPickle


class DataDump(Routine):
    """A routine to save data in data store"""
    def __init__(self, key, output_dir):
        Routine.__init__(self)
        self._key = key
        self._output_dir = output_dir
        
    def initialize(self):
        if not os.path.exists(self.output_dir):
            print '[INFO] Path %s does not exist, creating ...' % self._output_dir
            os.makedirs(self._output_dir)
    
    def execute(self):
        tod_id = self.get_context().get_id()
        data = self.get_context().get_store().get(self._key)
        with open(self._output_dir+str(tod_id)+".pickle", "w") as f:
            cPickle.dump(data, f, cPickle.HIGHEST_PROTOCOL)