# Antonov Battleships

![am i responsive](docs/amireponsive.png)

The site is deployed [here](https://rfow-antonov-battleship-game-ecd25dcecf29.herokuapp.com/)

## About Antonov Battleships

Antonov Battleships is a game played between the user and the computer. The user can choose to play with any size board from 5 by 5 to 8 by 8. The number ships the board has varies from 5, 7, 9 and 12 ships depending on the size of board.

When the user starts the game the app presents 4 options with different size boards with a number of ships. Then the app asks for the user\'s name and starts the game. Two boards are presented with the ships placed on the boards at random.

The objective is to sink all the ships before one\'s opponent does.

## How to play

The game is started by entering p and pressing enter.

### Board size selection

The first thing the app asks for is to select the board size as shown. Each size comes with a number of ships to play with.

![board size select option](docs/board-size-selection.png)

### Name input

The second thing the app asks for is your name.

![name input](docs/name-input.png)

### Opening game

The game opens up with this as shown

![opening game](docs/play-open-round.png)

It displays two boards and informatiom on the right. The first board shows the computer. Each position is marked with a dot and ships are revealed.

The second board, your board, shows the position of the ships. On each board the rows are labeled by numbers and column by letters. You enter your guess of where you think the computer ship is. You enter the coordinates using the column row format: for example to enter column C row 2 you enter c2 as shown above.

### Play

![during game play](docs/game-in-play-2.png)

If the coordinates that you\'ve input results in a miss a blank space appears. If it results in a hit a red asterisk sppears as shown above.

The panel on the right show what happened during previous round: whether you and the computer had missed or hit a ship.

### End Game

When you won that is the computer has all its ships hit the game ends with this message as shown below.

![congratulatory message](docs/player-won-message.png)

If you lose all your ships the message below is shown.

![player lost message](docs/player-lost-message.png)

## Features

![Opening Title](docs/antonov-battleships.png)

### Existing Features

The app features title with options, instructions and the game.
The app starts with the opening title as shown above. After user has selected the size of board and entered one's name, the computer's, player's board, information board is displayed as shown below.

![the game in play](docs/game-in-play-general.png)

The information panel on the right displays what happened during the previous round and input instructions below that.

#### Board

Each board has player's or computer name, score showing both hits and misses and the game board. The board's column are headed letters and rows by numbers from 1.

#### Information panel

The information panel display on the right of the two boards displays what happened during the previous round. Underneath the input instructions are displayed. At the end of the game, a game over message is displayed.

#### Input validation

The app validates an incorrect input with a message as shown below. An invalid message is displayed with white text on red background.

![invalid input](docs/example-invalid-input.png)

If the user input coordinates already inputed this message below is displayed. As it is a warning message, the text is displayed with black text on a white background.

![warning message](docs/warning-message.png)

## Concept and Design

The title for the game was chosen arbitrarily.

## Data Model



## Testing

Testing the app was done on codeanywhere, on the deployed site at Heroku and by running the code through the PEP8 linter: [Code Institute Python Linter](https://pep8ci.herokuapp.com/).

### Bugs

#### Spelling mistakes in identifiers

Most of the bugs encountered were due to spelling mistakes in identifiers. These were corrected as soon as they were identified.

#### Invalid comparison

This was the most baffaling. During the test to parse input to process co-ordinates, this code always evaluated to false.

```py
...

elif len(choice) == 2:
    parse_status = self._parse_input(choice)

...
```

To fix this the code was changed from the literal \'2\' to \'int(2)\' as below.

```py
...

elif len(choice == int(2):
    parse_status = self._parse_input(choice)

...
```

#### Error detected during linting

This error was detected during linting.

```py
if self._check_coord_picked(row, column) == False:
    list_coord = [row, column]
    self.previous_chosen_coord.append(list_coord)
    break
```

To pass the lint test the code was changed to this shown below.

```py
if self._check_coord_picked(row, column) is False:
    list_coord = [row, column]
    self.previous_chosen_coord.append(list_coord)
    break
```

#### Color reproduction

During testing on codeanywhere the colours were not not reproduced accurately. To test whether the colors displayed correctly the code had to be deployed to github and then to Heroku.

On the first test of the app on Heroku the background and foreground colors was preselected and then clear screen command was sent. This resulted in the corruption of the background color. Instead of it being black displayed a grey background. The result was to rethink how colors should be applied in the app. The result was a redesign of how the app applied the colors. The result was to use the system default background color and only the background color where it was needed.

### Remaining Bugs

There are no known bugs remaining.

### Validator Testing

The pep8 validator used was the [Code Institute Python Linter](https://pep8ci.herokuapp.com/). It was used frequently during code refactoring. All errors and warnings were addresses until the linter gave out no error or warnings.

## Deployment

The game was deployed to Heroku as follows

- Login to your Heroku account
- Click on create new app
- Enter the app name in the \'App Name\'
- Click on Choose a region and select Europe
- Click on \'Settings\'
- In the Config Vars create a _Config Var_ called PORT and set this value to 8000
- In the build pack section add Python and then Nodejs
- Click on Deploy
- In the deployment method section click on Connect to Github
- Click on the Connect to Github button to confirm
- In the search for repository enter the \'antonov-battleship-game\' and click on search
- In the earch field on the repository and click on connect
- In the automatic deploy section click on \'Enable Automatic Deploys\' button
- The game is now is now deployed to Heroku

The link to deployed app is [here](https://rfow-antonov-battleship-game-ecd25dcecf29.herokuapp.com/)

## Credits

I'd like to thank my mentor for providing excellent guidance and advice.

### Resources

Use of ASCII escape control code in classes CSI and SGR was taken from [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code)

The use of clearing screen and positioning the cursor using control codes was taken from [CSI (Control Sequence Introducer) sequences](https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences) on Wikipedia.

The use of color control codes used in the SGR class was taken from [SGR (Select Graphic Rendition) parameters](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters) on Wikipedia.

This resource was useful to aid my understanding on the use of control characters to position cursors, clear screens and color foreground and background [Build your own Command Line with ANSI escape codes](https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html).

Corey's Tutorial on \'if __name__ == \'__main__\'\'
[Python Tutorial: if __name__ == '__main__'](https://www.youtube.com/watch?v=sugvnHA7ElY)

This was also useful to aid my understanding of classes and property in python
[Python OOP Tutorial](https://www.youtube.com/watch?v=ZDa-Z5JzLYM)

This resource was useful to understand the original Battleship game on [The Battleship Game](https://en.wikipedia.org/wiki/Battleship_(game)) on Wikipedia.
