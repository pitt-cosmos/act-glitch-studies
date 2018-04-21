import cPickle
import glob


class EventLoop:
    """Main driving class for looping through coincident signals of different TODs"""
    def __init__(self, depot = "outputs/coincident_signals/", postfix="pickle"):
        self._routines = []
        self._veto = False
        self._depot = depot
        self._store = DataStore()  # initialize data store
        
    def add_routine(self, routine):
        """Add a routine to the event loop"""
        self._routines.append(routine)
        routine.add_context(self)  # make event loop accessible in each routine
        
    def get_store(self):
        """Access the shared data storage"""
        return self._store
    
    def retrieve_file(self):
        self._files = glob.glob(self._depot + "*." + postfix)
        
    def initialize(self):
        """Initialize all routines"""
        for routine in self._routines:
            routine.initialize()
    
    def execute(self):
        """Execute all routines"""
        for routine in self._routines:
            # check veto signal, if received, skip subsequent routines
            if self._veto:
                break
            else:
                routine.execute()
        self._veto = False
    
    def finalize(self):
        """Finalize all routines"""
        for routine in self._routines:
            routine.finalize()
    
    def veto(self):
        """Veto a TOD from subsequent routines"""
        self._veto = True

        
        
class Routine:
    def __init__(self):
        self._context = None
    
    def initialize(self):
        pass
    
    def veto(self):
        self.get_context().veto()
        
    def add_context(self, context):
        self._context = context
        
    def get_context(self):
        return self._context
    

    
class DataStore:
    """Cache class for event loop"""
    def __init__(self):
        self._store = {}
    
    def get(self, key):
        """Retrieve an object based on a key
        @par: 
            key: str
        @ret:   
            Object of an arbitrary type associated with the key
            or None if no object is associated with the key"""
        
        if key in self._store:
            return self._store[key]
        else:
            return None
    
    def set(self, key, obj):
        """Save an object with a key
        @par:
            key: str
            obj: a object of arbitrary type
        @ret: nil"""
        
        self._store[key] = obj
        