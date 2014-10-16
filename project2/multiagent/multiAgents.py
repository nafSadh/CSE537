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
from random import randint
from pacman import GameState
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
      successorGameState = currentGameState.generatePacmanSuccessor(action)
      curFood = currentGameState.getFood()
      curFoodList = curFood.asList()
      curPos = currentGameState.getPacmanPosition()
      newPos = successorGameState.getPacmanPosition()
      newFood = successorGameState.getFood()
      newGhostStates = successorGameState.getGhostStates()
      newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
      newFoodList = newFood.asList()

      ghostPositions = successorGameState.getGhostPositions()
      distance = float("inf")
      scared = newScaredTimes[0] > 0
      for ghost in ghostPositions:
        d = manhattanDistance(ghost, newPos)
        distance = min(d, distance)

      distance2 = float("inf")
      distance3 = float("-inf")
      distance4 = float("inf")
      for food in newFoodList:
        d = manhattanDistance(food, newPos)
        d0 = manhattanDistance(food, curPos)
        distance2 = min(d, distance2)
        distance3 = max(d, distance3)

      cond = len(newFoodList) < len(curFoodList)
      count = len(newFoodList)
      if cond:
        count = 10000
      if distance < 2:
        distance = -100000
      else:
        distance = 0
      if count == 0:
        count = -1000
      if scared:
        distance = 0
      return distance + 1.0/distance2 + count - successorGameState.getScore()
	   
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

def smartScorer(currentGameState):
    if not isinstance(currentGameState, GameState):
      return scoreEvaluationFunction(currentGameState)

    foodList = currentGameState.getFood().asList()
    distances = [manhattanDistance(currentGameState.getPacmanPosition(),pos)
                 for pos in foodList]
    nearestFoodDistance = 0 if len(distances)<1 else min(distances)
    bonus = len(currentGameState.getCapsules())*37
    return currentGameState.getScore()+(
      -nearestFoodDistance-bonus+len(currentGameState.getLegalPacmanActions())
      )


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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2', profile = False):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.profile = profile

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
      count=[0]
      #if len(actions)>1 and Directions.STOP in actions: actions.remove(Directions.STOP)
      options = [(action,
                  mini_max(1, range(gameState.getNumAgents()), self.depth,
                           gameState.generateSuccessor(0, action),self.evaluationFunction,
                           count))
                 for action in actions]
      act, val = options[0]
      for (a,v) in options: val = max(val, v)

      choices = []
      for (a,v) in options:
        if v==val:
          choices.append(a)

      if self.profile: print "total", count[0],"nodes expanded"
      return choices[randint(1,len(choices)) -1]

def mini_max(agent,agentsList,depth,state,evaluator,nc):
  """
  mini_max function
  """
  nc[0]=nc[0]+1
  if depth == 0 or state.isWin() or state.isLose():
    return evaluator(state)
  # Based on the value of the agent call the minimiser or maximiser
  optimizer = max if agent == 0 else min
  nextDepth = depth - 1 if agent == agentsList[-1] else depth
  nextAgent = agentsList[(agent+1) % len(agentsList)]
  return optimizer([mini_max(nextAgent, agentsList, nextDepth,
                       state.generateSuccessor(agent,act), evaluator,nc)
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
    actions = gameState.getLegalActions(0)
    if len(actions)>1 and Directions.STOP in actions: actions.remove(Directions.STOP)
    options=[]
    count = [0]
    mmcnt = [0]

    if self.profile:
      for action in actions:
        mini_max(1, range(gameState.getNumAgents()), self.depth,
                 gameState.generateSuccessor(0, action),self.evaluationFunction,
                 mmcnt)

    for action in actions:
      v = alpha_beta(1, range(gameState.getNumAgents()), alpha, beta,
                       self.depth, gameState.generateSuccessor(0, action),
                       self.evaluationFunction, count)
      options.append((action,v))
      alpha = max(alpha, v)

    choices = []
    for (a,v) in options:
      if v==alpha:
        choices.append(a)

    if self.profile: print (count[0]*100/mmcnt[0]),"%\t",count[0],"\t",mmcnt[0]
    return choices[randint(1,len(choices)) -1]

def alpha_beta(agent, agentsList, alpha, beta, depth, state, evaluator, nc):
  nc[0]=nc[0]+1
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
                                 state.generateSuccessor(agent,act), evaluator
                                 ,nc)
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

