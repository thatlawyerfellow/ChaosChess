# uncomment this line if running on colab or other notebooks else run pip install chess before you run the main.py file to install the chess library
# !pip install chess
# Import necessary libraries
import chess  # Chess library providing board management and move generation/validation
import random  # Used for generating random decisions within the game logic
import pickle  # For saving and loading game states
import os      # For file path management and checks

# Custom Chess Board Class
class ChaosChessBoard(chess.Board):
    def __init__(self):
        super().__init__()  # Initialize the superclass; creates a standard chess board

    def display(self):
        # Custom method to display the chess board in the console with a user-friendly layout
        print("  a b c d e f g h")
        print(" +-----------------+")
        for i in range(8, 0, -1):  # Loop over rows in reverse order to match traditional chess board representation
            line = f"{i}|"  # Start each line with the row number
            for j in range(97, 105):  # Loop over columns (a-h) by ASCII codes
                piece = self.piece_at(chess.parse_square(f"{chr(j)}{i}"))  # Retrieve the piece at the given square
                line += " " + (piece.symbol() if piece else ".")  # Append piece symbol or empty square marker
            print(line + f"|{i}")  # Print the completed line for the current row
        print(" +-----------------+")
        print("  a b c d e f g h\n")

# Spotter Class
class Spotter:
    def __init__(self, color):
        self.color = color  # Assign the spotter's team color

    def call_piece(self, board: ChaosChessBoard):
        # Method to randomly select a piece type that can legally move, returning the piece type and a suggested move
        pieces = ['Pawn', 'Knight', 'Bishop', 'Rook', 'Queen', 'King']
        random.shuffle(pieces)  # Randomize the order of piece types to select from
        for piece in pieces:  # Iterate through the shuffled list of pieces
            # Find all legal moves for the given piece type
            moves = [move for move in board.legal_moves if board.piece_at(move.from_square).piece_type == chess.PIECE_SYMBOLS.index(piece[0].lower())]
            if moves:  # If there are legal moves available for this piece type
                return piece, random.choice(moves)  # Return the piece type and a randomly selected legal move
        return None, None  # Return None if no legal moves are found for any piece type

# Game Management Functions
def save_game(game_state, filename='chaos_chess_game.pickle'):
    # Save the current game state to a file
    with open(filename, 'wb') as f:
        pickle.dump(game_state, f)  # Serialize and write the game state to the file
    print("Game saved successfully.")

def load_game(filename='chaos_chess_game.pickle'):
    # Load a game state from a file
    if os.path.exists(filename):  # Check if the file exists
        with open(filename, 'rb') as f:
            return pickle.load(f)  # Deserialize and return the loaded game state
    else:
        print("No saved game found.")
        return None

def play_game(human_color='white'):
    # Main game loop for playing Chaos Chess
    board = ChaosChessBoard()  # Initialize the chess board
    human_spotter = Spotter(human_color)  # Create a Spotter instance for the human player
    computer_color = 'black' if human_color == 'white' else 'white'  # Determine the computer's color based on the human's choice
    computer_spotter = Spotter(computer_color)  # Create a Spotter instance for the computer player

    while not board.is_game_over():  # Continue playing until the game is over
        board.display()  # Display the current state of the chess board

        if board.turn == chess.WHITE and human_color == 'black':
            # Computer's turn to move as white
            _, move = computer_spotter.call_piece(board)
            print(f"Computer (as White) moves: {move}")
            board.push(move)

        elif board.turn == chess.BLACK and human_color == 'white':
            # Computer's turn to move as black
            _, move = computer_spotter.call_piece(board)
            print(f"Computer (as Black) moves: {move}")
            board.push(move)

        else:
            # Human's turn
            piece, move = human_spotter.call_piece(board)
            print(f"Your spotter calls: {piece}. Example move: {move}")
            move_made = False
            while not move_made:
                user_move = input("Your move: ")
                if user_move.lower() == 'save':
                    save_game((board.fen(), human_color))
                    continue
                elif user_move.lower() == 'exit':
                    print("Exiting game.")
                    return
                try:
                    board.push_san(user_move)
                    move_made = True
                except ValueError:
                    print("Invalid move, try again.")

    # Game over logic
    print("Game over.")
    if board.is_checkmate():
        print("Checkmate!")
    elif board.is_stalemate():
        print("Stalemate!")
    elif board.is_insufficient_material():
        print("Draw due to insufficient material.")

def main():
    # Entry point of the application; presents the user with initial options
    print("""Welcome to Chaos Chess!
Choose your color and play against the computer. Your spotter will call a piece, and you must move it if possible.""")
    choice = input("Start a new game (n), load a game (l), or exit (e)? ")
    if choice.lower() == 'n':
        color_choice = input("Choose your color (white/black): ").lower()
        play_game(color_choice)
    elif choice.lower() == 'l':
        game_state = load_game()
        if game_state:
            board_state, human_color = game_state
            play_game(human_color)
    elif choice.lower() == 'e':
        print("Goodbye!")

if __name__ == "__main__":
    main()  # Run the main function if this script is executed directly
