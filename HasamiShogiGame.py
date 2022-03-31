# Author: Juan Pablo Duque Ochoa
# Date: 11/27/2021
# Description: Hasami Shogi game simulator between two players (Black and Red). It has two classes, HasamiShogiGame
# and Board.


class HasamiShogiGame:
    """
    Represents a Hasami Shogi Game between a Black Player and a Red Player, playing in a 9x9 Board, each player with
    9 pieces.
    """
    def __init__(self):
        """
        Starts the Game, by initializing the game state, the first turn for the Black Player,
        a Board object, and the 9 starting pieces of each player.
        """
        # Board initialization with players' pieces in starting positions in the board
        self._board = Board().get_board()
        self._game_state = "UNFINISHED"
        self._active_player = "BLACK"
        self._black_pieces = 9
        self._red_pieces = 9

    def capture_piece(self, inactive_piece: str):
        """
        Takes inactive_piece ('B ' or 'R ') and captures the piece of the inactive player (whose turn is next),
        reducing the number of its pieces by 1.
        """
        # After Black player makes its move, Red player becomes the active player, but first the captures update is made
        if inactive_piece == "R ":
            self._red_pieces -= 1
        # After Red player makes its move, Black player becomes the active player, but first the captures update is made
        elif inactive_piece == "B ":
            self._black_pieces -= 1

    def get_game_state(self):
        """
        Returns the current state of the game (UNFINISHED, RED_WON, BLACK_WON).
        """
        return self._game_state

    def get_active_player(self):
        """
        Returns whose turn it is to play (RED or BLACK).
        """
        return self._active_player

    def get_num_captured_pieces(self, color: str):
        """
        Takes one parameter, 'RED' or 'BLACK', and returns the number of pieces of that color that have been captured.
        """
        if color == "BLACK":
            return 9 - self._black_pieces
        elif color == "RED":
            return 9 - self._red_pieces

    def validate_move(self, curr_row: int, curr_col: int, next_row: int, next_col:int):
        """
        Takes the piece's current position (curr_row, curr_col) and next position (next_row, next_col),
        validates the movement selected by the player, and returns True if the move is valid or False otherwise.
        """
        h_board = self._board
        # identification of active piece:
        if self._active_player == "BLACK":
            active_piece = "B "
        else:
            active_piece = "R "
        # If the game has been already WON:
        if self._game_state != 'UNFINISHED':
            return False
        # Move invalidation:
        # if the current position is not occupied by a piece of the active player
        if h_board[curr_row][curr_col] != active_piece:
            return False
        # if the next square is not empty
        if h_board[next_row][next_col] != ". ":
            return False
        # if the current square and next square are the same
        if curr_row == next_row and curr_col == next_col:
            return False
        # if the move is neither vertical or horizontal
        if curr_row != next_row and curr_col != next_col:
            return False
        # Check unobstructed horizontal movement
        if curr_row == next_row:
            if curr_col > next_col:
                step = -1
            else:
                step = 1
            for i in range(curr_col+step, next_col+step, step):
                if h_board[curr_row][i] != ". ":
                    return False
        # Check unobstructed vertical movement
        elif curr_col == next_col:
            if curr_row > next_row:
                step = -1
            else:
                step = 1
            for i in range(curr_row+step, next_row+step, step):
                if h_board[i][curr_col] != ". ":
                    return False
        return True

    def make_move(self, curr_square: str, next_square: str):
        """
        Takes the piece's current position and next position, and checks if the movement is valid.
        If the movement is valid, it moves the piece, checks and makes the capture of the other player's pieces,
        updates the state of the game (if necessary) and the active player, and returns True.
        If the movement is not valid, returns False.
        """

        # Interpretation of the algebraic notation of the board's squares
        row_pos = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8}
        col_pos = {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8}
        # Indexes of current square
        curr_row = row_pos[curr_square[0]]
        curr_col = col_pos[curr_square[1]]
        # Indexes of next square
        next_row = row_pos[next_square[0]]
        next_col = col_pos[next_square[1]]
        # Validate the move by calling validate_move method
        if not self.validate_move(curr_row, curr_col, next_row, next_col):
            return False

        h_board = self._board

        # identification of active piece:
        if self._active_player == "BLACK":
            active_piece = "B "
            inactive_piece = "R "
        else:
            active_piece = "R "
            inactive_piece = "B "
        # Move making and player turn switching:
        if self._active_player == "BLACK":
            # Change position of the piece from current to next square
            h_board[curr_row][curr_col] = ". "
            h_board[next_row][next_col] = "B "
            # Change the player's turn
            self._active_player = "RED"
        elif self._active_player == "RED":
            # Change position of the piece from current to next square
            h_board[curr_row][curr_col] = ". "
            h_board[next_row][next_col] = "R "
            # Change the player's turn
            self._active_player = "BLACK"

        # Check and make captures of pieces
        # if move is vertical
        if curr_col == next_col:
            # if move is upward
            if next_row < curr_row:
                # eval_captures_right
                self.right_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_left
                self.left_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_up
                self.up_capture(next_row, next_col, active_piece, inactive_piece)
            # if move is downward
            if next_row > curr_row:
                # eval_captures_right
                self.right_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_left
                self.left_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_down
                self.down_capture(next_row, next_col, active_piece, inactive_piece)
        # if move is horizontal
        if curr_row == next_row:
            # if move is left
            if next_col < curr_col:
                # eval_captures_up
                self.up_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_down
                self.down_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_left
                self.left_capture(next_row, next_col, active_piece, inactive_piece)
            # if move is right
            if next_col > curr_col:
                # eval_captures_up
                self.up_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_down
                self.down_capture(next_row, next_col, active_piece, inactive_piece)
                # eval_captures_right
                self.right_capture(next_row, next_col, active_piece, inactive_piece)
        # Check corner capture (upper left, lower left, upper right, lower right)
        self.corner_captures(next_row, next_col, active_piece, inactive_piece)

        # Check and update the state of the game in case a player has won
        if self._red_pieces <= 1:
            self._game_state = "BLACK_WON"
        elif self._black_pieces <= 1:
            self._game_state = "RED_WON"
        return True

    def right_capture(self, next_row: int, next_col: int, active_piece: str, inactive_piece:str):
        """
        Takes the row and column indexes of the final position of the piece moved, checks the pieces to the
        right for captures, and executes the capture.
        """
        if next_col == 8:
            return

        pos = next_col + 1
        col_pos = []
        board = self._board
        # check for other player's pieces to the right of the moved piece
        while board[next_row][pos] == inactive_piece and pos < 8:
            col_pos.append(pos)
            pos += 1
        # if the last piece of the row belongs to the current player, make the captures
        if board[next_row][pos] == active_piece:
            for idx in col_pos:
                board[next_row][idx] = ". "
                self.capture_piece(inactive_piece)
        return

    def left_capture(self, next_row: int, next_col: int, active_piece: str, inactive_piece: str):
        """
        Takes the row and column indexes of the final position of the piece moved, checks the pieces to the
        left for captures, and executes the capture.
        """
        if next_col == 0:
            return

        pos = next_col - 1
        col_pos = []
        board = self._board
        # check for other player's pieces to the right of the moved piece
        while board[next_row][pos] == inactive_piece and pos > 0:
            col_pos.append(pos)
            pos -= 1
        # if the last piece of the row belongs to the current player, make the captures
        if board[next_row][pos] == active_piece:
            for idx in col_pos:
                board[next_row][idx] = ". "
                self.capture_piece(inactive_piece)
        return

    def up_capture(self, next_row: int, next_col: int, active_piece: str, inactive_piece: str):
        """
        Takes the row and column indexes of the final position of the piece moved, checks the pieces
        upward for captures, and executes the capture.
        """
        if next_row == 0:
            return

        pos = next_row - 1
        row_pos = []
        board = self._board
        # check for other player's pieces to the right of the moved piece
        while board[pos][next_col] == inactive_piece and pos > 0:
            row_pos.append(pos)
            pos -= 1
        # if the last piece of the row belongs to the current player, make the captures
        if board[pos][next_col] == active_piece:
            for idx in row_pos:
                board[idx][next_col] = ". "
                self.capture_piece(inactive_piece)
        return

    def down_capture(self, next_row: int, next_col: int, active_piece: str, inactive_piece: str):
        """
        Takes the row and column indexes of the final position of the piece moved, checks the pieces
        downward for captures, and executes the capture.
        """
        if next_row == 8:
            return

        pos = next_row + 1
        row_pos = []
        board = self._board
        # check for other player's pieces to the right of the moved piece
        while board[pos][next_col] == inactive_piece and pos < 8:
            row_pos.append(pos)
            pos += 1
        # if the last piece of the row belongs to the current player, make the captures
        if board[pos][next_col] == active_piece:
            for idx in row_pos:
                board[idx][next_col] = ". "
                self.capture_piece(inactive_piece)
        return

    def corner_captures(self, next_row: int, next_col: int, active_piece: str, inactive_piece: str):
        """
        Takes the active player's pieces, the other player's pieces, the row and columns indexes of the final position
        of the piece moved, checks the corner for captures, and executes the capture.
        """
        h_board = self._board

        # Upper left corner
        if (next_row == 1 and next_col == 0) or (next_row == 0 and next_col == 1):
            if h_board[1][0] == active_piece and h_board[0][1] == active_piece and h_board[0][0] == inactive_piece:
                h_board[0][0] = ". "
                self.capture_piece(inactive_piece)

        # Upper right corner
        elif (next_row == 0 and next_col == 7) or (next_row == 1 and next_col == 8):
            if h_board[0][7] == active_piece and h_board[1][8] == active_piece and h_board[0][8] == inactive_piece:
                h_board[0][8] = ". "
                self.capture_piece(inactive_piece)

        # Lower left corner
        elif (next_row == 7 and next_col == 0) or (next_row == 8 and next_col == 1):
            if h_board[7][0] == active_piece and h_board[8][1] == active_piece and h_board[8][0] == inactive_piece:
                h_board[8][0] = ". "
                self.capture_piece(inactive_piece)

        # Lower right corner
        elif (next_row == 7 and next_col == 8) or (next_row == 8 and next_col == 7):
            if h_board[7][8] == active_piece and h_board[8][7] == active_piece and h_board[8][8] == inactive_piece:
                h_board[8][8] = ". "
                self.capture_piece(inactive_piece)
        return

    def get_square_occupant(self, square: str):
        """
        Takes a string representing a square (such as 'i7'), and returns 'RED', 'BLACK', or 'NONE',
        depending on whether the specified square is occupied by a red piece, a black piece, or neither.
        """
        # Interpretation of the algebraic notation of the board's squares
        row_pos = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8}
        col_pos = {'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8}
        # Indexes of square
        row = row_pos[square[0]]
        col = col_pos[square[1]]
        h_board = self._board
        if h_board[row][col] == "B ":
            return 'BLACK'
        elif h_board[row][col] == "R ":
            return 'RED'
        else:
            return 'NONE'

    def print_board(self):
        """
        Prints the current state of the game's board for debugging purposes.
        """
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                print(self._board[i][j], end='')
            print()
        return


class Board:
    """
    Represents a 9x9 Hasami Shogi Board, where two Players (Black and Red) play the Game.
    """
    def __init__(self):
        """
        Initializes the board to start playing the Hasami Shogi game, with the Red Player's pieces in the top row,
        and the Black Player's pieces in the bottom row.
        """
        rows = 9
        cols = 9
        board = [[". " for i in range(cols)] for j in range(rows)]
        for row in range(len(board)):
            for col in range(len(board[row])):
                if row == 0:
                    board[row][col] = "R "
                elif row == 8:
                    board[row][col] = "B "

        self._board = board

    def get_board(self):
        """
        Returns the list of lists (board) of the Board object.
        """
        return self._board

    def check_pos_element(self, row, col):
        """
        Checks a specific position in the board, for debugging purposes
        """
        board = self._board
        print(board[row][col])
        return


def main():
    game = HasamiShogiGame()
    moves = [ [ 'i8', 'e8' ], [ 'a7', 'h7' ], [ 'i1', 'd1' ], [ 'h7', 'h1' ], [ 'e8', 'e7' ], [ 'h1', 'i1' ],
              [ 'e7', 'a7' ], [ 'a8', 'i8' ],[ 'd1', 'b1' ], [ 'a9', 'h9' ], [ 'b1', 'b8' ], [ 'i8', 'c8' ],
              [ 'b8', 'a8' ], [ 'h9', 'a9' ]]
    for i in range(len(moves)):
        print(game.get_active_player(), moves[i][0], "to", moves[i][1])
        game.make_move(moves[i][0], moves[i][1])
        print(game.get_game_state())
        print("R captured:", game.get_num_captured_pieces("RED"))
        print("B captured:", game.get_num_captured_pieces("BLACK"))
        game.print_board()


if __name__ == '__main__':
    main()

