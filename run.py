# Write your code to expect a terminal of 80 characters wide and 24 rows high
import random


class CSI:
    '''
    CSI class

    provides screen clearing
    cursor positioning
    '''
    @staticmethod
    def clear_screen():
        print('\x9B3J\x9B;H\x9B0J', end='')

    @staticmethod
    def position_cursor(row, column):
        print(f'\x9B{row};{column}H', end='')

    @staticmethod
    def move_cursor_right(column_relative):
        if int(column_relative) > 0:
            print(f'\x9B{int(column_relative)}C', end='')
        else:
            return

    @staticmethod
    def move_cursor_up_one():
        print('\x9B1A', end='')


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
        fg_clr_prm = (int(fg_clr) + 30) \
            if int(fg_clr) < 8 else (int(fg_clr) + 82)
        fg_chars = str(f'\x9B{fg_clr_prm}m')
        return str(fg_chars + str(str_char_arg))

    @staticmethod
    def print(str_argument, fg_clr, bg_clr=None, endline='\n'):
        fg_clr_prm = (int(fg_clr) + 30) \
            if int(fg_clr) < 8 else (int(fg_clr) + 82)
        fg_chars = str(f'\x9B{fg_clr_prm}m')
        fg_def_chars = str('\x9B39m')

        if bg_clr is not None:
            bg_clr_prm = (int(bg_clr) + 40) \
                if int(bg_clr) < 8 else (int(bg_clr) + 92)
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
        CSI.clear_screen()
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
                SGR.print(
                    ' Invalid Input! Make sure that you enter one ',
                    SGR.white(), SGR.red())
                SGR.print(
                    ' of these options: 5, 6, 7 or 8              ',
                    SGR.white(), SGR.red())

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
            'char': SGR.char('S ', SGR.black())
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
        self.num_ships_remaining = self._number_of_ships
        self.previous_message = ''
        self.previous_chosen_coord = []
        self._create_board()
        self._position_ships()

    def _check_coord_picked(self, row, column):
        for element in self.previous_chosen_coord:
            if element[0] == row and element[1] == column:
                return True

        return False

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
        count_1 = Board._board_size
        while count_1 > 0:
            list_column = []
            count_2 = Board._board_size
            while count_2 > 0:
                list_column.append(obj_blank)
                count_2 -= 1
            self.board.append(list_column)
            count_1 -= 1

    def _position_ships(self):
        ship = self._get_obj_id_by_label(Board._OBJ_SHIP)
        blank = self._get_obj_id_by_label(Board._OBJ_BLANK)
        count = Board._number_of_ships

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

    def _get_str_row(self, list_row):
        obj_blank = self._get_obj_id_by_label(Board._OBJ_BLANK)
        obj_blank_char = self._get_obj_char_by_id(obj_blank)
        obj_ship = self._get_obj_id_by_label(Board._OBJ_SHIP)
        obj_ship_char = self._get_obj_char_by_id(obj_ship)
        obj_miss = self._get_obj_id_by_label(Board._OBJ_MISS)
        obj_miss_char = self._get_obj_char_by_id(obj_miss)
        obj_hit = self._get_obj_id_by_label(Board._OBJ_HIT)
        obj_hit_char = self._get_obj_char_by_id(obj_hit)

        row_string = ' '
        for column_count in range(Board._board_size):
            if list_row[column_count] == obj_blank:
                row_string += obj_blank_char
            elif list_row[column_count] == obj_ship:
                row_string += obj_ship_char \
                    if self.reveal_ships else obj_blank_char
            elif list_row[column_count] == obj_miss:
                row_string += obj_miss_char
            elif list_row[column_count] == obj_hit:
                row_string += obj_hit_char
            else:
                raise Exception('An error has occured in _get_str_row().')

        return row_string

    def _display_board(self, row, column):
        current_row = int(row)
        for row_count in range(Board._board_size):
            CSI.position_cursor(current_row, column)
            row_op_string = self._get_str_row(self.board[row_count])
            SGR.print(row_op_string, SGR.white(), SGR.blue(), '')
            current_row += 1
        print()

    def _display_column_header(self, column_relative):
        CSI.move_cursor_right(column_relative)
        chr_a = ord('A')
        display_str = ''
        for col in range(self._board_size):
            display_str += chr(chr_a + col) + ' '
        SGR.print(display_str, SGR.yellow())

    def _display_row_header(self, column_relative):
        for row in range(self._board_size):
            CSI.move_cursor_right(column_relative)
            SGR.print(str(row + 1).rjust(2), SGR.yellow())

    def _display_score(self, column_relative):
        CSI.move_cursor_right(column_relative)
        SGR.print(str(f'{self.name}'), SGR.yellow())
        print()

        CSI.move_cursor_right(column_relative)
        SGR.print(str(f'Hits:   {self.hits}'), SGR.yellow())

        CSI.move_cursor_right(column_relative)
        SGR.print(str(f'Misses: {self.misses}'), SGR.yellow())

    def _strike(self, row_select, column_select):
        '''
        returns either Hit or Miss depending
        on whether the ship has been struck or not
        '''

        id_value = self.board[row_select][column_select]

        if id_value == self._get_obj_id_by_label(Board._OBJ_SHIP):
            self.board[row_select][column_select] = \
                self._get_obj_id_by_label(Board._OBJ_HIT)
            self.num_ships_remaining -= 1
            exit_message = 'Hit'

        elif id_value == self._get_obj_id_by_label(Board._OBJ_BLANK):
            self.board[row_select][column_select] = \
                self._get_obj_id_by_label(Board._OBJ_MISS)
            exit_message = 'Miss'

        else:
            raise Exception('An error has occured during call to strike()')

        return exit_message

    def _strike_object(self, opponent, row, column):
        strike_status = opponent._strike(row, column)
        if strike_status == 'Hit':
            self.previous_message = 'Hit'
            self.hits += 1
        elif strike_status == 'Miss':
            self.previous_message = 'Miss'
            self.misses += 1
        else:
            raise Exception('Return from strike() has to be Hit or Miss.')

    def display(self, row, column):
        CSI.position_cursor(row, 1)
        self._display_score(column + 3)
        print()
        self._display_column_header(column + 3)
        print()
        self._display_row_header(column - 1)
        self._display_board(row + 7, column + 3)

    def get_message_previous(self):
        if self.previous_message == 'Hit':
            previous_message = str(f'{self.name} has hit')
        elif self.previous_message == 'Miss':
            previous_message = str(f'{self.name} has missed')
        elif self.previous_message == '':
            previous_message = ''
        else:
            raise Exception('An error has occured in get_message_previous()')

        return previous_message

    def has_ships(self):
        return True if self.num_ships_remaining > 0 else False


