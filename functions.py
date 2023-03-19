"""Adds functionality to checkers game."""

class GameState(): #class creates template for object, object is things with attributes 
    def __init__(self):
        self.board: list[list[str]]= [ # this is the board.
            ["..", "w", "..", "w", "..", "w", "..", "w"],
            ["w", "..", "w", "..", "w", "..", "w", ".."],
            ["..", "w", "..", "w", "..", "w", "..", "w"],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["b", "..", "b", "..", "b", "..", "b", ".."],
            ["..", "b", "..", "b", "..", "b", "..", "b"],
            ["b", "..", "b", "..", "b", "..", "b", ".."]
        ]

        self.blackTurn: bool = True
        self.gamelog = []
        self.captures = []

    def makeMove(self, move):        
        if move.jump:
            captureLocation = self.board[abs(move.startrow + move.endrow) // 2][abs(move.startcolumn + move.endcolumn) // 2]
            self.captures.append(captureLocation)
            self.board[abs(move.startrow + move.endrow) // 2][abs(move.startcolumn + move.endcolumn) // 2] = ".."
            
        self.board[move.startrow][move.startcolumn] = ".."
        self.board[move.endrow][move.endcolumn] = move.piece

        if move.promo:
            self.board[move.endrow][move.endcolumn] = move.piece + "K"


        self.gamelog.append(move)

        if not move.jump:
            self.blackTurn = not self.blackTurn
        tempMoves = self.legalMoves()

        if self.legalMoves() == []:
            self.blackTurn = not self.blackTurn

    def undoMove(self):
        if len(self.gamelog) >= 1:
            lastmove = self.gamelog[len(self.gamelog) - 1]
            self.board[lastmove.startrow][lastmove.startcolumn] = lastmove.piece
            self.board[lastmove.endrow][lastmove.endcolumn] = ".."

            if lastmove.jump:
                    self.board[abs(lastmove.startrow + lastmove.endrow) // 2][abs(lastmove.startcolumn + lastmove.endcolumn) // 2] = self.captures[len(self.captures) - 1]


            self.gamelog.pop(len(self.gamelog) - 1)
            self.blackTurn = not self.blackTurn

    def legalMoves(self):
        moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                piece = self.board[row][column]
                if ((piece == "b" or piece == "bK") and self.blackTurn):
                    self.blackMoves(moves, row, column, piece)
                elif ((piece == "w" or piece == "wK") and not self.blackTurn):
                    self.whiteMoves(moves, row, column, piece)

        if len(self.gamelog) >= 1:
            lastmove = self.gamelog[len(self.gamelog) - 1]
            if self.blackTurn:
                if lastmove.jump and (lastmove.piece == "b" or lastmove.piece == "bK"):
                    for i in range(len(moves) - 1, -1, -1):
                        if moves[i].startrow != lastmove.endrow or moves[i].startcolumn != lastmove.endcolumn or moves[i].jump == False:
                            moves.pop(i)
            else:
                if lastmove.jump and (lastmove.piece == "w" or lastmove.piece == "wK"):
                    for i in range(len(moves) - 1, -1, -1):
                        if moves[i].startrow != lastmove.endrow or moves[i].startcolumn != lastmove.endcolumn or moves[i].jump == False:
                            moves.pop(i)
                
        return moves

    def blackMoves(self, moves, row, column, piece):
        if column + 1 <= 7 and row - 1 >= 0:
            if self.board[row - 1][column + 1] == "..":
                moves.append(Move((row, column), (row - 1, column + 1), self.board))

        if column + 2 <= 7 and row - 2 >= 0:
            if (self.board[row - 1][column + 1] == "w" or self.board[row - 1][column + 1] == "wK") and self.board[row - 2][column + 2] == "..":
                moves.append(Move((row, column), (row - 2, column + 2), self.board, True))

        if column - 1 >= 0 and row - 1 >= 0:
            if self.board[row - 1][column - 1] == "..":
                moves.append(Move((row, column), (row - 1, column - 1), self.board))
        
        if column - 2 >= 0 and row - 2 >= 0:
            if (self.board[row - 1][column - 1] == "w" or self.board[row - 1][column - 1] == "wK") and self.board[row - 2][column - 2] == "..":
                moves.append(Move((row, column), (row - 2, column - 2), self.board, True))

        if piece == "bK":

            if column + 1 <= 7 and row + 1 <= 7:
                if self.board[row + 1][column + 1] == "..":
                  moves.append(Move((row, column), (row + 1, column + 1), self.board))
            
            if column + 2 <= 7 and row + 2 <= 7:
                if (self.board[row + 1][column + 1] == "w" or self.board[row + 1][column + 1] == "wK") and self.board[row + 2][column + 2] == "..":
                    moves.append(Move((row, column), (row + 2, column + 2), self.board, True))

            if column - 1 >= 0 and row + 1 <= 7:
                if self.board[row + 1][column - 1] == "..":
                    moves.append(Move((row, column), (row + 1, column - 1), self.board))

            if column - 2 >= 0 and row + 2 <= 7:
                if (self.board[row + 1][column - 1] == "w" or self.board[row + 1][column - 1] == "wK") and self.board[row + 2][column - 2] == "..":
                    moves.append(Move((row, column), (row + 2, column - 2), self.board, True))

        
    def whiteMoves(self, moves, row, column, piece):
        if column + 1 <= 7 and row + 1 <= 7:
            if self.board[row + 1][column + 1] == "..":
                moves.append(Move((row, column), (row + 1, column + 1), self.board))
            
        if column + 2 <= 7 and row + 2 <= 7:
            if (self.board[row + 1][column + 1] == "b" or self.board[row + 1][column + 1] == "bK") and self.board[row + 2][column + 2] == "..":
                moves.append(Move((row, column), (row + 2, column + 2), self.board, True))

        if column - 1 >= 0 and row + 1 <= 7:
            if self.board[row + 1][column - 1] == "..":
                moves.append(Move((row, column), (row + 1, column - 1), self.board))
        
        if column - 2 >= 0 and row + 2 <= 7:
            if (self.board[row + 1][column - 1] == "b" or self.board[row + 1][column - 1] == "bK") and self.board[row + 2][column - 2] == "..":
                moves.append(Move((row, column), (row + 2, column - 2), self.board, True))

        if piece == "wK":

            if column + 1 <= 7 and row - 1 >= 0:
                if self.board[row - 1][column + 1] == "..":
                    moves.append(Move((row, column), (row - 1, column + 1), self.board))

            if column + 2 <= 7 and row - 2 >= 0:
                if (self.board[row - 1][column + 1] == "b" or self.board[row - 1][column + 1] == "bK") and self.board[row - 2][column + 2] == "..":
                    moves.append(Move((row, column), (row - 2, column + 2), self.board, True))

            if column - 1 >= 0 and row - 1 >= 0:
                if self.board[row - 1][column - 1] == "..":
                    moves.append(Move((row, column), (row - 1, column - 1), self.board))
            
            if column - 2 >= 0 and row - 2 >= 0:
                if (self.board[row - 1][column - 1] == "b" or self.board[row - 1][column - 1] == "bK") and self.board[row - 2][column - 2] == "..":
                    moves.append(Move((row, column), (row - 2, column - 2), self.board, True))
                




class Move():
    
    def __init__(self, startpos, endpos, board, jump = False):
        self.startrow = startpos[0]
        self.startcolumn = startpos[1]
        self.endrow = endpos[0]
        self.endcolumn = endpos[1]
        self.piece = board[self.startrow][self.startcolumn]
        self.jump = jump
        self.promo = False
        if (self.piece == "b" and self.endrow == 0) or (self.piece == "w" and self.endrow == 7):
            self.promo = True

    def __eq__(self, other):
        if isinstance(other, Move):
            return other.startrow == self.startrow and other.startcolumn == self.startcolumn \
                and other.endrow == self.endrow and other.endcolumn == self.endcolumn
        return False