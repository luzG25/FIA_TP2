# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostPositions = successorGameState.getGhostPositions()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        oldPos = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood().asList()
        
        score = 0

        for ghost_pos in newGhostPositions:
          if manhattanDistance(newPos, ghost_pos) == 2:
            score -= 5000
            return score
      
        if newPos in oldFood:
          score += 50

        if oldPos == newPos:
          score -= 20
        
        newFood_distance = []
        if len(oldFood) > 0:
          for food in oldFood:
            newFood_distance.append((manhattanDistance(newPos, food), food))
          closest_food = min(newFood_distance)
          if manhattanDistance(newPos, closest_food[1]) < manhattanDistance(oldPos, closest_food[1]):
            score += 40
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def minimax(self, gameState, agentIndex, depth):
        #we start from depth 0 and increase until the self.depth
        #for two ghosts we have NumAgents == 3 and agentIndext starting from 0 will be 0,1,2
        #so when we call minimax after last agent has played we use agentIndex+1 == 3 which equals to NumAgents and we stop
        #now pacman has to play and we go one level deeper
        if agentIndex >= gameState.getNumAgents():
            depth     += 1
            agentIndex = 0

        #check if we are on depth zero or final state
        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        # agent is pacman
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        # agent is a ghost
        else:
            return self.minValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        val = -float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = max(val,self.minimax(successorGameState, agentIndex + 1, depth))
        return val
    
    def minValue(self, gameState, agentIndex, depth):
        val = float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = min(val,self.minimax(successorGameState, agentIndex + 1, depth))
        return val
    
    # we start playing with pacman and for every action that he has we need to calculate the minimax value and take the max
    def getAction(self, gameState):
        agentIndex = 0 #for pacman
        max_value = -float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = self.minimax(successorGameState, 1, 0) #call minimax for successorGameState and agent --> ghost number 1
            if val > max_value:
              max_value = val
              best_action = action
        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
      This is the same code as MinimaxAgent but now we added alpha, beta and prunning 
    """
    def alpha_beta(self, gameState, alpha, beta, agentIndex, depth):
        if agentIndex >= gameState.getNumAgents():
            depth     += 1
            agentIndex = 0

        #check if we are on depth zero or final state
        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        # agent is pacman
        if agentIndex == 0:
            return self.maxValue(gameState, alpha, beta, agentIndex, depth)
        # agent is a ghost
        else:
            return self.minValue(gameState, alpha, beta, agentIndex, depth)

    def maxValue(self, gameState, alpha, beta, agentIndex,depth):
        val = -float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = max(val, self.alpha_beta(successorGameState, alpha, beta, agentIndex + 1, depth))
            if val > beta:
              return val
            alpha = max(alpha, val)
        return val
    
    def minValue(self, gameState, alpha, beta, agentIndex,depth):
        val = float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = min(val,self.alpha_beta(successorGameState, alpha, beta, agentIndex + 1, depth))
            if val < alpha:
              return val
            beta = min(beta, val)
        return val

    def getAction(self, gameState):
        agentIndex = 0
        alpha = -float("inf")
        beta = float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = self.alpha_beta(successorGameState, alpha, beta, 1, 0)
            if val > alpha:
              alpha = val
              best_action = action
        return best_action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
      Now we don't have min players.
      We use expected value to calculate the val for ghosts
      We assume that ghosts don't play optimaly
    """
    def expectimax(self, gameState, agentIndex, depth):
        
        if agentIndex >= gameState.getNumAgents():
            depth     += 1
            agentIndex = 0

        #check if we are on depth zero or final state
        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        
        # agent is pacman
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)
        # agent is a ghost
        else:
            return self.expValue(gameState, agentIndex, depth)

    def maxValue(self, gameState, agentIndex, depth):
        val = -float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = max(val,self.expectimax(successorGameState, agentIndex + 1, depth))
        return val
    
    def expValue(self, gameState, agentIndex, depth):
        val = 0
        legalActions = gameState.getLegalActions(agentIndex)
        # every move has the same probability so the probability is
        probability = 1.0 / float(len(legalActions))
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val += probability * self.expectimax(successorGameState, agentIndex + 1, depth)
        return val

    def getAction(self, gameState):
        agentIndex = 0
        max_value = -float("inf")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            val = self.expectimax(successorGameState, 1, 0)
            if val > max_value:
              max_value = val
              best_action = action
        return best_action

import time

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: I achieved 6/6 after some trial and error and a lot of thinking
      
    Features:
    1) number of food dots - we want to have less food that's why I did 1.0/len(foodList)
    2) distance from closest food dot - again we want the distance to be as small as possible that's why we use 1.0/min(food_distances)
    3) if we are near a ghost then just run
    4) how long ghosts are scared
    """
    score = 0
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    food_distances = []
    
    for food in foodList:
        food_distances.append(manhattanDistance(pacmanPos, food))
    
    if len(food_distances) > 0:
        score += 10 * 1.0/min(food_distances)
        score += 5  * 1.0/len(foodList)
    
    ghostPositions = currentGameState.getGhostPositions()
    if manhattanDistance(pacmanPos , ghostPositions[0]) < 3:
        score -= 1000

    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    score += 10 * sum(scaredTimes)

    """
    score += 10 * 1.0 / currentGameState.getNumAgents()
    
    if currentGameState.isWin():
        score += 1000 
    
    if currentGameState.isLose():
        score -= 1000

    capsules = currentGameState.getCapsules()
    if len(capsules) > 0:
        score += 10 * 1.0/len(capsules)
    """
    return score + 100 * currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction
