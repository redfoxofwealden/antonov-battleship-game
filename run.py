# Write your code to expect a terminal of 80 characters wide and 24 rows high

class Char:
    clear_screen = '\x9B3J\x9B;H\x9B0J'

def clear_screen():
    print(Char.clear_screen, end='')

def test():
    for c in range(20):
        print('lots of messages')

    input('Press return to continue\n')

    clear_screen()

    print('Screen should be clear')

test()