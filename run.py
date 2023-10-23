# Write your code to expect a terminal of 80 characters wide and 24 rows high

class Char:
    '''
    Contains a list of characters from clearing the terminal screen
    to characters representing hits, misses, ships.
    '''
    _clear_screen = '\x9B3J\x9B;H\x9B0J'

    hit = '\u2731'
    miss = '-'
    ship = 'S'
    unknown = '\u25CF'

    def clear_screen():
        print(Char._clear_screen, end='')

# Constant for foreground colour initial setting
FG_COLOR = int(82)
# Constant for background colour initial setting
BG_COLOR = int(0)

class Color:
    '''
    Manages ASCII Select Graphic Rendition characters
    for selecting foreground and background colours.

    Manages 256 color for setting and retrieval.
    '''
    _template_background = '\x9B48;5;{}m'
    _template_foreground = '\x9B38;5;{}m'

    _current_background = ''
    _current_foreground = ''

    _current_background_int = 0
    _current_foreground_int = 0

    _reset = '\x9B0m'
    
    @staticmethod
    def get_background():
        return Color._current_background_int

    @staticmethod
    def get_foreground():
        return Color._current_foreground_int

    @staticmethod
    def reset():
        print(Color._reset, end='')

    @staticmethod
    def set_background(background_color):
        Color._current_background_int = int(background_color)
        Color._current_background = str(
            Color._template_background.format(
                int(background_color))
        )
        print(Color._current_background, end='')

    @staticmethod
    def set_foreground(foreground_color):
        Color._current_foreground_int = int(foreground_color)
        Color._current_foreground = str(
            Color._template_foreground.format(
                int(foreground_color))
        )
        print(Color._current_foreground, end='')

    @staticmethod
    def init():
        Color.reset()
        Color.set_background(BG_COLOR)
        Color.set_foreground(FG_COLOR)

class Title:
    '''
    Displaying the title of the game.
    '''
    _title_name = str('''
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
              | |_/ / (_| | |_| |_| |  __/\__ \ | | | | |_) \__ \\
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

test()
