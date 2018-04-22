from eventloop.base import Routine


class DurationFilter(Routine):
    """An event filter based on the duration of events (set max duration)"""
    def __init__(self, max_duration=50):
        Routine.__init__(self)
        self.max_duration = max_duration
        
    def execute(self):
        cosig = self.get_context().get_store().get("cosig")
        peaks = cosig['peaks']
        print '[INFO] Before: n_tracks = %d' % len(cosig['peaks'])
        peaks_filtered = [peak for peak in peaks if peak[2] < self.max_duration]
        cosig['peaks'] = peaks_filtered
        print '[INFO] After: n_tracks = %d' % len(cosig['peaks'])
        self.get_context().get_store().set("cosig", cosig)
        
        
class PixelFilter(Routine):
    """An event filter based on the number of pixels affected (set max n_pixels)"""
    def __init__(self, max_pixels=10):
        Routine.__init__(self)
        self.max_pixels = max_pixels
        
    def execute(self):
        cosig = self.get_context().get_store().get("cosig")
        peaks = cosig['peaks']
        print '[INFO] Before: n_tracks = %d' % len(cosig['peaks'])
        peaks_filtered = [peak for peak in peaks if peak[3] < self.max_pixels]
        cosig['peaks'] = peaks_filtered
        print '[INFO] After: n_tracks = %d' % len(cosig['peaks'])
        self.get_context().get_store().set("cosig", cosig)
        