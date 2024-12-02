########################################
# Tic Tac Toe
# Game for two players
#
#  1 | 2 | 3  		   |   |
# ---+---+---  		---+---+---
#  4 | 5 | 6  		   |   |
# ---+---+---  		---+---+---
#  7 | 8 | 9  		   |   |
########################################

# Tic Tac Toe 3 x 3 board (list)
game_board = [
    " ", " ", " ",
    " ", " ", " ",
    " ", " ", " "
]

# Tic Tac Toe winning combinations
WINNING_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],    # Horizontal lines
    [0, 3, 6], [1, 4, 7], [2, 5, 8],    # Vertical lines
    [0, 4, 8], [2, 4, 6]                # Diagonal lines
]

# List of taken fields
previous_turns = []

# Game score
score = {
    "X": 0,
    "O": 0
}


def print_game_board():
    """
    Displays the Tic Tac Toe game board
    :return: None
    """
    print()
    print(f" 1 | 2 | 3  \t\t {game_board[0]} | {game_board[1]} | {game_board[2]} ")
    print("---+---+---  \t\t---+---+---")
    print(f" 4 | 5 | 6  \t\t {game_board[3]} | {game_board[4]} | {game_board[5]} ")
    print("---+---+---  \t\t---+---+---")
    print(f" 7 | 8 | 9  \t\t {game_board[6]} | {game_board[7]} | {game_board[8]} ")
    print()


def reset_game():
    """
    Resets the game board and list of turns before starting a new game
    :return: None
    """
    for index in range(9):
        game_board[index] = " "

    previous_turns.clear()


def get_player_move(player):
    """
    Gets user input, validates it and updates the game board accordingly (adds X or O symbol)
    :param player: X or O
    :return: None
    """
    move = input(f"Next turn: '{player}'. Please select a number (1 - 9) to place your symbol: ")
    error_message = "Please try again. Select a number (1 - 9): "

    while True:
        if move.isdigit():
            move = int(move)
            if 1 <= move <= 9 and move not in previous_turns:
                previous_turns.append(move)
                game_board[move - 1] = player
                print_game_board()
                break
            else:
                move = input(error_message)
        else:
            move = input(error_message)


def check_winner(player):
    """
    Checks if player wins
    :param player: X or O
    :return: True if player wins, otherwise False
    """
    is_winner = False
    for combination in WINNING_COMBINATIONS:
        if player == game_board[combination[0]] == game_board[combination[1]] == game_board[combination[2]]:
            is_winner = True
            break
    return is_winner


# Play the game
def play_tictactoe():
    """
    Main game logic
    :return: None
    """
    players = ["X", "O"]

    print("Welcome to Tic Tac Toe game for two players!")
    print_game_board()

    for turn in range(9):               # Maximum 9 turns
        player = players[turn % 2]      # Players take turns
        get_player_move(player)
        is_winner = check_winner(player)
        if is_winner:
            score[player] += 1
            print(f"Player {player} wins!")
            print(f"Current score: 'X' : 'O' = {score['X']} : {score['O']}")
            break
    else:
        print("It is a tie!")
        print(f"Current score: 'X' : 'O' = {score['X']} : {score['O']}")


if __name__ == "__main__":
    while True:
        play_tictactoe()

        play_again = input("Play again (Y/N): ")
        if play_again.lower() == "y":
            reset_game()
        else:
            print(f"Final score: 'X' : 'O' = {score['X']} : {score['O']}")
            print("Thank you for playing.")
            break
