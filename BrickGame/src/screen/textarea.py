import pygame

class Textarea(object):
    def __init__(self, position, size, color, font):
        """Initialize textarea

        position - position of textarea on the screen in pixels (x, y)
        size - size of textarea in chars (w, h)
        color - textarea color
        font - Font class object
        """
        self.size = size
        self._color, self.font = color, font
        self.rect = pygame.Rect(position, (self.size[0]*self.font.width,
                                           self.size[1]*self.font.height))
        #self.surface = pygame.display.get_surface().subsurface(self.rect)
        self.surface = pygame.Surface(self.rect.size)
        self.surface.convert()
        self.surface.set_colorkey(0x000000)
        self.str = ""
        self.prev_str = ""
        self.space = " *** "
        self.mode = 'l '
        self.cursor_v = False
        self.move_allowed = True
        self.changed = ''
        self.counter = -size[0]
        self.editing = False
        self.prev_edit = 0
        self.cursor_c = chr(0x81)

    def put(self, text):
        """Add text to textarea"""
        if type(text) != type(''):
            text = str(text)
        self.str += text
        self.changed += 't'

    def replace(self, text):
        """Replace text in textarea"""
        if type(text) != type(''):
            text = str(text)
        self.str = text
        self.changed += 't'

    def align(self, mode):
        """Text align

        mode -  2 chars string describing align mode
            mode[0] -  one of [l, c, r] - first letter of [left, center, right]
            mode[1] -  fill character
        """
        self.mode = mode
        self.changed += 't'

    def color(self, color):
        """Set text color"""
        self._color = color

    def clear(self):
        """Clear textarea"""
        self.str = ""
        self.counter = 0
        self.changed += 't'

    def move(self, dir=1): # -1 <= dir <= 1
        if self.move_allowed == True:
        #if self.editing == False:
            prev = self.counter
            self.counter += dir
            if self.counter >= len(self.str) + len(self.space):
                self.counter = 0
            elif self.counter < 0:
                if prev >= 0:
                    self.counter = len(self.str) + len(self.space);
            self.changed += 't'

    def move_allow(self, allow=None):
        """Allow/disallow Textarea movement

        allow - boolean value determining Textarea movement
                (if None returns current state without any change)
        """
        prev = self.move_allowed
        if allow is not None:
            self.move_allowed = allow
        return prev

    def edit(self, edit):
        """Turn editing mode on/off, move cursor

        action - what to do:
                 <bool> - start/end editing mode
                 <int> - set cursor position
        """
        if edit is None:
            return self.editing
        elif edit == False:
            print "edit mode disabled"
            self.editing = False
            self.str = self.prev_str
            self.counter = 0
            self.prev_str = ""
            self.prev_edit = 0
            self.cursor_v = False
            self.move_allowed = True
        elif edit == True:
            print "edit mode enabled"
            self.prev_str = self.str
            self.str = ""
            self.mode = 'l '
            self.editing = 0 #len(self.str) - 1 #????????
            self.prev_edit = 0
            self.counter = 0 #len(self.str) - self.size[0]
            self.cursor_v = True
            self.move_allowed = False
        elif self.editing != False: # <<<-----------------
            print "editing:", edit
            self.prev_edit = self.editing
            ln = len(self.str)
            w = self.size[0]
            if ln <= w:
                self.editing = edit
                self.changed +='c'
            else:
                if edit == ln - 1:
                    self.counter = ln - w
                    self.editing = w - 1
                    self.changed += 'tc'
                elif ln - edit < w / 2 + 1:
                    self.editing = w - (ln - edit)
                    self.changed += 'c'
                elif len - edit >= w / 2 + 1 and edit >= w / 2:
                    self.counter = edit - w / 2
                    self.changed += 't'
                elif edit < w / 2:
                    self.editing = edit
                    self.changed += 'c'
            print " * changed:", self.changed
            print " * counter:", self.counter
            print " * cursor:", self.editing

    def blink(self):
        self.cursor_v = not self.cursor_v
        self.changed = 'c'

    def update(self):
        if 't' in self.changed and self.editing == False:
            if len(self.str) <= self.size[0]:
                if len(self.mode) == 1:
                    self.mode += ' '
                if self.mode[0] == 'l':
                    self.font.put_text(self.surface, (0, 0), self.str.ljust(self.size[0], self.mode[1]), self._color)
                elif self.mode[0] == 'c':
                    self.font.put_text(self.surface, (0, 0), self.str.center(self.size[0], self.mode[1]), self._color)
                elif self.mode[0] == 'r':
                    self.font.put_text(self.surface, (0, 0), self.str.rjust(self.size[0], self.mode[1]), self._color)
            else:
                if self.size[1] == 1: # scroll message
                    if self.counter < 0:
                        current = 0
                    else:
                        current = self.counter
                    tmp = self.str + self.space + self.str + self.space
                    self.font.put_text(self.surface, (0, 0), tmp[current:self.size[0]+current],
                        self._color)
                else:
                    lines = list()
                    for line in self.str.split('\n'):
                        while len(line) > self.size[0]: # spliting line to fit in textarea
                            lines.append(line[:self.size[0]])
                            line = line[self.size[0]:]
                        else:
                            lines.append(line)
                    l = 0
                    while l in range(self.size[0]) and l < len(lines): # add not visible lines visibility <-----
                        self.font.put_text(self.surface, (0, self.font.height*l),
                                      lines[l], self._color)
                        l += 1
        elif 't' in self.changed and self.editing == True:
            self.font.put_text(self.surface, (0, 0), self.str[self.counter:self.counter+self.size[0]].ljust(self.size[0]), self._color)
        if 'c' in self.changed and self.editing != False:
            if self.prev_edit != self.editing:
                self.font.put_text(self.surface, (self.prev_edit*self.font.width, 0), self.str[self.prev_edit], self._color)
            if self.cursor_v == True:
                self.font.put_text(self.surface, (self.editing*self.font.width, 0), self.cursor_c, self._color)
            else:
                self.font.put_text(self.surface, (self.editing*self.font.width, 0), self.str[self.editing], self._color)
        if self.changed:
            pygame.display.get_surface().blit(self.surface, self.rect)
            pygame.display.update(self.rect)
        self.changed = ''

class Textareas(object):
    def __init__(self, fonts, data={}):
        """Initialize all Textarea classes

        fonts - Fonts object
        data - dict of name and lists of atributes
        """
        self.textareas = {}
        self.fonts = fonts
        for item in data.iteritems():
            self.add_new(*item)

    def add_new(self, name, data):
        """Add new Textarea

        name - Teaxtarea name
        data - list of atributes
        """
        if not self.textareas.has_key(name):
            self.textareas[name] = Textarea(font = self.fonts[data[-1]], *data[:-1])

    def move(self):
        """Move all Textareas"""
        for ta in self.textareas.itervalues():
            ta.move()

    def update(self):
        """Refresh all Textareas"""
        for ta in self.textareas.itervalues():
            ta.update()

    def __getitem__(self, name):
        return self.textareas[name]

    def __getattr__(self, name):
        if self.textareas.has_key(name):
            return self.textareas[name]
        else:
            raise AttributeError, name
