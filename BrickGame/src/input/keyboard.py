from pygame.locals import *

class Keyboard(object):
    def __init__(self, sys, ui):
        """Initialize Keyboard processing class

        sys, ui - dictionaries containing key sets
                  {(key, action): (function, modifiers)}
                   key: key activating selected function
                   action: KEYDOWN / KEYUP action
                   function: function called when key is pressed / released
                   modifiers: keys like CTRL, ALT, etc. holded to call function
                  sys key set is always active
                  ui key set is active only when Keyboard is in ui mode
                  (which is default)
        """
        self.sys_key_set = sys
        self.ui_key_set = ui
        self.game_key_set = {}
        self.input_mode = 'u' # u - UI, i - input, g - game
        self.str = ""
        self.cur = 0
        self.uppercase = {
            '`':'~', '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', '6':'^',
            '7':'&', '8':'*', '9':'(', '0':')', '-':'_', '=':'+', '[':'{',
            ']':'}', ';':':', '\'':'"', '\\':'|', ',':'<', '.':'>', '/':'?'
        }
        self.keypad = {
            K_KP_PERIOD:'.', K_KP_DIVIDE:'/', K_KP_MULTIPLY:'*',
            K_KP_MINUS:'-', K_KP_PLUS:'+'
        }

    def game_keys(self, game_keys):
        """Load game key set

        game_keys - dictionary similar to ui key set
                    game key set is activated when game_keys are loaded
        """
        if game_keys is not None:
            self.game_key_set = game_keys
        self.input_mode = 'g'

    def mode(self, mode=None):
        """Set Keyboard mode

        mode - one of None, 'u', 'g', 'i'
               None: nothing is changed, function returns current mode
               'u': UI mode, ui key set is activated
               'g': game mode, game key set is activated
               'i': input mode, ui and game key sets are disactivated to allow
                    user text input

        return - previous mode
        """
        prev = self.input_mode
        if mode is not None:
            self.input_mode = mode
        return prev

    def get_input(self):
        if self.input_mode == 'i':
            return (self.str, self.cur)
        else:
            return None

    def process(self, type, key, mod):
        """Process pressed key

        type - KEYDOWN or KEYUP
        key  - pressed key
        mod  - active modifiers while pressing key
        """
        try:
            a = self.sys_key_set[(key, type)]
            if a[1] == None or mod & a[1]:
                a[0]()
            else:
                raise KeyError
        except KeyError:
            try: # ui and game are not taking care of modifiers
                if self.input_mode == 'u':
                    self.ui_key_set[(key, type)]()
                elif self.input_mode == 'g':
                    self.game_key_set[(key, type)]()
                elif self.input_mode == 'i' and type == KEYDOWN and self.cur > 0:
                    if key == K_BACKSPACE and len(self.str) > 0:
                        self.str = self.str[:self.cur-1] + self.str[self.cur:]
                        self.cur -= 1
                    elif key == K_LEFT and self.cur > 0:
                        self.cur -= 1
                    elif key == K_RIGHT and self.cur <= len(self.str):
                        self.cur += 1
                    elif key == K_HOME:
                        self.cur = 0
                    elif key == K_END:
                        self.cur = len(self.str) + 1
                    elif K_SPACE <= key <= 125: # '{'
                        if mod & (KMOD_SHIFT | KMOD_CAPS):
                            if K_a <= key <= K_z:
                                c = chr(key).upper()
                            else:
                                c = self.uppercase[chr(key)]
                        else:
                             c = chr(key)
                        self.str = self.str[:self.cur] + c + self.str[self.cur:]
                        self.cur += 1
                    elif K_KP0 <= key <= K_KP_PLUS:
                        if mod & KMOD_NUM:
                            if K_KP0 <= key <= K_KP9:
                                c = chr(key - 208)
                            elif K_KP_PERIOD <= key <= K_KP_PLUS:
                                c = self.keypad[key]
                            self.str = self.str[:self.cur] + c + self.str[self.cur:]
                            self.cur += 1
                    print "str:", self.str, self.cur
            except KeyError:
                print "key:", type, key, mod