class Human(Board):
    '''
    Human player
    '''
    def __init__(self, name):
        super().__init__(name, True)
        self.continue_play_game = True
        self.row_user_select = -1
        self.column_user_select = -1

    def _parse_input(self, coordinates):
        parse_chars = [char for char in coordinates]

        first_column = ord(parse_chars[0]) - ord('A')
        if first_column > -1 and first_column < Board._board_size:
            second_row = ord(parse_chars[1]) - ord('1')
            if second_row > -1 and second_row < Board._board_size:
                bool_already_picked = \
                    self._check_coord_picked(second_row, first_column)
                if bool_already_picked:
                    exit_msg = 'Chosen'

                else:
                    self.column_user_select = first_column
                    self.row_user_select = second_row

                    list_coord = [second_row, first_column]
                    self.previous_chosen_coord.append(list_coord)
                    exit_msg = 'OK'
            else:
                exit_msg = 'Invalid'

        else:
            exit_msg = 'Invalid'

        return exit_msg

    def get_coord_quit(self):
        print()
        SGR.print('Enter your co-ordinates or', SGR.yellow())
        SGR.print('your option to exit.', SGR.yellow())

        print()
        while True:
            choice = str(
                input('Enter your choice:\n'
                      )).replace(' ', '').upper()

            if choice == 'Q' or choice == 'QUIT':
                self.continue_play_game = False
                return

            elif len(choice) == int(2):
                parse_status = self._parse_input(choice)

            else:
                parse_status = 'Invalid'

            if parse_status == 'OK':
                return

            elif parse_status == 'Invalid':
                print()
                SGR.print(
                    ' Invalid Input!                          ',
                    SGR.white(), SGR.red())
                SGR.print(' Make sure you enter valid co-ordinates. ',
                          SGR.white(), SGR.red())
                SGR.print(' Or enter q or quit to exit.             ',
                          SGR.white(), SGR.red())
                print()

            elif parse_status == 'Chosen':
                print()
                SGR.print(' These co-ordinates have been already chosen. ',
                          SGR.black(), SGR.lt_grey())
                SGR.print(' Enter another one.                           ',
                          SGR.black(), SGR.lt_grey())
                print()

            else:
                raise Exception('An error has occured in get_coord_quit()')

    def exec(self, opponent):
        if self.row_user_select == -1 or self.column_user_select == -1:
            raise Exception(
                'get_coord_quit() has to be called' +
                ' first before calling this function.')
        else:
            self._strike_object(opponent,
                                self.row_user_select, self.column_user_select)

    def continue_playing(self):
        return self.continue_play_game


