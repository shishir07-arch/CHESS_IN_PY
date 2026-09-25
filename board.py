indexLetters = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
Lettersindex = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
rankToRow = {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7}


class Board:

    def __init__(self):
        self.board = self.createBoard()

        self.whiteKingPos = ("e", 1)
        self.blackKingPos = ("e", 8)

        self.turn = 1

        self.moveFunctions = {
            "P": self.whitePawnValidation,
            "p": self.blackPawnValidation,
            "R": self.rookLogic,
            "r": self.rookLogic,
            "N": self.knightLogic,
            "n": self.knightLogic,
            "B": self.bishopLogic,
            "b": self.bishopLogic,
            "Q": self.queenLogic,
            "q": self.queenLogic,
            "K": self.kingLogic,
            "k": self.kingLogic,
        }

    def createBoard(self):
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

    def printBoard(self):
        for row in self.board:
            print(row)

    def movePiece(self, letter, number, newLetter, newNumber):

        if letter not in indexLetters or newLetter not in indexLetters:
            print("INVALID FILE")
            return False

        if number not in rankToRow or newNumber not in rankToRow:
            print("INVALID RANK")
            return False

        piece = self.board[rankToRow[number]][indexLetters[letter]]

        if piece.isupper() and self.turn == 0:
            print("Not Your Turn")
            return False

        if piece.islower() and self.turn == 1:
            print("Not Your Turn")
            return False

        if piece == ".":
            print("NO PIECE EXISTS")
            return False

        valid = None

        if piece == "P":
            valid = self.whitePawnValidation(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        elif piece == "p":
            valid = self.blackPawnValidation(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        elif piece in ("R", "r"):
            valid = self.rookLogic(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        elif piece in ("n", "N"):
            valid = self.knightLogic(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        elif piece in ("k", "K"):
            valid = self.kingLogic(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        elif piece in ("b", "B"):
            valid = self.bishopLogic(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        elif piece in ("q", "Q"):
            valid = self.queenLogic(letter, number, newLetter, newNumber)

            if valid:
                valid = self.isMoveLegal(letter, number, newLetter, newNumber)

            if valid:
                self._executeMove(letter, number, newLetter, newNumber)

        if valid:
            self.turn = not self.turn

        return valid

    def getPieceMoves(self, letter, number):
        piece = self.board[rankToRow[number]][indexLetters[letter]]
        valid_moves = []
        functionOfPiece = self.moveFunctions[piece]

        for newNumber in range(1, 9):
            for newLetter in indexLetters:

                endRow = rankToRow[newNumber]
                endCol = indexLetters[newLetter]

                valid = functionOfPiece(letter, number, newLetter, newNumber)

                if valid:
                    valid_moves.append((letter, number, newLetter, newNumber))
        return valid_moves

    def isMoveLegal(self, letter, number, newLetter, newNumber):
        oldBoard = [row[:] for row in self.board]
        oldWhiteKingPos = self.whiteKingPos
        oldBlackKingPos = self.blackKingPos

        # Make the move temporarily
        self._executeMove(letter, number, newLetter, newNumber)

        # Figure out whose king we need to check
        piece = oldBoard[rankToRow[number]][indexLetters[letter]]

        if piece.isupper():
            legal = not self.isInCheck("White")
        else:
            legal = not self.isInCheck("Black")

        # Restore the original position
        self.board = oldBoard
        self.whiteKingPos = oldWhiteKingPos
        self.blackKingPos = oldBlackKingPos

        return legal

    def getLegalMoves(self, letter, number):
        possible_moves = self.getPieceMoves(letter, number)
        legal_moves = []

        for move in possible_moves:
            if self.isMoveLegal(move[0], move[1], move[2], move[3]):
                legal_moves.append(move)
        return legal_moves

    def _executeMove(self, letter, number, newLetter, newNumber):
        piece = self.board[rankToRow[number]][indexLetters[letter]]

        self.board[rankToRow[newNumber]][indexLetters[newLetter]] = piece
        self.board[rankToRow[number]][indexLetters[letter]] = "."

        if piece == "K":
            self.whiteKingPos = (newLetter, newNumber)
        elif piece == "k":
            self.blackKingPos = (newLetter, newNumber)

    def isSquareAttacked(self, letter, number, side):

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece == ".":
                    continue

                if side == "White" and not piece.isupper():
                    continue

                if side == "Black" and not piece.islower():
                    continue

                piece_letter = Lettersindex[col]
                piece_number = 8 - row

                if piece in ("P", "p"):

                    if piece == "P":
                        attackNumber = piece_number + 1
                    else:
                        attackNumber = piece_number - 1

                    attackCols = [col - 1, col + 1]

                    for attackCol in attackCols:
                        if 0 <= attackCol < 8:
                            attackLetter = Lettersindex[attackCol]

                            if attackLetter == letter and attackNumber == number:
                                return True

                    continue

                moves = self.getPieceMoves(piece_letter, piece_number)

                for move in moves:
                    if move[2] == letter and move[3] == number:
                        return True

        return False

    def isInCheck(self, side):

        if side == "White":
            letter, number = self.whiteKingPos
            return self.isSquareAttacked(letter, number, "Black")

        elif side == "Black":
            letter, number = self.blackKingPos
            return self.isSquareAttacked(letter, number, "White")

        return False

    def whitePawnValidation(self, letter, number, newLetter, newNumber):

        # Check starting position contains a white pawn
        if self.board[rankToRow[number]][indexLetters[letter]] != "P":

            return False

        # Check bounds
        if newNumber < 1 or newNumber > 8:

            return False

        if newLetter not in indexLetters:

            return False

        startCol = indexLetters[letter]
        newCol = indexLetters[newLetter]

        row = rankToRow[newNumber]
        col = indexLetters[newLetter]

        destination = self.board[row][col]

        # Moving forward one square
        if newLetter == letter and newNumber == number + 1:

            if destination == ".":

                return True

            else:

                return False

        # Moving forward two squares from starting position
        if number == 2 and newLetter == letter and newNumber == 4:

            middleSquare = self.board[rankToRow[3]][startCol]

            if middleSquare == "." and destination == ".":

                return True

            else:

                return False

        # Capturing diagonally
        if newNumber == number + 1 and abs(newCol - startCol) == 1:

            if destination != "." and destination.islower():  # black piece

                return True

            else:

                return False

        return False

    def blackPawnValidation(self, letter, number, newLetter, newNumber):

        # Check starting position contains a white pawn
        if self.board[rankToRow[number]][indexLetters[letter]] != "p":

            return False

        # Check bounds
        if newNumber < 1 or newNumber > 8:

            return False

        if newLetter not in indexLetters:

            return False

        startCol = indexLetters[letter]
        newCol = indexLetters[newLetter]

        row = rankToRow[newNumber]
        col = indexLetters[newLetter]

        destination = self.board[row][col]

        # Moving forward one square
        if newLetter == letter and newNumber == number - 1:

            if destination == ".":

                return True

            else:

                return False

        # Moving forward two squares from starting position
        if number == 7 and newLetter == letter and newNumber == 5:

            middleSquare = self.board[rankToRow[6]][startCol]

            if middleSquare == "." and destination == ".":

                return True

            else:

                return False

        # Capturing diagonally
        if newNumber == number - 1 and abs(newCol - startCol) == 1:

            if destination != "." and destination.isupper():  # black piece

                return True

            else:

                return False

        return False

    def rookLogic(self, letter, number, newLetter, newNumber):

        piece = self.board[rankToRow[number]][indexLetters[letter]]

        if piece not in ["R", "r"]:

            return False

        startRow = rankToRow[number]
        endRow = rankToRow[newNumber]

        startCol = indexLetters[letter]
        endCol = indexLetters[newLetter]

        target = self.board[endRow][endCol]

        # Can't capture own piece
        if target != ".":
            if piece.isupper() == target.isupper():

                return False

        # Must move in one direction only
        if startRow != endRow and startCol != endCol:

            return False

        # Horizontal move
        if startRow == endRow:

            step = 1 if endCol > startCol else -1

            for col in range(startCol + step, endCol, step):
                if self.board[startRow][col] != ".":

                    return False

        # Vertical move
        else:

            step = 1 if endRow > startRow else -1

            for row in range(startRow + step, endRow, step):
                if self.board[row][startCol] != ".":

                    return False

        return True

    def bishopLogic(self, letter, number, newLetter, newNumber):

        if newLetter not in indexLetters or newNumber not in rankToRow:
            return False

        startRow = rankToRow[number]
        endRow = rankToRow[newNumber]

        startCol = indexLetters[letter]
        endCol = indexLetters[newLetter]

        piece = self.board[startRow][startCol]

        if piece not in ["B", "b"]:
            return False

        target = self.board[endRow][endCol]

        # Can't capture own piece
        if target != "." and piece.isupper() == target.isupper():
            return False

        # Must move diagonally
        if abs(startRow - endRow) != abs(startCol - endCol):
            return False

        rowStep = 1 if endRow > startRow else -1
        colStep = 1 if endCol > startCol else -1

        r = startRow + rowStep
        c = startCol + colStep

        while r != endRow:
            if self.board[r][c] != ".":
                return False

            r += rowStep
            c += colStep

        return True

    def queenLogic(self, letter, number, newLetter, newNumber):
        if newLetter not in indexLetters or newNumber not in rankToRow:
            return False

        startRow = rankToRow[number]
        endRow = rankToRow[newNumber]
        startCol = indexLetters[letter]
        endCol = indexLetters[newLetter]

        piece = self.board[startRow][startCol]
        target = self.board[endRow][endCol]

        if piece not in ["Q", "q"]:
            return False

        if target != "." and piece.isupper() == target.isupper():
            return False

        # diagonally
        if abs(startRow - endRow) == abs(startCol - endCol):
            rowStep = 1 if endRow > startRow else -1
            colStep = 1 if endCol > startCol else -1

            r = startRow + rowStep
            c = startCol + colStep

            while r != endRow:
                if self.board[r][c] != ".":

                    return False
                r += rowStep
                c += colStep

        # Horizontal move
        elif startRow == endRow:

            step = 1 if endCol > startCol else -1

            for col in range(startCol + step, endCol, step):
                if self.board[startRow][col] != ".":
                    return False

        # Vertical move
        elif startCol == endCol:

            step = 1 if endRow > startRow else -1

            for row in range(startRow + step, endRow, step):
                if self.board[row][startCol] != ".":

                    return False

        else:
            return False

        return True

    def knightLogic(self, letter, number, newLetter, newNumber):
        if newLetter not in indexLetters or newNumber not in rankToRow:
            return False

        startRow = rankToRow[number]
        endRow = rankToRow[newNumber]
        startCol = indexLetters[letter]
        endCol = indexLetters[newLetter]

        target = self.board[endRow][endCol]
        piece = self.board[startRow][startCol]

        if piece not in ["n", "N"]:
            return False

        valid = False
        if abs(startCol - endCol) == 2 and abs(endRow - startRow) == 1:
            valid = True
        elif abs(startRow - endRow) == 2 and abs(endCol - startCol) == 1:
            valid = True

        if not valid:
            return False

        # Now check the target piece
        target = self.board[endRow][endCol]
        if target != "." and target.isupper() == piece.isupper():
            return False

        return True

    def kingLogic(self, letter, number, newLetter, newNumber):

        if newLetter not in indexLetters or newNumber not in rankToRow:
            return False

        startRow = rankToRow[number]
        endRow = rankToRow[newNumber]
        startCol = indexLetters[letter]
        endCol = indexLetters[newLetter]

        target = self.board[endRow][endCol]
        piece = self.board[startRow][startCol]

        if piece not in ["k", "K"]:
            return False

        valid = False
        if endCol == startCol and abs(startRow - endRow) == 1:
            valid = True

        elif endRow == startRow and abs(startCol - endCol) == 1:
            valid = True

        elif abs(startRow - endRow) == 1 and abs(startCol - endCol) == 1:
            valid = True

        if not valid:
            return False

        if target != "." and target.isupper() == piece.isupper():
            return False

        return True

    def resetBoard(self):
        self.board = self.createBoard()
        self.printBoard()
