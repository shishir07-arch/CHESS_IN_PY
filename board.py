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
        self.board[rankToRow[newNumber]][indexLetters[newLetter]] = self.board[rankToRow[number]][indexLetters[letter]] 
        self.board[rankToRow[number]][indexLetters[letter]] = "."
        self.printBoard()
    def resetBoard(self):
        self.board = self.createBoard()
        self.printBoard()
    

game = Board()
#game.printBoard()
#game.movePiece("a",2,"a",3)
# game2 = Board()
# game2.printBoard()
game.resetBoard()