import os.path
#!/usr/bin/env python
#
# Brick game
# platform for simple games
#
# Released under the GNU General Public License

VERSION = "0.3"

try:
    import os
    import random
    import re
    import string
    import sys

    import pygame
    from pygame.locals import *

    import data_make
    import imgs
    from screen import Screen
    from input import Keyboard
    from timer import Timers
except ImportError, err:
    print "Couldn't load module.", err
    sys.exit(2)

class Modules(object): # TODO make this class works
    def __init__(self, path, screen):
        self.screen = screen
        self.current = None
        # adding game modules search path
        sys.path.append(os.path.abspath(path))
        # loading modules
        print "loading modules"+'<'*10
        files = os.listdir(path)
        mod = re.compile("_game\.py$", re.IGNORECASE)
        files = filter(mod.search, files)
        print "files:", files
        moduleNames = map(lambda f: os.path.splitext(f)[0], files)
        modules = map(__import__, moduleNames)
        print "modules:", modules
        self.modules = filter(self._test, modules)
        print "filtered modules:", self.modules
        
    def _test(self, module):
        try:
            if module.name and module.info and module.Game:
                if issubclass(module.Game, object):
                    return True
        except (AttributeError, TypeError):
            pass
        return False

    def list(self):
        pass

    def step(self):
        try:
            self.module.step()
        except AttributeError:
            pass

class Interface(object):
    def __init__(self, screen):
        self.screen = screen
        self._score = 0
        self._level = 0
        self._speed = False

    def __getattr__(self, name):
        if self._displays.has_key(name):
            return self._displays[name]
        else:
            raise AttributeError, name

class UI(object):
    def __init__(self, screen):
        self.screen = screen
        self.screen.textareas.main.align('c')
        self.screen.textareas.main.put("> Brick Game <")
        self.screen.textareas.score.align('r0')
        self.screen.textareas.score.put("0")
        self.screen.indicators.score.state = 1
        self.screen.displays.main.clear(0)
        self.screen.displays.main.visibility(True, 0)
        i = 0
        for c in range(0x33, 0xcc, 0x08):
            self.screen.displays.main.fill((0, i, 10, 1), 0x81, c << 8, 0)
            i += 1
        self.screen.displays.main.put_text((2,5,5,1), 'Brick', 0xffffff, 0)
        self.screen.displays.main.put_text((4,6,4,1), 'Game', 0xffffff, 0)
        self.screen.displays.main.put_text((0,8,10,1), 'written in', 0xffffff, 0)
        self.screen.displays.main.put_text((1,9,8,1), 'Python &', 0xffffff, 0)
        self.screen.displays.main.put_text((2,10,6,1), 'Pygame', 0xffffff, 0)

class GI(object):
    """Game Interface

    """
    def __init__(self):
        pass

