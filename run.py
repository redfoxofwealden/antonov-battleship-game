# Write your code to expect a terminal of 80 characters wide and 24 rows high
import random

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

class Board:
    '''
    Board class
    '''

    _board_size = 5
    _number_of_ships = 5

    @staticmethod
    def _set_board_size(size_board):
        Board._board_size = int(size_board)
        Board._number_of_ships = int(Board._board_size * Board._board_size / 5)
    
    @staticmethod
    def player_select_board_size():
        clear_screen()        
        SGR.print(str(
            'What size of board do you want to play with?'
            '\nEnter one of the following choices:-'
            '\n'
            '\n 5 for 5 by 5 board with 5 ships;'
            '\n 6 for 6 by 6 board with 7 ships;'
            '\n 7 for 7 by 7 board with 9 ships;'
            '\n 8 for 8 by 8 board with 12 ships.'
        ), SGR.yellow())

        while True:
            try:
                user_board_size = input('\nEnter your choice:\n')
                if int(user_board_size) > 4 and int(user_board_size) < 9:
                    Board._set_board_size(int(user_board_size))
                    break
                else:
                    raise ValueError
            
            except ValueError:
                print()
                SGR.print(' Invalid Input! Make sure that you enter one ', SGR.white(), SGR.red())
                SGR.print(' of these options: 5, 6, 7 or 8              ', SGR.white(), SGR.red())
    
    _OBJ_BLANK = 'Blank'
    _OBJ_SHIP = 'Ship'
    _OBJ_MISS = 'Miss'
    _OBJ_HIT = 'Hit'

    _OBJECTS = (
        {
            'id': 0,
            'label': _OBJ_BLANK,
            'char': SGR.char('\u25CF ', SGR.lt_grey())
        },
        {
            'id': 1,
            'label': _OBJ_SHIP,
            'char': SGR.char('S ', SGR.white())
        },
        {
            'id': 2,
            'label': _OBJ_MISS,
            'char': '  '
        },
        {
            'id': 3,
            'label': _OBJ_HIT,
            'char': SGR.char('\u2731 ', SGR.red())
        }
    )
    
    def __init__(self, name, reveal_ships):
        self.name = str(name)
        self.reveal_ships = bool(reveal_ships)
        self.board = []
        self.hits = 0
        self.misses = 0
        self.num_ships = self._number_of_ships
        self._create_board()
        self._position_ships()

    def _get_obj_char_by_id(self, object_id):
        for objs in Board._OBJECTS:
            if objs['id'] == object_id:
                return objs['char']

    def _get_obj_id_by_label(self, object_label):
        for objs in Board._OBJECTS:
            if objs['label'] == object_label:
                return objs['id']

    def _create_board(self):
        obj_blank = self._get_obj_id_by_label(Board._OBJ_BLANK)
        for row in range(Board._board_size):
            list_column = []
            for column in range(Board._board_size):
                list_column.append(obj_blank)
            self.board.append(list_column)
    
    def _position_ships(self):
        ship = self._get_obj_id_by_label(Board._OBJ_SHIP)
        blank = self._get_obj_id_by_label(Board._OBJ_BLANK)
        count = self._number_of_ships

        while count > 0:
            random_num = random.randrange(
                int(Board._board_size * Board._board_size))
            row = random_num // Board._board_size
            column = random_num % Board._board_size

            value = self.board[row][column]
            if value == blank:
                self.board[row][column] = ship
                count -= 1
            else:
                continue

    def _position_cursor(self, row, column):
        print(f'\x9B{row};{column}H', end='')

    def _move_cursor_right(self, col_relative):
        if int(col_relative) > 0:
            print(f'\x9B{int(col_relative)}C', end='')
        else:
            return

    def _get_str_row(self, list_row):
        obj_blank = self._get_obj_id_by_label(Board._OBJ_BLANK)
        obj_blank_char = self._get_obj_char_by_id(obj_blank)
        obj_ship = self._get_obj_id_by_label(Board._OBJ_SHIP)
        obj_ship_char = self._get_obj_char_by_id(obj_ship)

        row_string = ' '
        for board_object in list_row:
            if board_object == obj_blank:
                row_string += obj_blank_char
            elif board_object == obj_ship:
                row_string += obj_ship_char if self.reveal_ships else obj_blank_char
        
        return row_string

    def _display_board(self, row, column):
        current_row = int(row)
        for board_row in self.board:
            self._position_cursor(current_row, int(column))
            row_op_string = self._get_str_row(board_row)
            SGR.print(row_op_string, SGR.white(), SGR.blue(), '')
            current_row += 1
        print()

    def _display_column_header(self, col_relative):
        self._move_cursor_right(col_relative)
        chr_a = ord('A')
        display_str = ''
        for col in range(self._board_size):
            display_str += chr(chr_a + col) + ' '
        SGR.print(display_str, SGR.yellow())

    def _display_row_header(self, column_relative):
        for row in range(self._board_size):
            self._move_cursor_right(column_relative)
            SGR.print(str(row + 1).rjust(2), SGR.yellow())
    
    def _display_score(self, column_relative):
        self._move_cursor_right(column_relative)
        SGR.print(str(f'{self.name}'), SGR.yellow())
        print()
        
        self._move_cursor_right(column_relative)
        SGR.print(str(f'Hits:   {self.hits}'), SGR.yellow())
        
        self._move_cursor_right(column_relative)
        SGR.print(str(f'Misses: {self.misses}'), SGR.yellow())

    def display(self, row, column):
        self._position_cursor(row, 1)
        self._display_score(column + 3)
        print()
        self._display_column_header(column + 3)
        print()
        self._display_row_header(column - 1)
        self._display_board(row + 7, column + 3)

    def num_of_ships_remaining(self):
        return self.num_ships

