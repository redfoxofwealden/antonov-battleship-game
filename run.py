# Write your code to expect a terminal of 80 characters wide and 24 rows high

def clear_screen(): 
        print('\x9B3J\x9B;H\x9B0J', end='')

class SGR:
    '''
    List of colors
    '''

    @staticmethod
    def bg_blue():
        return str('\x9B44m')
    
    @staticmethod
    def bg_red():
        return str('\x9B41m')
    
    @staticmethod
    def fg_green():
        return str('\x9B32m')

    @staticmethod
    def fg_lt_green():
        return str('\x9B92m')

    @staticmethod
    def fg_red():
        return str('\x9B31m')

    @staticmethod
    def fg_lt_red():
        return str('\x9B91m')

    @staticmethod
    def fg_white():
        return str('\x9B97m')

    @staticmethod
    def fg_yellow():
        return str('\x9B33m')

    @staticmethod
    def fg_lt_yellow():
        return str('\x9B93m')

    @staticmethod
    def reset():
        return str('\x9B0m')

    @staticmethod
    def bg_default():
        return str('\x9B49m')

    @staticmethod
    def fg_default():
        return str('\x9B39m')

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
            'char': str(SGR.fg_white() + '\u25CF')
        },
        {
            'id': 1,
            'label': BOARD_OBJ_SHIP,
            'char': str(SGR.fg_white() + 'S')
        },
        {
            'id': 2,
            'label': BOARD_OBJ_MISS,
            'char': str(SGR.fg_white() + ' ')
        },
        {
            'id': 3,
            'label': BOARD_OBJ_HIT,
            'char': str(SGR.fg_red() + '\u2731')
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
        while True:
            try:
                print(
                    SGR.fg_yellow() +
                    'Enter the following choices for the'
                    '\nsize of board that you want:'
                    '\n 5 for 5 by 5 board;'
                    '\n 6 for 6 by 6 board;'
                    '\n 7 for 7 by 7 board;'
                    '\n 8 for 8 by 8 board.' +
                    SGR.fg_default()
                )
                user_board_size = input('\nEnter your choice for the size of board:\n')
                if int(user_board_size) > 4 and int(user_board_size) < 9:
                    Board.set_board_size(int(user_board_size))
                    break
                else:
                    raise ValueError
            
            except ValueError:
                print()
                print(
                    SGR.bg_red() + SGR.fg_white() +
                    ' Invalid Input! Make sure that you enter the '
                    + SGR.reset()
                )
                print(
                    SGR.bg_red() + SGR.fg_white() +
                    ' size of board: from 5 to 8                  '
                    + SGR.reset()
                )
                print()

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
    _title_name = str(SGR.fg_lt_green() + r'''
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
    ''' + SGR.fg_default())
    
    @staticmethod
    def display_title():
        print(TitleMenu._title_name)

    @staticmethod
    def display_menu():
        print(SGR.fg_yellow() + str('Enter I for instructions,').center(80))
        print(str('   or P to play the game.').center(80) + SGR.fg_default())
 
    @staticmethod
    def input_user_response():
        while True:
            user_input = str(input('\nEnter your option:\n')).lower()
            if user_input == 'i' or user_input == 'p' or user_input == 'q':
                return user_input
            else:
                print(
                    SGR.fg_white() + SGR.bg_red() +
                    ' Invalid Input! Make sure you enter one of these options: ' +
                    SGR.reset()
                )
                print(
                    SGR.fg_white() + SGR.bg_red() +
                    ' I for instructions, or P to play.                        ' +
                    SGR.reset()
                )
    
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
    Board.user_select_board_size()
    print(Board._board_size)
    print(Board._num_of_ships)

main()
