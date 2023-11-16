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
from pacman import GameState
from math import inf

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newFood = successorGameState.getFood()
        newGhostPositions = successorGameState.getGhostPositions()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        oldPos = currentGameState.getPacmanPosition() # obter posiçao do pacman
        oldFood = currentGameState.getFood().asList() #obter lista das coordenadas das comidas atuais
        #print(oldFood)

        score = 0

        # distancia entre meu pacman e os ghosts:
        for ghost_pos in newGhostPositions:
            if manhattanDistance(newPos, ghost_pos) == 2:
                # se essa distancia for igual a 2, reduzir o score em 5000
                score -= 5000
                return score
            
        if newPos in oldFood: 
            # se a nova posicao possui comida
            score += 50

        if oldPos == newPos:
            # se a proxima acao levar o pacman a posicao onde ele esta atualmente
            score -= 20

        newFood_distance = [] # armazenar a distancia entre o pacman e cada comida

        if len(oldFood) > 0: 
            # caso houver mais comida
            for food in oldFood:
                newFood_distance.append((manhattanDistance(newPos, food), food)) # tupla (distancia, coordenada da comida)

            perto_food = min(newFood_distance) # comida mas perto do pacman
            #print(perto_food)

        if manhattanDistance(newPos, perto_food[1]) < manhattanDistance(oldPos, perto_food[1]):
            # se a proxima acao ficar mas perto da comida, aumentar o score 
            score += 40
        
        
        return score

