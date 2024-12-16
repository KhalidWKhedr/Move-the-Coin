The "Moving The Coin" game is a graphical game where players control a coin's movement across a grid of nodes. The game allows for both human and machine players, with different modes available based on who starts first. This game is built using Python and Tkinter for the graphical interface and features an interactive board with nodes and links that represent possible movements.
Features

    Interactive GUI: A grid of nodes with clickable areas where the coin can move.
    Human vs Machine: Players can choose whether they or the machine will start the game.
    Restart & Exit: Players can restart the game or exit at any time.
    Game Logic: The coin moves according to a pathfinding algorithm (Bresenham's line algorithm) to create smooth movement across the grid.

Installation

To run this project locally, follow these steps:

    Clone the repository:

git clone https://github.com/yourusername/moving-the-coin.git

Navigate into the project directory:

cd moving-the-coin

Install the required dependencies: This project requires Python and the Tkinter module for the GUI. If you don't have Tkinter installed, you can install it via:

pip install tk

Run the game: To start the game, run the following command:

    python game.py

How to Play

    Choose who starts: You can choose to have either the machine or the human player start the game by selecting the appropriate option from the GUI.

    Move the coin: Once the game starts, you can click on the nodes to move the coin. The goal is to make strategic moves to win the game.

    Restart the game: If you'd like to play again, click the "Restart" button.

    Exit the game: You can exit the game at any time by clicking the "Exit" button.

Game Configuration

The game graph (nodes and connections) is defined in a config.txt file, which the game reads to build the grid. This file contains the following:

    The number of nodes.
    A list of nodes, each with a name and coordinates (X, Y).
    A list of connections, each specifying a pair of nodes and a value indicating the strength of the connection.

Example config.txt:

5
Start 100 100
A 200 200
B 300 300
C 400 400
D 500 500
Start A 1
A B 2
B C 3
C D 4

Contributing

If you would like to contribute to the project:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes.
    Commit your changes (git commit -am 'Add new feature').
    Push to the branch (git push origin feature-branch).
    Create a new Pull Request.