class Human(Board):
    '''
    Human player
    '''
    def __init__(self, name):
        super().__init__(name, True)
        self.quit = False
        self.row_user_select = 0
        self.column_user_select = 0
 
    def get_coord_quit(self):
        ord_A = int(ord('A'))
        ord_nought = int(ord('1'))

        print()
        SGR.print('Enter your co-ordinates in the column row format', SGR.yellow())
        SGR.print('For example to enter column C row 4, enter C4.', SGR.yellow())
        msg_line = str(f'From A to {chr(self._board_size - 1 + ord_A)} and')
        msg_line += str(f' from 1 to {chr(self._board_size - 1 + ord_nought)}')
        SGR.print(msg_line, SGR.yellow())
        print()
        SGR.print('Or if you wish to exit, enter q or quit.', SGR.yellow())
        print()
        while True:
            try:
                choice = str(input('Enter your choice:\n')).replace(' ', '').upper()
 
                if choice == 'Q' or choice == 'QUIT':
                    self.quit = True
                    return

                elif len(choice) == int(2):
                    self._parse_input(choice)
                    return

                else:
                    raise ValueError

            except ValueError:
                print()
                SGR.print(' Invalid Input!                          ', SGR.white(), SGR.red())
                SGR.print(' Make sure you enter valid co-ordinates. ', SGR.white(), SGR.red())
                SGR.print(' Or enter q or quit to exit.             ', SGR.white(), SGR.red())

            except Exception:
                print()
                SGR.print(' Co-ordinates out of range!                   ', SGR.black(), SGR.lt_grey())
                SGR.print(' Make sure that you enter valid co-ordinates. ', SGR.black(), SGR.lt_grey())
                SGR.print(str(' ' + msg_line + str(' ' * 18)), SGR.black(), SGR.white())

    def exec(self, opponent):
        pass

    def _parse_input(self, coordinates):
        parse_chars = [char for char in coordinates]

        first_column = ord(parse_chars[0]) - ord('A')
        second_row = ord(parse_chars[1]) - ord('1')
        if first_column > -1 and first_column < Board._board_size:
            self.column_user_select = first_column
        elif second_row > -1 and second_row <  Board._board_size:
            self.row_user_select = second_row
        else:
            raise Exception

    def continue_playing(self):
        return self.quit

class Computer(Board):
    '''
    Computer player
    '''
    def __init__(self):
        super().__init__('Computer', False)
        pass

    def exec(self, opponent):
        pass
        
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
    def title_select_option():
        clear_screen()
        TitleMenu.display_title()
        TitleMenu.display_menu()
        user_response = TitleMenu.input_user_response()
        return user_response

class Game:
    '''
    Game class
    '''
    @staticmethod
    def _get_player_name():
        MAX_LENGTH = 16

        clear_screen()
        SGR.print('What\'s your name?', SGR.yellow())
        print()
        while True:
            name_plyr = str(input(str(
                f'Enter your name (max. {MAX_LENGTH} characters):\n'
            )))

            if len(name_plyr) == 0:
                print()
                SGR.print('Sorry I didn\'t get your name.', SGR.yellow())
                SGR.print('Make sure that you enter your name below.', SGR.yellow())
                print()
            elif len(name_plyr) > MAX_LENGTH:
                print()
                SGR.print('Sorry the max characters that', SGR.yellow())
                SGR.print(str(f'you can input is {MAX_LENGTH}.'), SGR.yellow())
                print()
            else:
                return name_plyr

    @staticmethod
    def _display_congratulations():
        pass

    @staticmethod
    def _display_commiserations():
        pass

    @staticmethod
    def _display_key_info():
        pass

    @staticmethod
    def _play(human_player, computer_player):
        human_player.get_coord_quit()
        human_player.exec(computer_player)
        computer_player.exec(human_player)
        return human_player.continue_playing()

    @staticmethod
    def play_battleship():
        Board.player_select_board_size()
        player_name = Game._get_player_name()
        
        human_player = Human(player_name)
        computer_player = Computer()

        while True:
            clear_screen()
            computer_player.display(1, 1)
            human_player.display(1, 31)

            Game._display_key_info()
            game_status = Game._play(human_player, computer_player)

            if game_status == 'human won':
                Game._display_congratulations()
                game_status = 'exit'

            elif game_status == 'computer won':
                Game._display_commiserations()
                game_status = 'exit'

            if game_status == 'exit':
                input('Press Enter to continue:\n')
                del human_player
                del computer_player
                return 

            else:
                continue

def main():
    random.seed()
    while True:
        user_option_select = TitleMenu.title_select_option()
        if user_option_select == 'i':
            print('Feature not yet implemented')
            input('Press enter to continue:\n')

        elif user_option_select == 'p':
            Game.play_battleship()

        elif user_option_select == 'q':
            return

def test():
    while True:
        clear_screen()
        human_player = Human('John')
        human_player.get_coord_quit()

        print()
        exit_string = input('exit ?\n')
        if exit_string == 'q':
            return
        else:
            continue

test()
