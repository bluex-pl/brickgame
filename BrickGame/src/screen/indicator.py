import pygame

class Indicator(object):
    def __init__(self, color, rect):
        self.state = 0
        self.color = color
        self.rect = rect
        self.changed = True

    def __setattr__(self, name, value):
        if name != 'changed':
            object.__setattr__(self, name, value)
            object.__setattr__(self, 'changed', True)
        else:
            object.__setattr__(self, name, value)

class Indicators(object):
    def __init__(self, image, off_color, data={}):
        self.screen = pygame.display.get_surface()
        self.image = image
        self.bgcolor = off_color
        self.indicators = {}
        self.changed = []
        for name, item in data.iteritems():
            self.add_new(name, item)

    def add_new(self, name, data):
        #self.changed.append(name)
        if not self.indicators.has_key(name):
            self.indicators[name] = Indicator(*data)

    def state(self, name, st=None):
        if not self.indicators.has_key(name):
            raise ValueError, "There is no item named '%s'" % (name)
        self.changed.append(name)
        if st is not None:
            self.indicators[name].state = st
        else:
            self.indicators[name].state = int(not self.indicators[name].state)
        return self.indicators[name].state

    def color(self, name, color):
        if not self.indicators.has_key(name):
            raise ValueError, "There is no item named '%s'" % (name)
        self.changed.append(name)
        old_color = self.indicators[name].color
        self.indicators[name].color = color
        return old_color

    def update(self):
        for item in self.indicators.itervalues():
            if item.changed == True:
                color = item.color if item.state else self.bgcolor
                self.screen.fill(color, item.rect)
                self.screen.blit(self.image, item.rect, item.rect)
                pygame.display.update(item.rect)
                item.changed = False
        #self.changed = []

    def __getitem__(self, name):
        return self.indicators[name]

    def __getattr__(self, name):
        if self.indicators.has_key(name):
            return self.indicators[name]
        else:
            raise AttributeError, name