class Computer(Board):
    '''
    Computer player
    '''
    def __init__(self):
        super().__init__('Computer', False)

    def exec(self, opponent):
        while True:
            random_value = random.randrange(
                Board._board_size * Board._board_size
            )
            row = random_value // Board._board_size
            column = random_value % Board._board_size
            if self._check_coord_picked(row, column) is False:
                list_coord = [row, column]
                self.previous_chosen_coord.append(list_coord)
                break

        self._strike_object(opponent, row, column)


class TitleMenu:
    '''
    Displaying the title of the game.
    '''

    _TITLE_NAME = str(r'''
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
        SGR.print(TitleMenu._TITLE_NAME, SGR.lt_green())

    @staticmethod
    def display_menu():
        SGR.print(
            str('Enter I for instructions,    ').center(80), SGR.yellow())
        SGR.print(
            str('      P to play or Q to exit.').center(80), SGR.yellow())

    @staticmethod
    def input_user_option_select():
        while True:
            user_option = str(input('\nEnter your option:\n')).lower()
            if user_option == 'i':
                break

            elif user_option == 'p':
                break

            elif user_option == 'q':
                break

            else:
                print()
                SGR.print(
                    ' Invalid Input! Make sure you ' +
                    'enter one of these options: ',
                    SGR.white(), SGR.red())
                SGR.print(
                    ' I for instructions, P to play, ' +
                    'or Q to exit.             ',
                    SGR.white(), SGR.red())

        return user_option

    @staticmethod
    def title_select_option():
        CSI.clear_screen()
        TitleMenu.display_title()
        TitleMenu.display_menu()
        return TitleMenu.input_user_option_select()


class Game:
    '''
    Game class
    '''

    def __init__(self):
        self.computer_player = None
        self.human_player = None
        self.player_name = None

    _MAX_LENGTH = 16

    @staticmethod
    def _get_player_name():

        CSI.clear_screen()
        SGR.print('What\'s your name?', SGR.yellow())
        print()
        while True:
            name_plyr = str(input(str(
                f'Enter your name (max. {Game._MAX_LENGTH} characters):\n'
            )))

            if len(name_plyr) == 0:
                print()
                SGR.print('Sorry I didn\'t get your name.', SGR.yellow())
                SGR.print(
                    'Make sure that you enter your name below.',
                    SGR.yellow())
                print()
            elif len(name_plyr) > Game._MAX_LENGTH:
                print()
                SGR.print('Sorry the max characters that', SGR.yellow())
                SGR.print(str(
                    f'you can input is {Game._MAX_LENGTH}.'), SGR.yellow())
                print()
            else:
                return name_plyr

    def _display_congratulations(self):
        self._display_player_boards()
        print()
        message = str(f' {self.player_name} you\'ve beaten me. ')
        msg_length = len(message)
        msg_congratulations = str(' Congratulations!' + str(' ' * msg_length))
        msg_congratulations = msg_congratulations[0: msg_length]

        SGR.print(msg_congratulations, SGR.lt_yellow(), SGR.green())
        SGR.print(str(' ' * msg_length), SGR.lt_yellow(), SGR.green())
        SGR.print(message, SGR.lt_yellow(), SGR.green())

        print()
        Game._pause()

    def _display_commiserations(self):
        self._display_player_boards()
        print()
        message = str(f'Sorry {self.player_name}!')

        SGR.print(message, SGR.yellow())
        print()
        SGR.print('You\'ve lost.', SGR.yellow())
        SGR.print('Better luck next time!', SGR.yellow())

        print()
        Game._pause()

    def _display_player_boards(self):
        CSI.clear_screen()
        self._display_previous_message_key_info(1, 49)
        self.computer_player.display(1, 1)
        self.human_player.display(1, 24)

    def _display_previous_message_key_info(self, row, column):
        message_human = self.human_player.get_message_previous()
        message_computer = self.computer_player.get_message_previous()

        current_row = int(row)
        CSI.position_cursor(current_row, int(column))
        SGR.print('Previous round:', SGR.yellow(), None, '')
        current_row += 2

        CSI.position_cursor(current_row, int(column))
        if message_human != '':
            SGR.print(message_human, SGR.yellow(), None, '')
        current_row += 2

        CSI.position_cursor(current_row, int(column))
        if message_computer != '':
            SGR.print(message_computer, SGR.yellow(), None, '')
        current_row += 2

        CSI.position_cursor(current_row, int(column))
        SGR.print('Input Instructions:', SGR.yellow(), None, '')
        current_row += 2

        CSI.position_cursor(current_row, int(column))
        SGR.print('To enter the coordinates, enter', SGR.yellow(), None, '')
        current_row += 1

        CSI.position_cursor(current_row, int(column))
        SGR.print('the column letter, then row', SGR.yellow(), None, '')
        current_row += 1

        CSI.position_cursor(current_row, int(column))
        SGR.print('number. For e.g. to enter column', SGR.yellow(), None, '')
        current_row += 1

        CSI.position_cursor(current_row, int(column))
        SGR.print('C, row 4 enter C4.', SGR.yellow(), None, '')
        current_row += 2

        CSI.position_cursor(current_row, int(column))
        SGR.print('To exit, enter q or quit.', SGR.yellow(), None, '')
        print()

    def _play(self):
        self.human_player.get_coord_quit()
        if self.human_player.continue_playing():
            self.human_player.exec(self.computer_player)
            if self.computer_player.has_ships():
                self.computer_player.exec(self.human_player)
                if self.human_player.has_ships():
                    exit_status = ''
                else:
                    exit_status = 'computer won'
            else:
                exit_status = 'human won'
        else:
            exit_status = 'exit'

        return exit_status

    def _play_battleship(self):
        Board.player_select_board_size()
        self.player_name = Game._get_player_name()

        self.human_player = Human(self.player_name)
        self.computer_player = Computer()

        while True:
            self._display_player_boards()
            game_status = self._play()

            if game_status == 'human won':
                self._display_congratulations()
                game_status = 'exit'

            elif game_status == 'computer won':
                self._display_commiserations()
                game_status = 'exit'

            if game_status == 'exit':
                self.human_player = None
                self.computer_player = None
                return

            else:
                continue

    @staticmethod
    def _show_object_key_info(object_label, object_char, object_char_color):
        SGR.print(object_label, SGR.yellow())
        CSI.move_cursor_up_one()
        CSI.move_cursor_right(10)
        SGR.print(object_char, object_char_color, SGR.blue())
        CSI.move_cursor_right(10)
        SGR.print('   ', SGR.white(), SGR.blue())

    @staticmethod
    def _show_instructions():
        CSI.clear_screen()
        SGR.print('Antonov Battleships Instructions', SGR.lt_green())
        print()
        instructions_text = str(
            'Antonov battleships is game played between you and your '
            'opponent: the computer.'
            '\nThe objective is to sink all of your opponent\'s ships '
            'before your opponent'
            '\ndoes. When you start the game you\'ll be asked what size '
            'board you\'ll want to'
            '\nplay with. You\'ll have a choice of playing with 5 by 5 '
            'with 5 ships, 6 by 6'
            '\nwith 7 ships, 7 by 7 with 9 ships, or 8 by 8 with 12 ships. '
            'The winner is the'
            '\none who sinks all of his or her opponent\'s ships first.'
        )
        SGR.print(instructions_text, SGR.yellow())
        print()
        SGR.print('Key Information:', SGR.yellow())
        print()

        CSI.move_cursor_right(10)
        SGR.print('   ', SGR.white(), SGR.blue())
        Game._show_object_key_info('Ship', ' S ', SGR.black())
        Game._show_object_key_info('Miss', '   ', SGR.white())
        Game._show_object_key_info('Hit', ' \u2731 ', SGR.red())
        Game._show_object_key_info('Unknown', ' \u25CF ', SGR.lt_grey())
        print()

        Game._pause()

        CSI.clear_screen()
        SGR.print('Antonov Battleships Instructions', SGR.lt_green())
        print()
        instructions_text = str(
            'After you\'ve selected your board size and entered your '
            'name, 2 boards'
            '\nand an information panel will be displayed. '
            'The first: the'
            '\ncomputer\'s, the second: yours, and on the right the'
            ' information'
            '\npanel showing the outcome of the previous round and input'
            '\ninstructions.'
            '\n'
            '\nOn each board the columns are labeled with letters and rows are'
            '\nlabeled with numbers. You\'ll enter the coordinates of '
            'where you'
            '\nthink the opponent\'s ships is by entering the column letter'
            '\nfollowed by the row number. For example to enter '
            'the coordinates'
            '\ncolumn C row 4, you\'ll enter C4.'
            '\n'
            '\nDuring the game you can exit by entering q or quit.'
        )
        SGR.print(instructions_text, SGR.yellow())
        print()

        Game._pause()

    @staticmethod
    def _pause():
        while True:
            space_string = input('Press space and then enter to continue.\n')
            if space_string == ' ':
                return
            else:
                print()
                SGR.print(str(
                    ' Invalid Input! Make sure you\'ve followed '
                    'the instruction below. '
                ), SGR.white(), SGR.red())
                continue

    def run(self):
        random.seed()
        while True:
            user_option_select = TitleMenu.title_select_option()
            if user_option_select == 'i':
                Game._show_instructions()

            elif user_option_select == 'p':
                self._play_battleship()

            elif user_option_select == 'q':
                return


def main():
    antonov_battleships = Game()
    antonov_battleships.run()


# The idea for including the following was taken
# from one of Corey Schafer's youtube Python tutorials:
# if __name__ == '__main__'.  The link is below
# (https://www.youtube.com/watch?v=sugvnHA7ElY)
if __name__ == '__main__':
    main()
