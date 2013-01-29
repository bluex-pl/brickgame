"""Main screen package class

Set up pygame window and all screen components
"""
import pygame
import os

from font import Fonts
from textarea import Textareas
from display import Displays
from indicator import Indicators
from .utils import load_image

class Screen(object):
    """Screen base class.

    """
    def __init__(self, config):
        pygame.display.init()
        icon = pygame.image.load(os.path.join(config['paths']['images'],
                                              config['screen']['icon'][0]))
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode(config['screen']['size'])
        pygame.display.set_caption('BrickGame', 'BGame')
        self.image = load_image(os.path.join(config['paths']['images'],
                                             config['screen']['image'][0]),
                                config['screen']['image'][1])[0]
        screen.blit(self.image, (0, 0))
        pygame.display.flip()
        self.fonts = Fonts(config['paths']['fonts'], config['fonts'])
        self.textareas = Textareas(self.fonts, config['textareas'])
        self.displays = Displays(self.image, self.fonts, config['displays'])
        self.indicators = Indicators(self.image,
                                     config['indicators'].pop('bg_color'),
                                     config['indicators'])

    def __del__(self):
        pygame.display.quit()

    def destroy(self):
        pygame.display.quit()

    def update(self):
        """Refresh all used objects"""
        self.indicators.update()
        self.textareas.update()
        self.displays.update()
