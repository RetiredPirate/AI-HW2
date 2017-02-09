import random
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *

##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#Variables:
#   playerId - The id of the player.
##
class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "AI_NOT_FOUND")

        
        self.enemyFood = []
        self.ourFood = []

        self.weHaveNotDoneThisBefore = True
        
    
    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters:
    #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):

        # get food lists
        if self.weHaveNotDoneThisBefore:
            foods = getConstrList(currentState, None, (FOOD,))
            for food in foods:
                if food.coords[1] > 3:
                    self.enemyFood.append(food)
                else:
                    self.ourFood.append(food)
            self.weHaveNotDoneThisBefore = False

        moves = listAllLegalMoves(currentState)
        selectedMove = moves[random.randint(0,len(moves) - 1)];

        #don't do a build move if there are already 3+ ants
        numAnts = len(currentState.inventories[currentState.whoseTurn].ants)
        while (selectedMove.moveType == BUILD and numAnts >= 3):
            selectedMove = moves[random.randint(0,len(moves) - 1)];
            
        return selectedMove
    
    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]


    #
    #
    #
    def getUtility(self, currentState):
        if self.hasWon(currentState, self.playerId):
            return 1.0
        elif self.hasWon(currentState, (self.playerId + 1) % 2):
            return 0.0

        for inv in currentState.inventories:
            if inv.player == currentState.whoseTurn:
                ourInv = inv
            else:
                enemyInv = inv

        # Range of 0.5 to 1.5
        foodUtil = (float(ourInv.foodCount) / float(ourInv.foodCount + enemyInv.foodCount))  + 0.5

        numAnts = len(ourInv.ants)
        if numAnts < 3:
            antUtil = 0.5
        elif numAnts in range(3,5):
            antUtil = 1.5
        else:
            antUtil = 1

        enemyNumAnts = len(enemyInv.ants)
        if enemyNumAnts > 6:
            enemyAntUtil = 1.5
        else:
            enemyAntUtil = (enemyNumAnts / 6) + 0.5

        utility = ( (foodUtil * antUtil * enemyAntUtil) / (1.5*1.5*1.5) ) - 0.05

        return utility





    # Register a win
    def hasWon(self, currentState, playerId):
        opponentId = (playerId + 1) % 2
        
        if ((currentState.phase == PLAY_PHASE) and 
        ((currentState.inventories[opponentId].getQueen() == None) or
        (currentState.inventories[opponentId].getAnthill().captureHealth <= 0) or
        (currentState.inventories[playerId].foodCount >= FOOD_GOAL) or
        (currentState.inventories[opponentId].foodCount == 0 and 
            len(currentState.inventories[opponentId].ants) == 1))):
            return True
        else:
            return False