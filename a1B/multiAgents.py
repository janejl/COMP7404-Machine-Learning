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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        BASE_NUMBER = 9999
        score = successorGameState.getScore()

        # take this action without consuming food
        if newFood.count() == prevFood.count():
            score -= BASE_NUMBER

        pacFoodDistances = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        minPacFoodDistance = min(pacFoodDistances) if pacFoodDistances else BASE_NUMBER
        # when ghost is very close to the pacman, raise alert level
        pacGhostDistances = [max(4 - manhattanDistance(newPos, ghostState.getPosition()), 0)**2 for ghostState in newGhostStates]

        score += 1 / minPacFoodDistance - sum(pacGhostDistances)

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

    def getAction(self, gameState):
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
        self.treeRealDepth = self.depth * gameState.getNumAgents()
        score, pacmanAction = self.MiniMax(gameState, self.treeRealDepth, 0, Directions.STOP)
        return pacmanAction

    def MiniMax(self, gameState, depth, agentIndex, pacmanAction):
        # in leaf node, return (utility value, action)
        if depth <= 0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), pacmanAction)

        results = []
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        for legalAction in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, legalAction)
            move = legalAction if agentIndex == 0 and depth == self.treeRealDepth else pacmanAction
            results.append(self.MiniMax(successor, depth - 1, nextAgentIndex, move))

        result = max(results) if agentIndex == 0 else min(results)
        return result


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.treeRealDepth = self.depth * gameState.getNumAgents()
        score, action = self.AlphaBeta(gameState, self.treeRealDepth, -float('inf'), float('inf'), 0, Directions.STOP)

        return  action

    def AlphaBeta(self, gameState, depth, alpha, beta, agentIndex, pacmanAction):
        # alpha: MAX's best option alone path to root.
        # beta: MIN's best option alone path to root.

        # in leaf node, return (utility value, action)
        if depth <= 0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), pacmanAction)

        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        if agentIndex == 0:
            v = (-float('inf'), Directions.STOP)
            for legalAction in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, legalAction)
                move = legalAction if depth == self.treeRealDepth else pacmanAction
                v = max(v, self.AlphaBeta(successor, depth - 1, alpha, beta, nextAgentIndex, move))
                alpha = max(alpha, v[0])
                if v[0] > beta:
                    # no need to explore this gameState anymore
                    return v
            return v
        else:
            v = (float('inf'), Directions.STOP)
            for legalAction in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, legalAction)
                v = min(v, self.AlphaBeta(successor, depth - 1, alpha, beta, nextAgentIndex, pacmanAction))
                beta = min(beta, v[0])
                if v[0] < alpha:
                    # no need to explore this gameState anymore
                    return v
            return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        self.treeRealDepth = self.depth * gameState.getNumAgents()
        score, pacmanAction = self.ExpectiMax(gameState, self.treeRealDepth, 0, Directions.STOP)
        return pacmanAction

    def ExpectiMax(self, gameState, depth, agentIndex, pacmanAction):
        # in leaf node, return (utility value, action)
        if depth <= 0 or gameState.isWin() or gameState.isLose():
            return (self.evaluationFunction(gameState), pacmanAction)

        results = []
        nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()

        for legalAction in gameState.getLegalActions(agentIndex):
            successor = gameState.generateSuccessor(agentIndex, legalAction)
            move = legalAction if agentIndex == 0 and depth == self.treeRealDepth else pacmanAction
            results.append(self.ExpectiMax(successor, depth - 1, nextAgentIndex, move))

        if agentIndex == 0:
            return max(results)
        else:
            return (sum([r[0] for r in results]) / len(results), pacmanAction)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>

    Case 1: if ghosts are chasing
        strategy: pacman should avoid ghosts, look for capsules (if available) and foods.
        For same distance, capsule is more important than food (to earn score in case 2)
    Case 2: if ghosts are scared
        strategy: pacman should look for ghosts and foods.

    Pacman score rules:
        - food: +10
        - capsule: 0
        - normal ghost: -500
        - scared ghost: +200 (back to normal ghost)
    """
    "*** YOUR CODE HERE ***"
    pacPos = currentGameState.getPacmanPosition()

    foodPositions = currentGameState.getFood().asList()
    ghostPositions = currentGameState.getGhostPositions()
    capsulePositions = currentGameState.getCapsules()

    BASE_NUMBER = 9999
    pacFoodDistances = [manhattanDistance(pacPos, foodPos) for foodPos in foodPositions]
    minPacFoodDistance = min(pacFoodDistances) if pacFoodDistances else BASE_NUMBER
    pacCapDistances = [manhattanDistance(pacPos, foodPos) for foodPos in capsulePositions]
    minPacCapDistance = min(pacCapDistances) if pacCapDistances else BASE_NUMBER

    if sum([ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]) == 0:
        # === Case 1: ghosts are chasing ===
        pacGhostDistances = [max(4 - manhattanDistance(pacPos, ghostPos), 0) ** 2 for ghostPos in ghostPositions]
        return currentGameState.getScore() + 1 / minPacFoodDistance + 10 / minPacCapDistance - sum(pacGhostDistances)
    else:
        # === Case 2: ghosts are scared ===
        pacGhostDistances = [manhattanDistance(pacPos, ghostPos) for ghostPos in ghostPositions]
        return currentGameState.getScore() + 1 / minPacFoodDistance + 100 / min(pacGhostDistances)

# Abbreviation
better = betterEvaluationFunction

