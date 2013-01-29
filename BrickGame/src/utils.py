import pygame

def load_image(name, colorkey=None):
    """load an image

    This will load image and convert pixel format.
    If colorkey is -1 then transparent pixel will
    be top left pixel from image. Returns Surface.
    """
    #fullname = os.path.join('Images', name)
    try:
        image = pygame.image.load(name)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
    except pygame.error, message:
        print "Couldn't load image.", name
        raise SystemExit, message
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    #fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error, message:
        print "Couldn't load sound.", name
        raise SystemExit, message
    return sound