class Game(object):
    def __init__(self):
        sys.path.append(os.path.abspath('.'))
        config = data_make.load()
        self.screen = Screen(config)
        try:
            self.modules = Modules('Games', self.screen)
        except:
            pass
        #self.interface = Interface(self.screen)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        self.mouse_focus = False
        self._pause = False
        self._fps = 120 #2*2*2*3*5
        self._running = True
        self.timers = Timers(self._fps)
        self.timers.add_new("ta_move", self.screen.textareas.move, 10, type='s')
        self.timers.add_new("pause", lambda:self.screen.indicators.state('pause'), 2, None, 's')
        #self.timers.add_new("focus_test", self.focusTest, 2, type='s')
        #print self.timers.listType('s')
        sys_keys = {
            #(key, KEYUP/KEYDOWN): (func, modifiers expected, modifiers allowed)
            (K_p, KEYDOWN): (self.pause, KMOD_CTRL),
            (K_i, KEYDOWN): (self.edit, KMOD_CTRL),
            #(K_e, KEYDOWN): (lambda:self.screen.textareas[0].edit(not bool(self.screen.textareas[0].edit())), KMOD_CTRL),
            (K_q, KEYDOWN): (self.stop, KMOD_CTRL),
            (K_r, KEYDOWN): (lambda:self.screen.displays.main.fill((random.randint(0,8), random.randint(0, 18), random.randint(1,10), random.randint(1, 20)), 0x81, random.randint(0, 0xffffff), 0), None),
            (K_t, KEYDOWN): (lambda:self.screen.displays.main.put_text((random.randint(0,8), random.randint(0, 18), random.randint(1,10), random.randint(1, 20)), 'test', random.randint(0, 0xffffff), 0), None),
            (K_l, KEYDOWN): (self.test, KMOD_CTRL),
            (K_c, KEYDOWN): (self.compile_conf, KMOD_CTRL),
        }
        self.keyboard = Keyboard(sys_keys, {})
        self.rects = (
        #    (self.screen.textarea1, Rect(self.screen.textarea1)),
        )
        self.clicked = -1
        self.pos = [0,0]
        self.editing = False # <<<<<<<<<<<
        #self.test()
        self.ui = UI(self.screen)
        self.run()

    def fps(self, fps = None):
        """set frame rate

        fps is frame rate value
        Return old frame rate
        """
        tmp = self._fps
        if fps:
            self._fps = fps
        return tmp

    def mouse(self, event):
        for i in  range(len(self.rects)):
            if self.rects[i][1].collidepoint(*event.pos):
                try:
                    if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP):
                        if event.button == 1:
                            self.rects[i][0].on_mouse_click(event.pos)
                    elif event.type == MOUSEMOTION:
                        if event.buttons[0]:
                            print (event.pos[0]-self.pos[0], event.pos[1]-self.pos[1])
                            self.rects[i][0].on_mouse_move(event.pos,
                                (event.pos[0]-self.pos[0], event.pos[1]-self.pos[1]))
                except AttributeError:
                    pass
                else:
                    self.clicked = i
                    break

    def test(self):
        try:
            test = __import__('test')
            test.test(self.screen)
        except:
            pass

    def compile_conf(self):
        try:
            cfg = __import__('config')
            data_make.pack(cfg.config, 'config.dat')
            print 'new config.dat created'
        except ImportError:
            print 'No config.py file found'

    def pause(self, state=None):
        if state is None:
            self._pause = not self._pause
        else:
            self._pause = bool(state)
        if self._pause == True:
            self.screen.indicators.state('pause', True)
            self.timers.unpause("pause")
        else:
            self.timers.pause("pause")
            self.screen.indicators.state('pause', False)

    def stop(self):
        self._running = False

    def edit(self, action=''):
        if action == True and self.editing == False:
            print "Input mode"+'<'*10
            self.editing = True
            self.keyboard.mode('i', self.edit)
            self.screen.textareas.main.edit(True)
            self.timers.pause("ta_move")
            #self.timers.add_new("ta_blink", self.screen.textareas.main.blink, 3, type='s')
        elif action == False and self.editing == True:
            pass
        else:
            print "editing:", action
            #self.screen.textareas.main.replace(str[0]+' ')
            self.screen.textareas.main.edit(str[1])

    def run(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == ACTIVEEVENT:
                    if event.state in (2, 6): # APPINPUTFOCUS and APPACTIVE
                        if event.gain == 0:
                            #prev_fps, self._fps = self._fps, 2
                            #self.timers.add_new(lambda:self.screen.indicators.state('pause'), 2)
                            self.prev_fps, self._fps = self._fps, 10
                            self.timers.add_new("pause", lambda:self.screen.indicators.state('pause'), 10, 0, 's')
                            print ">> Lost input focus <<"
                        else:
                            self._fps = self.prev_fps
                            self.timers.add_new("pause", lambda:self.screen.indicators.state('pause'), 10, None, 's')
                            self.screen.indicators.state('pause', False)
                            print ">> Gain input focus <<"
                elif event.type in (KEYDOWN, KEYUP):
                    self.keyboard.process(event.type, event.key, event.mod)
            self.screen.update()
            self.timers.tick()
            self.clock.tick(self._fps)

if __name__ == '__main__':
    try:
        cfg = __import__('config')
        data_make.pack(cfg.config)
        print 'new_config.dat created'
    except ImportError:
        pass
    g = Game()