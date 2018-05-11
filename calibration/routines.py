from todloop.base import Routine


class FixOpticalSign(Routine):
    """A routine that corrects for optical sign"""
    def __init__(self, input_key="tod_data"):
        Routine.__init__(self)
        self._input_key = input_key

    def execute(self):
        # fix optical sign of the TOD
        tod_data = self.get_store().get(self._input_key)  # retrieve TOD
        print tod_data.info

