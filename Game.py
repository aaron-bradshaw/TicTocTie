import os
class Game:
    def __init__(self):
        self.generateGame()

    #Resets the initial conditions to start the game
    def generateGame(self):
        self.boardValues = [0] * 9
        self.boardGrid = "┌───┬───┬───┐\n│   │   │   │\n├───┼───┼───┤\n│   │   │   │\n├───┼───┼───┤\n│   │   │   │\n└───┴───┴───┘"
        self.turnCount = 0
    
    #Checks if the move is valid
    def validTurn(self, location):
        if self.boardValues[location] == 0:
            return(True)
        else:
            return(False)

    #Checks for game end conditions and returns the winner
    def checkWin(self):
        #Checks for right diagonal wins
        if self.boardValues[0] > 0 and self.boardValues[0] == self.boardValues[4] and self.boardValues[0] == self.boardValues[8]:
            return(self.boardValues[0])
        #Checks for left diagonal wins
        elif self.boardValues[6] > 0 and self.boardValues[6] == self.boardValues[4] and self.boardValues[6] == self.boardValues[2]:
            return(self.boardValues[6])
        else:
            for i in range(3):
                #Checks for row wins
                if self.boardValues[3*i] > 0 and self.boardValues[3*i] == self.boardValues[3*i + 1] and self.boardValues[3*i] == self.boardValues[3*i + 2]:
                    return(self.boardValues[3*i])
                #Checks for column wins                    
                elif self.boardValues[i] > 0 and self.boardValues[i] == self.boardValues[i + 3] and self.boardValues[i] == self.boardValues[i + 6]:
                    return(self.boardValues[i])
         
        #Checks for draws
        if all(i > 0 for i in self.boardValues):
            return(0)
    
    # Writes moves to data and draws to the board
    def placeMarker(self, location, value):
        #Converts from value locations to board locations
        gridLocations = {0:16, 1:20, 2:24, 3:44, 4:48, 5:52, 6:72, 7:76, 8:80}
        self.boardValues[location] = value
        
        if value == 1:
            marker = 'X'
        else:
            marker = 'O'
        #Replaces blank space with the correct marker
        self.boardGrid = self.boardGrid[:gridLocations[location]] + marker + self.boardGrid[gridLocations[location] + 1:]

    # Simulates computer turn, returns best move weight and value location
    def maxComputer(self, alpha, beta):
        maxValue = -100
        maxLoc = None

        # Assigns weights to end cases
        winner = self.checkWin()
        if winner == self.playerValue:
            return(-10, 0)
        elif winner == self.compValue:
            return(10, 0)
        elif winner == 0:
            return(0, 0)

        # Loops through all squares
        for i in range(9):
            #Continues if square is empty
            if self.boardValues[i] == 0:
                #Assigns a value
                self.boardValues[i] = self.compValue
                #passes to the player simulation
                (min, location) = self.minPlayer(alpha, beta)

                #Updates best case scenario 
                if min > maxValue:
                     maxValue = min
                     maxLoc = i
                #resets board values
                self.boardValues[i] = 0

                #Quits early if subtree is worse than any previous subtrees
                if maxValue >= beta:
                    return(maxValue, maxLoc)
                #Updates best scenerio subtree
                if maxValue > alpha:
                    alpha = maxValue
        return(maxValue, maxLoc)
                
    # simulates player turn, returns minimum weight move for player and value location 
    def minPlayer(self, alpha, beta):
        minValue = 100
        minLoc = None

        #Checks for end cases and assigns weights
        winner = self.checkWin()
        if winner == self.playerValue:
            return(-10, 0)
        elif winner == self.compValue:
            return(10, 0)
        elif winner == 0:
            return(0, 0)
        
        #Loops through all squares
        for i in range(9):
            #Continues if square is empty
            if self.boardValues[i] == 0:
                #Assign value to square
                self.boardValues[i] = self.playerValue
                #Simulate computer turn
                (max, location) = self.maxComputer(alpha, beta)

                #Updates minimum weight move 
                if max < minValue:
                     minValue = max
                     minLoc = i
                #resets board values
                self.boardValues[i] = 0

                #Exits early if subtree is worse than best previous subtree
                if minValue <= alpha:
                    return(minValue, minLoc)
                #Assigns new minimum weight subtree
                if minValue < beta:
                    beta = minValue
        return(minValue, minLoc)

    #Clears window and reprits board
    def refresh(self):
        os.system('cls')
        print(self.boardGrid)

    #Starts and manages the game
    def playGame(self):
        #Player select
        playerNum = int(input("Enter player number: "))
        if playerNum == 1:
            self.playerValue = 1
            self.compValue = 2
        else:
            self.playerValue = 2
            self.compValue = 1

        #Loops until game ends    
        while True:
            self.refresh()
            #Checks for game end
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
            
            #Increments turn counter
            self.turnCount += 1
            #Alternates player turns
            turn = self.turnCount % 2

            #Actions if player is player 1
            if playerNum == 1:
                #Player turn
                if turn == 1:
                    #Loops until valid move input
                    while True:
                        try:
                            #user input
                            squareInput = int(input("Enter a square location: ")) - 1
                        except ValueError:
                            print("Invalid input, input an integer from 1 to 9")
                            continue
                        if squareInput > 8 or squareInput < 0:
                            print("Invalid input, input an integer from 1 to 9")
                        elif self.validTurn(squareInput):
                            #Makes move for player
                            self.placeMarker(squareInput, self.playerValue)
                            break
                        else:
                            print("Invalid input, square already occupied")
                #Computer turn
                else:
                    #Calculates optimal move
                    (max, location) = self.maxComputer(-100, 100)
                    #Makes move for computer
                    self.placeMarker(location, self.compValue)

            #Action if computer is player 1        
            else:
                #Player turn
                if turn == 0:
                    #Loops until valid move is input
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
                #Computer turn
                else:
                    #Calculates optimal move
                    (max, location) = self.maxComputer(-100, 100)
                    #Makes move for computer
                    self.placeMarker(location, self.compValue)
                    