indexLetters ={"a" : 0, "b" : 1 , "c" : 2 , "d" : 3 , "e" : 4 , "f" : 5 , "g" : 6 , "h" : 7}
rankToRow = {8: 0,7: 1,6: 2,5: 3,4: 4,3: 5,2: 6,1: 7}


class Board:
    def __init__(self):
        self.board = self.createBoard()

    def createBoard(self):
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["."] * 8,
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]

        
    def printBoard(self):
        for row in self.board:
            print(row)

    def movePiece(self, letter, number, newLetter, newNumber):

        if self.board[rankToRow[number]][indexLetters[letter]] == "." :
            print("NO PIECE EXISTS")
            return
        
        else:
            self.board[rankToRow[newNumber]][indexLetters[newLetter]] = self.board[rankToRow[number]][indexLetters[letter]] 
            self.board[rankToRow[number]][indexLetters[letter]] = "."
            self.printBoard()

    def whitePawnValidation(self, letter, number, newLetter, newNumber):

    # Check starting position contains a white pawn
        if self.board[rankToRow[number]][indexLetters[letter]] != "P":
            print("NO WHITE PAWN EXISTS")
            return False

        # Check bounds
        if newNumber < 1 or newNumber > 8:
            print("INVALID")
            return False

        if newLetter not in indexLetters:
            print("INVALID")
            return False

        startCol = indexLetters[letter]
        newCol = indexLetters[newLetter]

        row = rankToRow[newNumber]
        col = indexLetters[newLetter]

        destination = self.board[row][col]

        # Moving forward one square
        if newLetter == letter and newNumber == number + 1:

            if destination == ".":
                print("VALID")
                self.movePiece(letter, number, newLetter, newNumber)
                return True

            else:
                print("INVALID")
                return False


        # Moving forward two squares from starting position
        if number == 2 and newLetter == letter and newNumber == 4:

            middleSquare = self.board[rankToRow[3]][startCol]

            if middleSquare == "." and destination == ".":
                print("VALID")
                self.movePiece(letter, number, newLetter, newNumber)
                return True

            else:
                print("INVALID")
                return False


        # Capturing diagonally
        if newNumber == number + 1 and abs(newCol - startCol) == 1:

            if destination != "." and destination.islower():  # black piece
                print("VALID")
                self.movePiece(letter, number, newLetter, newNumber)
                return True

            else:
                print("INVALID")
                return False


        print("INVALID")
        return False

    def resetBoard(self):
        self.board = self.createBoard()
        self.printBoard()
    

game = Board()
#game.printBoard()
game.movePiece("a",2,"a",3)
# game2 = Board()
# game2.printBoard()
#game.resetBoard()