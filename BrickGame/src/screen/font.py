import os

from .utils import load_image

class Font(object):
    def __init__(self, filename, width, height, colorkey, add_chars=0):
        """Initialize bitmap font class

        filename - filename of image with chars
        width, height - width, height of char in pixels
        colorkey - color used when drawing font
        add_chars - aditional characters

        Image must be organised in 16x6 matrix of chars.
        When you specified add_chars height of matrix can be
        larger (>=7) to store additional characters
        """
        self.font = load_image(filename, colorkey)[0]
        self.width, self.height = width, height
        self.additional_chars = add_chars

    def put_text(self, surface, pos, text, color):
        """Put text on surface

        surface - destination surface
        pos - position of text in pixels
        text - putting text
        color - text color
        """
        if type(text) != type(str()):
            text = str(text)
        data = map(ord, text)
        a = 0
        surface.fill(color, (pos[0], pos[1], len(data)*self.width, self.height))
        for c in data:
            if c < 32 or c > 127 + self.additional_chars:
                c = 32
            c -= 32
            c2 = c % 16
            c1 = c / 16
            clip = (c2 * self.width, c1 * self.height, self.width, self.height)
            surface.blit(self.font, (pos[0]+a*self.width, pos[1]), clip)
            a += 1

    def put(self, surface, pos, data, color):
        """Put data on surface

        surface - destination surface
        pos - position of text in pixels
        data - iterable object containing char codes
        color - text color
        """
        if type(data) == type(str()):
            data = map(ord, data)
        a = 0
        for c in data:
            if c is not None or 32 <= c <= (127 + self.additional_chars):
                c -= 32
                c2 = c % 16
                c1 = c / 16
                clip = (c2 * self.width, c1 * self.height, self.width, self.height)
                surface.fill(color, (pos[0]+a*self.width, pos[1], self.width, self.height))
                surface.blit(self.font, (pos[0]+a*self.width, pos[1]), clip)
            a += 1
        #pygame.display.update((self.data[item][0][0], self.data[item][0][1],
        #    len(self.data[item][1])*self.width, self.height))

class Fonts(object):
    def __init__(self, path, data = {}):
        self._fonts = {}
        self._path = path
        for item in data.iteritems():
            self.add_new(*item)

    def add_new(self, name, data):
        self._fonts[name] = Font(os.path.join(self._path, data[0]), *data[1:])

    def update(self):
        for font in self._fonts:
            font.update()

    def __getitem__(self, name):
        return self._fonts[name]

    def __getattr__(self, name):
        if self._fonts.has_key(name):
            return self._fonts[name]
        else:
            raise AttributeError, name
