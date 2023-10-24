# Write your code to expect a terminal of 80 characters wide and 24 rows high

class Char:
    '''
    Contains a list of characters from clearing the terminal screen
    to characters representing hits, misses, ships.
    '''
    _clear_screen = '\x9B3J\x9B;H\x9B0J'

    HIT = '\u2731'
    MISS = '-'
    SHIP = 'S'
    UNKNOWN = '\u25CF'

    def clear_screen():
        print(Char._clear_screen, end='')

class Color:
    '''
    Manages ASCII Select Graphic Rendition characters
    for selecting foreground and background colours.

    Manages 256 color for setting and retrieval.
    '''

    _FOREGROUND_COLOR = int(82) # light green
    _BACKGROUND_COLOR = int(0)  # black

    _TEMPLATE_BACKGROUND = '\x9B48;5;{}m'
    _TEMPLATE_FOREGROUND = '\x9B38;5;{}m'
    _RESET = '\x9B0m'

    _current_background = ''
    _current_foreground = ''
    _current_background_int = -1
    _current_foreground_int = -1
    
    @staticmethod
    def format(string, fg_color=None, bg_color=None):
        fg_string = ''
        bg_string = ''

        if fg_color is not None:
            fg_string = Color._TEMPLATE_FOREGROUND.format(int(fg_color))
            
        if bg_color is not None:
            bg_string = Color._TEMPLATE_BACKGROUND.format(int(bg_color))
        
        format_string = bg_string + fg_string + string
        format_string += Color._current_background
        format_string += Color._current_foreground

        return str(format_string)
    
    @staticmethod
    def get_background():
        return Color._current_background_int

    @staticmethod
    def get_foreground():
        return Color._current_foreground_int

    @staticmethod
    def reset():
        '''
        Restore terminal colors to its system defaults
        '''
        print(Color._RESET, end='')
        Color._current_background = ''
        Color._current_foreground = ''
        Color._current_background_int = -1
        Color._current_foreground_int = -1

    @staticmethod
    def restore():
        if Color._current_background != '':
            print(Color._current_background, end='')
               
        if Color._current_foreground != '':
            print(Color._current_foreground, end='')

    @staticmethod
    def set_background(background_color):
        Color._current_background_int = int(background_color)
        Color._current_background = str(
            Color._TEMPLATE_BACKGROUND.format(
                int(background_color))
        )
        print(Color._current_background, end='')

    @staticmethod
    def set_foreground(foreground_color):
        Color._current_foreground_int = int(foreground_color)
        Color._current_foreground = str(
            Color._TEMPLATE_FOREGROUND.format(
                int(foreground_color))
        )
        print(Color._current_foreground, end='')
        return Color

    @staticmethod
    def init():
        Color.reset()
        Color.set_background(Color._BACKGROUND_COLOR)
        Color.set_foreground(Color._FOREGROUND_COLOR)

class Title:
    '''
    Displaying the title of the game.
    '''
    _title_name = str(r'''
                      ___        _                         
                     / _ \      | |                        
                    / /_\ \_ __ | |_ ___  _ __   _____   __
                    |  _  | '_ \| __/ _ \| '_ \ / _ \ \ / /
                    | | | | | | | || (_) | | | | (_) \ V / 
                    \_| |_/_| |_|\__\___/|_| |_|\___/ \_/  
                                                           
                                                           
              ______       _   _   _           _     _           
              | ___ \     | | | | | |         | |   (_)          
              | |_/ / __ _| |_| |_| | ___  ___| |__  _ _ __  ___ 
              | ___ \/ _` | __| __| |/ _ \/ __| '_ \| | '_ \/ __|
              | |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) \__ \
              \____/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/|___/
                                                      | |        
                                                      |_|          
    ''')
    
    @staticmethod
    def display():
        print(Title._title_name)

def test():
    Color.init()
    Char.clear_screen()
    Title.display()

    print(Color.format(' This is red on white background ', 1, 15))

test()
