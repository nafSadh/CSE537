# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
      newFood = successorGameState.getFood()
      newGhostStates = successorGameState.getGhostStates()
      newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

      "*** YOUR CODE HERE ***"
      returnScore=float(0)
      oldFood = currentGameState.getFood()
      foodList=oldFood.asList()

      foodList.sort(lambda x,y: util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))
      foodScore=util.manhattanDistance(newPos, foodList[0])
      #print(dir(newGhostStates[0]))
      GhostPositions=[Ghost.getPosition() for Ghost in newGhostStates]
      if len(GhostPositions) ==0 : GhostScore=0
      else:
          GhostPositions.sort(lambda x,y: disCmp(x,y,newPos))
          if util.manhattanDistance(newPos, GhostPositions[0])==0: return -99
          else:
              GhostScore=2*-1.0/util.manhattanDistance(newPos, GhostPositions[0])
      if foodScore==0: returnScore=2.0+GhostScore
      else: returnScore=GhostScore+1.0/float(foodScore)

      return returnScore

def disCmp(x,y,newPos):
    if (util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))<0: return -1
    else:
        if (util.manhattanDistance(newPos, x)-util.manhattanDistance(newPos, y))>0: return 1
        else:
            return 0
	   
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
      Your mini_max agent (question 2)
    """
    def getAction(self, gameState):
      """
        Returns the mini_max action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing mini_max.

        gameState.getLegalActions(agentIndex):
          Returns a list of legal actions for an agent
          agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
          Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
          Returns the total number of agents in the game
      """
      "*** YOUR CODE HERE ***"
      actions = gameState.getLegalActions(0)
      act, v = None, float("-inf")
      for action in actions:
        val = mini_max(1, range(gameState.getNumAgents()), self.depth, gameState.generateSuccessor(0, action),self.evaluationFunction)
        if val>v:
          act,v = action, val
      print val
      return act

def mini_max(agent,agentsList,depth,state,evaluator):
  """
  mini_max function
  """
  if depth == 0 or state.isWin() or state.isLose():
    return evaluator(state)
  # Based on the value of the agent call the minimiser or maximiser
  optimizer = max if agent == 0 else min
  nextDepth = depth - 1 if agent == agentsList[-1] else depth
  nextAgent = agentsList[(agent+1) % len(agentsList)]
  return optimizer([mini_max(nextAgent, agentsList, nextDepth,
                       state.generateSuccessor(agent,act), evaluator)
               for act in state.getLegalActions(agent)])
   	
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your mini_max agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the mini_max action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = float("-inf"), float("inf")
        act, v = None, alpha
        actions = gameState.getLegalActions(0)
        if Directions.STOP in actions: actions.remove(Directions.STOP)
        print v
        for action in actions:
          print action
          val = alpha_beta(1, range(gameState.getNumAgents()), alpha, beta,
                           self.depth, gameState.generateSuccessor(0, action),
                           self.evaluationFunction)
          print val
          if val > v:
            print "p:", action
            act, v = action, val
          #if v > beta:
          #  return action
          alpha = max(alpha, v)
        return act

def alpha_beta(agent, agentsList, alpha, beta, depth, state, evaluator):
  if depth==0 or state.isWin() or state.isLose():
    return evaluator(state)

  optimizer = max if agent == 0 else min
  nextDepth = depth - 1 if agent == agentsList[-1] else depth
  nextAgent = agentsList[(agent+1) % len(agentsList)]

  val = float("-inf") if agent==0 else float("inf")

  for act in state.getLegalActions(agent):
    if act != Directions.STOP:
      val = optimizer(val,
                      alpha_beta(nextAgent, agentsList, alpha, beta, nextDepth,
                                 state.generateSuccessor(agent,act), evaluator)
                      )
      if agent == 0:
        if val > beta: return val
        alpha = optimizer(alpha, val)
      else :
        if val < alpha: return val
        beta = optimizer(beta, val)

  return val


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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

