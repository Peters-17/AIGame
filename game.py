import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        drop_phase = True   # detect drop phase
        counter = 0
        for row in state:
            for cell in row:
                if cell == 'r' or cell == 'b':
                    counter += 1
        if counter >= 8:
            drop_phase = False

        if not drop_phase:
            # choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            move = [(-1, -1), (-1, -1)]
            # let depth = 3
            newState = self.minimax(state, 0, 'max')[1]
            for i in range(5):
                for j in range(5):
                    if state[i][j] != newState[i][j]:
                        if newState[i][j] == ' ':
                            move[1] = (i, j)
                        else:
                            move[0] = (i, j)
            return move

        # select an unoccupied space randomly
        # implement a minimax algorithm to play better
        move = []
        newState = self.minimax(state, 0, 'max')[1]
        for i in range(5):
            for j in range(5):
                if state[i][j] != newState[i][j]:
                    move.append((i, j))
                    return move
        return move

    def minimax(self, state, depth, type):
        if self.game_value(state) != 0:
            return self.game_value(state), state
        # we assume depth = 3 in make_move
        if depth == 3:
            return self.heuristic_game_value(state), state
        output = []
        succs = self.succ(state)
        if type == 'max':
            for s in succs:
                # recursively call and increase depth until get 3
                output.append(self.minimax(s, depth + 1, 'min')[0])
                maxValue = max(output)
                maxIndex = output.index(maxValue)
            return output[maxIndex], succs[maxIndex]
        else:
            for s in succs:
                # recursively call and increase depth until get 3
                output.append(self.minimax(s, depth + 1, 'max')[0])
                minValue = min(output)
                minIndex = output.index(minValue)
            return output[minIndex], succs[minIndex]

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == \
                        state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # check / diagonal wins
        for row in range(2):
            for col in range(4, 2, -1):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == \
                        state[row + 3][col - 3]:
                    return 1 if state[row][col] == self.my_piece else -1
        # check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == \
                        state[row+1][col] == state[row][col+1]:
                    return 1 if state[row][col] == self.my_piece else -1
        return 0  # no winner yet

    def heuristic_game_value(self, state):
        output = self.game_value(state)
        if output != 0:
            return output
        humanScore = 0
        AIScore = 0
        for i in range(1, 4):
            for j in range(1, 4):
                if state[i][j] == self.my_piece:
                    if state[i-1][j] == self.my_piece:
                        humanScore += 2
                    if state[i-1][j+1] == self.my_piece:
                        humanScore += 1
                    if state[i-1][j-1] == self.my_piece:
                        humanScore += 1
                    if state[i][j+1] == self.my_piece:
                        humanScore += 2
                    if state[i][j-1] == self.my_piece:
                        humanScore += 2
                    if state[i+1][j] == self.my_piece:
                        humanScore += 2
                    if state[i+1][j+1] == self.my_piece:
                        humanScore += 1
                    if state[i+1][j-1] == self.my_piece:
                        humanScore += 1
                    output -= humanScore/12
                    humanScore = 0
                if state[i][j] == self.opp:
                    if state[i-1][j] == self.opp:
                        AIScore += 2
                    if state[i-1][j+1] == self.opp:
                        AIScore += 1
                    if state[i-1][j-1] == self.opp:
                        AIScore += 1
                    if state[i][j+1] == self.opp:
                        AIScore += 2
                    if state[i][j-1] == self.opp:
                        AIScore += 2
                    if state[i+1][j] == self.opp:
                        AIScore += 2
                    if state[i+1][j+1] == self.opp:
                        AIScore += 1
                    if state[i+1][j-1] == self.opp:
                        AIScore += 1
                    output += AIScore/12
                    AIScore = 0
        return output

    def succ(self, state):
        output = []
        drop_phase = True
        counter = 0
        for row in state:
            for cell in row:
                if cell == 'r' or cell == 'b':
                    counter += 1
        if counter >= 8:
            drop_phase = False
        if drop_phase:
            emptyLocation = []
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        emptyLocation.append([row, col])
            for m in emptyLocation:
                newState = copy.deepcopy(state)
                newState[m[0]][m[1]] = self.my_piece
                output.append(newState)
        else:
            myLocation = []
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        myLocation.append([row, col])
            for i in myLocation:
                movement = []
                newState = copy.deepcopy(state)
                newState[i[0]][i[1]] = ' '
                move = [[i[0]-1, i[1]-1], [i[0]-1, i[1]], [i[0]-1, i[1]+1], [i[0], i[1]-1],
                        [i[0], i[1]+1], [i[0]+1, i[1]-1], [i[0]+1, i[1]], [i[0]+1, i[1]+1]]
                for j in range(8):
                    if 0 <= move[j][0] <= 4 and 0 < move[j][1] <= 4 and newState[move[j][0]][move[j][1]] == ' ':
                        movement.append(move[j])
                for k in movement:
                    temp = copy.deepcopy(newState)
                    temp[k[0]][k[1]] = self.my_piece
                    output.append(temp)
        return output


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
