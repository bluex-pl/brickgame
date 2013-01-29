class Timers(object): # TODO counter for maxFps multiplicity
    def __init__(self, maxFps):
        """Initialize timers

        maxFps - game frame rate
        """
        self.maxFps = maxFps
        self.timers = {}
        self.counter = 0 # counter for ticks
        self.counter2 = 0 # counter for maxFps multiplicity

    def add_new(self, name, func, fps, rep=0, type='g'):
        """Add new timer

        name - timer name
        func - function to run with specified frame rate
        fps  - frame rate
        rep  - amount of repetitions
                0   - run forever
               >0   - repeat x times
               <0   - repeat x times when started (created in paused mode)
               None - run forever when started (created in paused mode)
        type - timer type
               s - system timer
               g - game timer (deleted when game module ends)
        """
        #if type(name) != type(''):
        #    raise TypeError, "timer name must be string"
        if not callable(func):
            raise ValueError, "non callable object '%s'" % func.func_name
        if self.maxFps%fps != 0:
            raise ValueError, "maxFps=%d must be divisible by fps=%d"%(self.maxFps, fps)
        if type[0] not in ('g', 's'):
            raise ValueError, "timer type must be s(system) or g(game)"
        if type == 'g' and self.timers.has_key(name):
            raise ValueError, "can't overwrite system timer"
        self.timers[name] = [func, self.maxFps/fps, rep, type[0]]

    def modify(self, name, func=None, fps=None, rep=False):
        """Modify timer

        name - timer name
        func - function to run with specified frame rate (default previous value)
        fps  - frame rate (default previous value)
        rep  - amount of repetitions (default previous value)
                0   - run forever
               >0   - repeat x times
               <0   - repeat x times when started (created in paused mode)
               None - run forever when started (created in paused mode)
        """
        tmp_t = self.timers[name]
        if func is None:
            func = tmp_t[0]
        if fps is None:
            fps = tmp_t[1]
        if rep == False:
            rep = tmp_t[2]
        self.add_new(name, func, fps, rep, tmp_t[3])

    def rem(self, names):
        """Remove timer

        names - names list or single name used as argument when adding timer
        """
        if type(names) == type(str()):
            names = (names,)
        for name in names:
            try:
                del self.timers[name]
            except KeyError:
                pass

    def switch(self, names):
        """Pause/Unpause timer

        names - names used as argument when adding timer
        """
        if type(names) == type(str()):
            names = (names,)
        for name in names:
            try:
                v = self.timers[name]
                if v[2] == 0:
                    v[2] = None
                elif v[2] is None:
                    v[2] = 0
                else:
                    v[2] = -v[2]
            except KeyError:
                pass

    def pause(self, names):
        """Pause timer

        names - names used as argument when adding timer
        """
        if type(names) == type(str()):
            names = (names,)
        for name in names:
            try:
                v = self.timers[name]
                if v[2] == 0:
                    v[2] = None
                elif v[2] is not None:
                    v[2] = -abs(v[2])
            except KeyError:
                pass

    def unpause(self, names):
        """Unause timer

        names - names used as argument when adding timer
        """
        if type(names) == type(str()):
            names = (names,)
        for name in names:
            try:
                v = self.timers[name]
                if v[2] is None:
                    v[2] = 0
                else:
                    v[2] = abs(v[2])
            except KeyError:
                pass

    def list_type(self, type):
        """Generate list of timers with scpecified type

        type - timer type (s / g)

        return - list of timers names
        """
        return [k for k,v in self.timers.iteritems() if v[3] == type]

    def tick(self):
        for k in self.timers.keys():
            v = self.timers[k]
            if self.counter % v[1] == 0 and v[2] > -1:
                v[0]()
                if v[2] > 1:
                    v[2] -= 1
                elif v[2] == 1:
                    del self.timers[k]
        self.counter += 1
        if self.counter == self.maxFps:
            self.counter = 0
            self.counter2 += 1
            if self.counter2 > 100:
                self.counter2 = 0

    def __getitem__(self, name):
        return tuple(self.timers[name])