import pygame

class Display(object): # FIXME rendering objects on layers
    """Multi layer display

    class

    layers order:
                  screen
        layer  0 -------- (system layer, not for game use)
           nr  1 --------
               2 --------

    colors 0x000000 and 0xfeeffe can't be used
    """
    def __init__(self, position, size, default_color, layers, image, font):
        """Initialize display

        position - position on the screen in pixels (x, y)
        size - size in chars (w, h)
        default_color - color used while filling display when no color specified
        layers - amount of display layers
        image - Screen background image
        font - Font class object
        bg - Screen background image
        """
        self.size = size
        self.def_color = default_color
        self.font = font
        self.layers = layers
        self.rect = pygame.Rect(position, (self.size[0]*self.font.width,
                                           self.size[1]*self.font.height))
        print "Display self.rect", self.rect
        self.image = image.subsurface(self.rect)
        self.visible = [False]*self.layers
        self.surface = pygame.Surface(self.rect.size)
        self.surface.convert()
        #self.surface.fill(0x000000)
        self.surface.set_colorkey(0x000000)
        self.dispRect = pygame.Rect((0, 0), self.size)
        self.buffer = []
        for l in range(self.layers):
            s = pygame.Surface(self.rect.size)
            s.convert()
            s.fill(0xfeeffe)
            s.set_colorkey(0xfeeffe)
            self.buffer.append(s)
        self.changed = []

    def _layers_p(self, layers):
        if layers is None:
            layers = range(self.layers)
        else:
            try:
                layers[0]
            except TypeError:
                layers = [layers]
            except IndexError:
                return None
        return layers

    def clear(self, layers=None):
        """Clear layer(s)

        layer - layer number (default all layers)
        """
        print "clearing" + '<' * 10
        layers = self._layers_p(layers)
        if layers is not None:
            changed = 0
            for layer in layers:
                self.buffer[layer].fill(0xfeeffe)
                #self.visible[layer] = False
                print "clearing layer", layer
                if self.visible[layer]:
                    changed += 1
            if changed > 0:
                self.changed.append(self.dispRect)

    def visibility(self, vis, layers=None):
        """Change layer(s) visibility status

        vis - layer visibility
        layers - layer to change (default all layers)
        """
        layers = self._layers_p(layers)
        if layers is not None:
            changed = 0
            vis = bool(vis)
            for layer in layers:
                if self.visible[layer] != vis:
                    self.visible[layer] = vis
                    changed += 1
            if changed > 0:
                self.changed.append(self.dispRect)

    def fill(self, rect, char, color=None, layer=None):
        """Fill part of display

        rect - pygame recstyle object counted in chars
        char - index of font char (None -> transparent)
        color - filling color (default default_color)
        layer - layer number (default lowermost)
        """
        print "filling" + '<' * 10
        rect = pygame.Rect(rect)
        print rect
        rect = rect.clip(self.dispRect)
        print "after clip:", rect
        if layer is None:
            layer = self.layers - 1
        if self.visible[layer]:
            self.changed.append(rect)
            print "filling layer", layer, rect
        if char is None:
            self.buffer[layer].fill(0xfeeffe, self.convert_rect(rect))
        else:
            if type(char) == type(str()):
                char = ord(char)
            if color is None:
                color = self.def_color
            r = self.convert_rect(rect)
            #tmp_s = pygame.Surface((r.width, self.font.height))
            #tmp_s.set_colorkey(0x000000)
            #self.buffer[layer].blit(self.image, r.topleft, r)
            #tmp_s.blit(self.buffer[layerS], (0,0), r)
            for i in range(rect.bottom-rect.top):
                self.font.put(self.buffer[layer], (r.left, r.top+i*self.font.height), (char,)*rect.width, color)
                #self.font.put(tmp_s, (0, 0), (char,)*rect.width, color)
                #self.buffer[layer].blit(tmp_s, (r.left, r.top+i*self.font.height))
                #print " > ({3}) fill with: {0} color: 0x{1:06x} at: {2}".format((char,)*rect.width, color, (r.left, r.top+i*self.font.height), i)
                print " > (%d) fill with: '%s' color: 0x%06x at: %s" % (i, (char,)*rect.width, color, (r.left, r.top+i*self.font.height))

    def copy(self, rect, pos, layerS=None, layerD=None):
        """Copy part of display to another place

        rect - pygame recstyle object counted in chars
        pos - destination position counted in chars
        layerS - source layer (default lowermost)
        layerD - destination layer (default source layer)
        """
        rect = pygame.Rect(rect)
        nrect = pygame.Rect(rect)
        nrect.topleft = pos
        nrect.clamp_ip(self.dispRect)
        if layerS is None:
            layerS = self.layers - 1
        if layerD is None:
            layerD = layerS
        if self.visible[layerD]:
            self.changed.append(nrect)
        r = self.convert_rect(rect)
        tmp_s = pygame.Surface(r.size)
        tmp_s.convert()
        tmp_s.set_colorkey(0xfeeffe)
        tmp_s.blit(self.buffer[layerS], (0,0), r)
        r = self.convert_rect(nrect)
        self.buffer[layerD].blit(tmp_s, r.topleft)

    def put_text(self, rect, text, color=None, layer=None):
        """Put text on display

        rect - pygame recstyle object counted in chars defining textarea
        text - text to put
        color - text color (default default_color)
        layer - layer number (default lowermost)
        """
        print "writting" + '<' * 10
        rect = pygame.Rect(rect)
        rect = rect.clip(self.dispRect)
        if layer is None:
            layer = self.layers - 1
        if self.visible[layer]:
            self.changed.append(rect)
            print "writting layer", layer, rect
        if color is None:
            color = self.def_color
        lines = 0
        for line in text.split('\n'):
            print " > line: '%s'" % line
            print " > spliting line: %d lines" % (len(line) / rect.width + 1)
            for i in range(len(line) / rect.width + 1):
                print "  * step:", i
                if lines >= rect.height:
                    print "  ! lines(%d) >= rect.height(%d) exiting func" % (lines, rect.height)
                    return
                r = self.convert_rect(rect)
                self.font.put_text(self.buffer[layer], (r.left, r.top+lines*self.font.height), line[i*rect.width:(i+1)*rect.width], color)
                #print "  * put text: '{0}' color: 0x{1:06x} at: {2}".format(line[i*rect.width:(i+1)*rect.width], color, (r.left, r.top+i*self.font.height))
                print "  * put text: '%s' color: 0x%06x at: %s" % (line[i*rect.width:(i+1)*rect.width], color, (r.left, r.top+i*self.font.height))
                lines += 1

    def map_data(self, rect, data, color=None, layer=None):
        """Put data on display

        rect - pygame recstyle object counted in chars defining textarea
        data - 2 dimensional list containing char codes
        color - data color (default default_color)
        layer - layer number (default lowermost)
        """
        print "mapping data" + '<' * 10
        rect = pygame.Rect(rect)
        rect = rect.clip(self.dispRect)
        if layer is None:
            layer = self.layers - 1
        if self.visible[layer]:
            self.changed.append(rect)
            print "writting layer", layer, rect
        if color is None:
            color = self.def_color
        r = self.convert_rect(rect)
        #tmp_st = pygame.Surface(r.size)
        #tmp_st.set_colorkey(0x000000)
        #tmp_st.fill(0xfeeffe)
        #tmp_si = pygame.Surface(r.size)
        #tmp_si.set_colorkey(0xfeeffe)
        #self.buffer[layer].blit(self.image, r.topleft, r)
        #tmp_si.blit(self.image, (0, 0), r)
        for y in range(rect.height):
            self.font.put(self.buffer[layer], (r.left, r.top+y*self.font.height), data[y][:rect.width], color)
            #self.font.put(tmp_st, (0, y*self.font.height), data[y][:rect.width], color)
            print "  * ({3}) put: {0} color: 0x{1:06x} at: {2}".format(data[y][:rect.width], color, (r.left, r.top+y*self.font.height), y)
        #tmp_si.blit(tmp_st, (0, 0))
        #self.buffer[layer].blit(tmp_si, r.topleft)

    def elem(self, el):
        """Generate ASCII code from graphic element index"""
        return chr(el + 0x80)

    def convert_rect(self, rect):
        """Convert rect counted in chars to rect counted in pixels"""
        return pygame.Rect(rect.left * self.font.width,
                           rect.top * self.font.height,
                           rect.width * self.font.width,
                           rect.height * self.font.height)

    def update(self):
        """Refresh display"""
        if len(self.changed) > 0:
            print "updating"+'<'*10
            if len(self.changed) == 1:
                changed = self.changed
            else:
                changed = []
                print "processing rects"
                while len(self.changed) > 0:
                    print "len(self.changed):", len(self.changed)
                    rect = self.changed[0]
                    print " * del first key:", rect
                    del self.changed[0]
                    cl = rect.collidelistall(self.changed)
                    print " * colide list:", cl
                    if len(cl) > 0:
                        changed.append(rect.unionall([self.changed[r] for r in cl]))
                        print " * changed after union:", changed
                        for r in sorted(cl, reverse = True):
                            print "  > del key:", r, ",", self.changed[r]
                            del self.changed[r]
                    else:
                        changed.append(rect)
                        print " * changed without union:", changed
                else:
                    print " * loop end"
            print "changed:", changed
            for ch in changed:
                rect = self.convert_rect(ch)
                #rect = pygame.Rect(0,0,0,0).unionall([r for r,l in self.changed])
                #rect = self.convert_rect(rect)
                print "update Display:", rect
                for l in reversed(range(self.layers)):
                    print " > layer", l
                    if self.visible[l] == True:
                        print "  * visible, refresh rect:", rect
                        self.surface.fill(0x000000, rect)
                        self.surface.blit(self.buffer[l], rect.topleft, rect)
                        #self.surface.fill(random.randint(0, 0xffffff), rect)
                pygame.display.get_surface().blit(self.image, self.rect.move(rect.topleft), rect)
                pygame.display.get_surface().blit(self.surface, self.rect.move(rect.topleft), rect) #FIXME update part of screen
                pygame.display.update(self.rect)
            self.changed = []

class Displays(object):
    def __init__(self, image, fonts, data = {}):
        """Initialize all Display classes

        image - Screen background image
        fonts - Fonts object
        data - list of lists of atributes
        """
        self._displays = {}
        self._image = image
        self._fonts = fonts
        for item in data.iteritems():
            self.add_new(*item)

    def add_new(self, name, data):
        """Add new Display

        data - list of atributes
        """
        self._displays[name] = Display(image=self._image, font=self._fonts[data[-1]], *data[:-1])

    def update(self):
        """Refresh all Displays"""
        for disp in self._displays.itervalues():
            disp.update()

    def __getitem__(self, name):
        return self._displays[name]

    def __getattr__(self, name):
        if self._displays.has_key(name):
            return self._displays[name]
        else:
            raise AttributeError, name
