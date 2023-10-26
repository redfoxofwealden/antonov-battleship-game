# Write your code to expect a terminal of 80 characters wide and 24 rows high
def clear_screen(): 
        print('\x9B3J\x9B;H\x9B0J', end='')

class SGR:
    '''
    List of colors
    '''

    @staticmethod
    def black():
        return 0
    
    @staticmethod
    def red():
        return 1

    @staticmethod
    def green():
        return 2

    @staticmethod
    def yellow():
        return 3
    
    @staticmethod
    def blue():
        return 4

    @staticmethod
    def magenta():
        return 5

    @staticmethod
    def cyan():
        return 6

    @staticmethod
    def lt_grey():
        return 7

    @staticmethod
    def grey():
        return 8

    @staticmethod
    def lt_red():
        return 9

    @staticmethod
    def lt_green():
        return 10
    
    @staticmethod
    def lt_yellow():
        return 11
    
    @staticmethod
    def lt_blue():
        return 12
    
    @staticmethod
    def lt_magenta():
        return 13
    
    @staticmethod
    def lt_cyan():
        return 14

    @staticmethod
    def white():
        return 15

    @staticmethod
    def char(str_char_arg, fg_clr):
        fg_clr_prm = (int(fg_clr) + 30) if int(fg_clr) < 8 else (int(fg_clr) + 82)
        fg_chars = str(f'\x9B{fg_clr_prm}m')
        return str(fg_chars + str(str_char_arg))

    @staticmethod
    def print(str_argument, fg_clr, bg_clr=None, endline='\n'):
        fg_clr_prm = (int(fg_clr) + 30) if int(fg_clr) < 8 else (int(fg_clr) + 82)
        fg_chars = str(f'\x9B{fg_clr_prm}m')
        fg_def_chars = str('\x9B39m')

        if bg_clr is not None:
            bg_clr_prm = (int(bg_clr) + 40) if int(bg_clr) < 8 else (int(bg_clr) + 92)
            bg_chars = str(f'\x9B{bg_clr_prm}m')
            bg_def_chars = str('\x9B49m')
        else:
            bg_chars = ''
            bg_def_chars = ''

        print(fg_chars + bg_chars, end='')
        print(str(str_argument), end='')
        print(fg_def_chars + bg_def_chars, end=endline)

BOARD_OBJ_BLANK = 'Blank'
BOARD_OBJ_SHIP = 'Ship'
BOARD_OBJ_MISS = 'Miss'
BOARD_OBJ_HIT = 'Hit'

class Board:
    '''
    Process players board position
    '''
    def __init__(self, name, reveal_position):
        self.name = str(name)
        self.reveal_position = bool(reveal_position)

    _BOARD_OBJECTS = (
        {
            'id': 0,
            'label': BOARD_OBJ_BLANK,
            'char': SGR.char('\u25CF', SGR.lt_grey())
        },
        {
            'id': 1,
            'label': BOARD_OBJ_SHIP,
            'char': SGR.char('S', SGR.white())
        },
        {
            'id': 2,
            'label': BOARD_OBJ_MISS,
            'char': ' '
        },
        {
            'id': 3,
            'label': BOARD_OBJ_HIT,
            'char': SGR.char('\u2731', SGR.red())
        }
    )

    _board_size = 0
    _num_of_ships = 0

    @staticmethod
    def set_board_size(size_board):
        Board._board_size = int(size_board)
        Board._num_of_ships = int(Board._board_size * Board._board_size / 5)
    
    @staticmethod
    def user_select_board_size():
        clear_screen()
        board_size_question = str(
            'What size of board do you want to play with?'
            '\nEnter one of the following choices:-'
            '\n'
            '\n 5 for 5 by 5 board with 5 ships;'
            '\n 6 for 6 by 6 board with 7 ships;'
            '\n 7 for 7 by 7 board with 9 ships;'
            '\n 8 for 8 by 8 board with 12 ships.'
        )
        SGR.print(board_size_question, SGR.yellow())

        while True:
            try:
                user_board_size = input('\nEnter your choice:\n')
                if int(user_board_size) > 4 and int(user_board_size) < 9:
                    Board.set_board_size(int(user_board_size))
                    break
                else:
                    raise ValueError
            
            except ValueError:
                print()
                SGR.print(' Invalid Input! Make sure that you enter one ', SGR.white(), SGR.red())
                SGR.print(' of these options: 5, 6, 7 or 8              ', SGR.white(), SGR.red())

class Human(Board):
    '''
    Human player
    '''
    def __init__(self, name):
        super().__init__(self, name, True)

class Computer(Board):
    '''
    Computer player
    '''
    def __init__(self):
        super().__init__(self, 'Computer', False)

        
class TitleMenu:
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
    def display_title():
        SGR.print(TitleMenu._title_name, SGR.lt_green())

    @staticmethod
    def display_menu():
        SGR.print(str('Enter I for instructions,').center(80), SGR.yellow())
        SGR.print(str('   or P to play the game.').center(80), SGR.yellow())
 
    @staticmethod
    def input_user_response():
        while True:
            user_input = str(input('\nEnter your option:\n')).lower()
            if user_input == 'i' or user_input == 'p' or user_input == 'q':
                return user_input
            else:
                print()
                SGR.print(' Invalid Input! Make sure you enter one of these options: ', SGR.white(), SGR.red())
                SGR.print(' I for instructions, or P to play.                        ', SGR.white(), SGR.red())
    
    @staticmethod
    def run():
        clear_screen()
        TitleMenu.display_title()
        TitleMenu.display_menu()
        user_response = TitleMenu.input_user_response()
        return user_response

def main():
    while True:
        user_option_select = TitleMenu.run()
        if user_option_select == 'i':
            print('Feature not yet implemented')
            input('Press enter to continue:\n')

        elif user_option_select == 'p':
            print('Feature not yet implemented')
            input('Press enter to continue:\n')

        elif user_option_select == 'q':
            return

def test():
    while True:
        clear_screen()

        print('Select one of the following:')
        print('1. run main()')
        print('2. rum test()')
        print('q to quit.')
        user_choice = input('Enter choice\n')
        if user_choice == '1':
            main()
        elif user_choice == '2':
            Board.user_select_board_size()
        elif user_choice == 'q':
            print('Done')
            break

test()
