# BrickGame module

#from BrickGame import *
from pygame.locals import *

__all__ = ['Game', 'name', 'info']

name = 'Snake'
info = 'Simple snake game'

class Game(object):
    keys = {
        (K_UP, KEYDOWN): (lambda:self.move('u'), None),
        (K_DOWN, KEYDOWN): (lambda:self.move('d'), None),
        (K_LEFT, KEYDOWN): (lambda:self.move('l'), None),
        (K_RIGHT, KEYDOWN): (lambda:self.move('r'), None),
    }
    def __init__(self, screen, timers):
        self.screen = screen
        self.timers = timers
        self.snake = list()
        self.level = 0
        self.length = 3
        self.lives = 3
        
    def load_level(self):
        self.snake.extend([(5,9), (5,10), (5,11)])

    def move(self, direction):
        pass

    def step(self):
        pass
