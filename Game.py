import os
class Game:
    def __init__(self):
        self.generateGame()

    def generateGame(self):
        self.boardValues = [0] * 9
        self.boardGrid = "┌───┬───┬───┐\n│   │   │   │\n├───┼───┼───┤\n│   │   │   │\n├───┼───┼───┤\n│   │   │   │\n└───┴───┴───┘"
        self.turnCount = 0

    def validTurn(self, location):
        if self.boardValues[location] == 0:
            return(True)
        else:
            return(False)


    def checkWin(self):
        if self.boardValues[0] > 0 and self.boardValues[0] == self.boardValues[4] and self.boardValues[0] == self.boardValues[8]:
            return(self.boardValues[0])
        elif self.boardValues[6] > 0 and self.boardValues[6] == self.boardValues[4] and self.boardValues[6] == self.boardValues[2]:
            return(self.boardValues[6])
        else:
            for i in range(3):
                if self.boardValues[3*i] > 0 and self.boardValues[3*i] == self.boardValues[3*i + 1] and self.boardValues[3*i] == self.boardValues[3*i + 2]:
                    return(self.boardValues[3*i])
                elif self.boardValues[i] > 0 and self.boardValues[i] == self.boardValues[i + 3] and self.boardValues[i] == self.boardValues[i + 6]:
                    return(self.boardValues[i])
         
        
        if all(i > 0 for i in self.boardValues):
            return(0)
    
    def placeMarker(self, location, value):
        gridLocations = {0:16, 1:20, 2:24, 3:44, 4:48, 5:52, 6:72, 7:76, 8:80}
        self.boardValues[location] = value
        if value == 1:
            marker = 'X'
        else:
            marker = 'O'
        self.boardGrid = self.boardGrid[:gridLocations[location]] + marker + self.boardGrid[gridLocations[location] + 1:]

    def maxComputer(self):
        maxValue = -100
        maxLoc = None
        winner = self.checkWin()

        if winner == self.playerValue:
            return(-10, 0)
        elif winner == self.compValue:
            return(10, 0)
        elif winner == 0:
            return(0, 0)

        for i in range(9):
            if self.boardValues[i] == 0:
                self.boardValues[i] = self.compValue
                (min, location) = self.minPlayer()
                 
                if min > maxValue:
                     maxValue = min
                     maxLoc = i
                self.boardValues[i] = 0
        return(maxValue, maxLoc)
                

    def minPlayer(self):
        minValue = 100
        minLoc = None
        winner = self.checkWin()
        if winner == self.playerValue:
            return(-10, 0)
        elif winner == self.compValue:
            return(10, 0)
        elif winner == 0:
            return(0, 0)
        
        for i in range(9):
            if self.boardValues[i] == 0:
                self.boardValues[i] = self.playerValue
                (max, location) = self.maxComputer()
                 
                if max < minValue:
                     minValue = max
                     minLoc = i
                self.boardValues[i] = 0
        return(minValue, minLoc)

    
    def refresh(self):
        os.system('cls')
        print(self.boardGrid)

    def playGame(self):
        playerNum = int(input("Enter player number: "))
        if playerNum == 1:
            self.playerValue = 1
            self.compValue = 2
        else:
            self.playerValue = 2
            self.compValue = 1

        while True:
            self.refresh()
            winner = self.checkWin()
            if winner == 1:
                print("Player 1 wins")
                break
            elif winner == 2:
                print("Player 2 wins")
                break
            elif winner == 0:
                print("Draw")
                break
            self.turnCount += 1
            turn = self.turnCount % 2

            if playerNum == 1:
                if turn == 1:
                    while True:
                        try:
                            squareInput = int(input("Enter a square location: ")) - 1
                        except ValueError:
                            print("Invalid input, input an integer from 1 to 9")
                            continue
                        if squareInput > 8 or squareInput < 0:
                            print("Invalid input, input an integer from 1 to 9")
                        elif self.validTurn(squareInput):
                            self.placeMarker(squareInput, self.playerValue)
                            break
                        else:
                            print("Invalid input, square already occupied")
                else:
                    (max, location) = self.maxComputer()
                    self.placeMarker(location, self.compValue)
            else:
                if turn == 0:
                    while True:
                        try:
                            squareInput = int(input("Enter a square location: ")) - 1
                        except ValueError:
                            print("Invalid input, input an integer from 1 to 9")
                            continue
                        if squareInput > 8 or squareInput < 0:
                            print("Invalid input, input an integer from 1 to 9")
                        elif self.validTurn(squareInput):
                            self.placeMarker(squareInput, self.playerValue)
                            break
                        else:
                            print("Invalid input, square already occupied")
                else:
                    (max, location) = self.maxComputer()
                    self.placeMarker(location, self.compValue)
                    


