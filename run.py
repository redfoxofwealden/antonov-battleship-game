# Write your code to expect a terminal of 80 characters wide and 24 rows high

class Char:
    '''
    Contains a list of characters from clearing the terminal screen
    to characters representing hits, misses, ships.
    '''
    HIT = '\u2731'
    MISS = '-'
    SHIP = 'S'
    UNKNOWN = '\u25CF'

def clear_screen(): 
        print('\n' * 24)
        
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
        print(TitleMenu._title_name)

    @staticmethod
    def display_menu():
        print('\nEnter one of the following:')
        print('\nI for instructions.')
        print('P to the play the game.')
 
    @staticmethod
    def input_user_response():
        while True:
            user_input = str(input('\nEnter your option\n')).lower()
            if user_input == 'i' or user_input == 'p':
                return user_input
            else:
                print('\nInvalid Input! Make sure you enter one of these options')
                print('I for instructions; or P to play.')
    
    @staticmethod
    def run():
        clear_screen()
        TitleMenu.display_title()
        TitleMenu.display_menu()
        user_response = TitleMenu.input_user_response()
        return user_response

def test():
    user_option = TitleMenu.run()
    print('\nUser response is ' + user_option)

test()
