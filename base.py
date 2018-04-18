import cPickle


class CutLoop:
    def __init__(self, depot = "outputs/cuts/"):
        self._routines = []
        self._veto = False
        self._depot = depot
        self.meta = None
        
    def add_routine(self, routine):
        self._routines.append(routine)
        routine.add_context(self)
        
    def on_cuts(self, cuts):
        # loop over dets
        for cut in cuts:
            for routine in self._routines:
                if self._veto:
                    break
                else:
                    routine.on_det(cut)
            self._veto = False
    
    def run_on_list(self, cuts_list):
        """Assume input is a list of cut ids"""
        for cut_id in range(len(cuts_list)):
            cuts = self.load_cuts(cut_id)
            for routine in self._routines:
                routine.on_file_load()
            
            self.on_cuts(cuts)
            
            for routine in self._routines:
                routine.on_file_finish()
            
    def veto_cut(self):
        self._veto = True
        
    def load_cuts(self, cut_id):
        print '[INFO] Loading %d.cut' % cut_id
        with open(self._depot+str(cut_id)+".cut", "r") as f:
            cut_meta = cPickle.load(f)
        self.meta = cut_meta
        return cut_meta['cuts'].cuts

class Routine:
    def __init__(self):
        self._context = None
    
    def on_file_load(self):
        pass
    
    def on_file_finish(self):
        pass
    
    def on_det(self, cut):
        return cut
    
    def veto(self):
        self.get_context().veto_cut()
        
    def add_context(self, context):
        self._context = context
        
    def get_context(self):
        return self._context
    