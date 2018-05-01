import moby2
from moby2.scripting import get_filebase
from base import EventLoop


class TODLoop(EventLoop):
    """A EventLoop specifically used to loop over TODs"""
    def __init__(self):
        EventLoop.__init__(self)
        self._tod_list = None
        self._fb = None
        self._abspath = False

    def add_tod_list(self, tod_list_dir, abspath=False):
        if abspath:  # if absolute path is used
            self._abspath = True
        with open(tod_list_dir, "r") as f:
            self._tod_list = [line.split('\n')[0] for line in f.readlines()]
            self._metadata = self._tod_list

    def initialize(self):
        """Initialize all routines"""
        self._fb = get_filebase()
        for routine in self._routines:
            routine.initialize()

    def run(self, start, end):
        """Main driver function to run the loop
        @param:
            start: starting tod_id
            end:   ending tod_id"""

        self.initialize()
        for tod_id in range(start, end):
            self._tod_id = tod_id
            print '[INFO] tod_id: %d' % tod_id

            if self._abspath:  # if absolute path is given
                tod_filename = self._tod_list[tod_id]
            else:
                tod_name = self._tod_list[tod_id]
                print '[INFO] tod_name: %s' % tod_name
                tod_filename = self._fb.filename_from_name(tod_name, single=True)  # get file path

            print '[INFO] tod_filename: %s' % tod_filename
            tod_data = moby2.scripting.get_tod({'filename': tod_filename, 'repair_pointing': True})
            self.get_store().set("tod_data", tod_data)  # save tod_data in memory for routines to process
            self.execute()
        self.finalize()

    def get_metadata(self):
        return self._metadata

