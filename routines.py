from eventloop.utils.pixels import PixelReader
from eventloop.base import Routine
from eventloop.utils.cuts import *
import moby2
from moby2.instruments import actpol
from moby2.scripting import get_filebase

class TestRoutine(Routine):
    def __init__(self):
        Routine.__init__(self)

    def initialize(self):
        self.filebase = get_filebase()

    def execute(self):
        cosig = self.get_context().get_store().get("data")
        cs = cosig['coincident_signals']
        print cs
        tod_name = self.get_context().get_name()
	name = self.filebase.filename_from_name(tod_name,single=True)
	print name