def scoreEvaluationFunction(currentGameState: GameState):
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
    def minimax(self, gameState, jogadorIndex, profundidade):
        if jogadorIndex >= gameState.getNumAgents(): 
            profundidade += 1
            jogadorIndex = 0
            
        if(profundidade == self.depth or gameState.isWin() or gameState.isLose()):
            # caso seja alcançada a fundo (depth 0) ou o jogo esta ganho ou perdido
            #avaliar esta possivel estado
            return self.evaluationFunction(gameState)
        
        # se o jogador for o pacman
        if jogadorIndex == 0:
            return self.maxValue(gameState, jogadorIndex, profundidade)
        # se o jogador for o ghost
        else:
            return self.minValue(gameState, jogadorIndex, profundidade)
            
    # determinar o maximo valor
    #aplicado para as jogadas do pacman        
    def maxValue(self, gameState, jogadorIndex, profundidade):
        val = -inf # definir o val para o menor valor possivel
        
        #ver as possiveis jogadas legais do pacman, ex: se ele pode ir para esquerda, frente ou trás,
        #se ele esta com uma parede do lado esquerdo certamente 'esquerda' não é uma jogada legal
        legalActions = gameState.getLegalActions(jogadorIndex) 
        for acao in legalActions:
            
            # gerar a proximo estado do jogo caso o pacman resolver tomar essa determinada ação
            successorGameState = gameState.generateSuccessor(jogadorIndex,acao)
            
            val = max(val,self.minimax(successorGameState,jogadorIndex + 1, profundidade))
        
        return val
            
    def minValue(self,gameState,jogadorIndex,profundidade):
        val = inf # definir o val para o maior valor possivel
        
        # gerar a proximo estado do jogo caso o ghost resolver tomar essa determinada ação
        legalActions = gameState.getLegalActions(jogadorIndex)
        for action in legalActions:
            successorGameState = gameState.generateSuccessor(jogadorIndex,action)
            val = min(val,self.minimax(successorGameState,jogadorIndex + 1, profundidade))
        
        return val
            
        

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        jogadorIndex = 0 # referenciando o pacman
        max_value = -inf
        legalAction = gameState.getLegalActions(jogadorIndex)
        
        for acao in legalAction:
            sucessorGameState = gameState.generateSuccessor(jogadorIndex, acao)
            val = self.minimax(sucessorGameState, 1, 0)
            #print(val)
           
           # comparar as ações, até encontrar a  jogada que possui a o maior valor evalution 
            if val > max_value: 
                max_value = val
                melhor_acao = acao
                
        return melhor_acao 
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def alpha_beta(self, gameState, alpha, beta, jogadorIndex, profundidade):
        if jogadorIndex >= gameState.getNumAgents(): 
            profundidade += 1
            jogadorIndex = 0
            
        if(profundidade == self.depth or gameState.isWin() or gameState.isLose()):
            # caso seja alcançada a fundo (depth 0) ou o jogo esta ganho ou perdido
            #avaliar esta possivel estado
            return self.evaluationFunction(gameState)
        
        # se o jogador for o pacman
        if jogadorIndex == 0:
            return self.maxValue(gameState, alpha, beta, jogadorIndex, profundidade)
        # se o jogador for o ghost
        else:
            return self.minValue(gameState, alpha, beta, jogadorIndex, profundidade)
        
        
    
    def maxValue(self, gameState, alpha, beta, jogadorIndex, profundidade):
        v = -inf
        
        for acao in  gameState.getLegalActions(jogadorIndex):
            proxima_jogada = gameState.generateSuccessor(jogadorIndex, acao)
            v = max(v, self.alpha_beta(proxima_jogada, alpha, beta, jogadorIndex+1, profundidade))
            
            if v > beta:
                return v
            
            alpha = max(alpha, v)
        return v
        
        
    def minValue(self, gameState, alpha, beta, jogadorIndex, profundidade):
        v =  inf
        
        for acao in  gameState.getLegalActions(jogadorIndex):
            proxima_jogada = gameState.generateSuccessor(jogadorIndex, acao)
            v = min(v, self.alpha_beta(proxima_jogada, alpha, beta, jogadorIndex+1, profundidade))
            
            if v < alpha:
                return v
            
            beta = min(beta, v)
        
        return v
    


    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        jogadorIndex = 0
        alpha = -inf
        beta = inf
        
        for acao in gameState.getLegalActions(jogadorIndex):
            proximaJogada = gameState.generateSuccessor(jogadorIndex, acao)
            v = self.alpha_beta(proximaJogada, alpha, beta, 1, 0)
            
            if v > alpha:
                alpha = v
                proxima_acao = acao
                
        return proxima_acao

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, gameState, jogadorIndex, profundidade):
        if jogadorIndex >= gameState.getNumAgents(): 
            profundidade += 1
            jogadorIndex = 0
            
        if(profundidade == self.depth or gameState.isWin() or gameState.isLose()):
            # caso seja alcançada a fundo (depth 0) ou o jogo esta ganho ou perdido
            #avaliar esta possivel estado
            return self.evaluationFunction(gameState)
        
        # se o jogador for o pacman
        if jogadorIndex == 0:
            return self.maxValue(gameState, jogadorIndex, profundidade)
        # se o jogador for o ghost
        else:
            return self.expVal(gameState, jogadorIndex, profundidade)
    # determinar o maximo valor
    #aplicado para as jogadas do pacman        
    def maxValue(self, gameState, jogadorIndex, profundidade):
        val = -inf # definir o val para o menor valor possivel
        
        #ver as possiveis jogadas legais do pacman, ex: se ele pode ir para esquerda, frente ou trás,
        #se ele esta com uma parede do lado esquerdo certamente 'esquerda' não é uma jogada legal
        legalActions = gameState.getLegalActions(jogadorIndex) 
        for acao in legalActions:
            
            # gerar a proximo estado do jogo caso o pacman resolver tomar essa determinada ação
            successorGameState = gameState.generateSuccessor(jogadorIndex,acao)
            
            val = max(val,self.expectimax(successorGameState,jogadorIndex + 1, profundidade))
        
        return val
    
    def expVal(self, gameState, jogadorIndex, profundidade):
        v = 0
        acoesPossiveis = gameState.getLegalActions(jogadorIndex)
        probabilidade = 1.0 / float(len(acoesPossiveis))
        
        for acao in acoesPossiveis:
            proxima_jogada = gameState.generateSuccessor(jogadorIndex, acao)
            
            v += probabilidade * self.expectimax(proxima_jogada, jogadorIndex + 1, profundidade)
        return v


        
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        jogadorIndex = 0 # referenciando o pacman
        max_value = -inf
        legalAction = gameState.getLegalActions(jogadorIndex)
        
        for acao in legalAction:
            sucessorGameState = gameState.generateSuccessor(jogadorIndex, acao)
            val = self.expectimax(sucessorGameState, 1, 0)
            #print(val)
           
           # comparar as ações, até encontrar a  jogada que possui a o maior valor evalution 
            if val > max_value: 
                max_value = val
                melhor_acao = acao
                
        return melhor_acao 
        
       

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    dots = currentGameState.getFood().asList() # lista de todos os dots disponivel no tabuleiro para o pacman comer
    dots_distancia = [] # distancia respectiva de cada dot no jogo em  relacao ao pacman
    pacman_coor = currentGameState.getPacmanPosition() # coordenada do pacman no tabuleiro
    
    score  = 0
    
    for dot in dots:
        # popular a lista para cada dot, com a manhattanDistance entre o pacman e o dot
        dots_distancia.append(manhattanDistance(pacman_coor, dot))

    n_dots = len(dots_distancia) # numero de dots disponiveis no jogo
    if n_dots > 0:
        score +=  5 * 1.0/min(dots_distancia) # aumentar o score em 5pts para o dot mais pero
        score +=  1.0/n_dots # aumentar o score inversamente em relacao ao numero de  dots no jogo

    # para quando o modo em que o ghost vira presa
    for estado in currentGameState.getGhostStates():
        score += 2 * estado.scaredTimer # aumentar o score em 2vezes em relacao ao tempo que esta em modo presa


    ghosts_coor = currentGameState.getGhostPositions() # obter a posicao dos ghosts no tabuleiro
    dist_pac_ghost = manhattanDistance(pacman_coor, ghosts_coor[0]) # distancia entre o pacman e ghost mais perto
    if dist_pac_ghost < 3:
        score -= dist_pac_ghost * 10 # reduzir a pontuacao se a distancia entre o ghost e o pacman for menor que 3

    return (score + 100 * currentGameState.getScore()) 
    

# Abbreviation
better = betterEvaluationFunction
