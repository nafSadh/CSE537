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
      newGhostStates = successorGameState.getGhostStates()
      newFoodList = newFood.asList()

      #find nearest ghost
      ghostPositions = successorGameState.getGhostPositions()
      distance = float("inf")
      scared = newScaredTimes[0] > 0
      for ghost in ghostPositions:
        d = manhattanDistance(ghost, newPos)
        distance = min(d, distance)

      # nearest and farthest food
      distance2 = float("inf")
      distance3 = float("-inf")
      for food in newFoodList:
        d = manhattanDistance(food, newPos)
        distance2 = min(d, distance2)
        distance3 = max(d, distance3)

      # eating food in this step?
      feeding = len(newFoodList) < len(curFoodList)
      count = 10000 if feeding else len(newFoodList)

      # sum them up
      distance = -100000 if distance < 2 else 0
      if scared: distance = 0
      if count == 0: count = -1000
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
  """
  a smart score evaluation function, which consider following:
  - if there is a capsule around, try to eat ti
  - penalize from going farther from nearest food
  - try to go where more actions are possible

  this eval function shall not be used for full depth Minimax

  :param currentGameState:
  :return: a empirical score, based on actual gameScore
  """
  if currentGameState.isLose() or currentGameState.isWin():
    return  scoreEvaluationFunction(currentGameState)

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
      """
      :param evalFn: evaluation function for Minimax steps
      :param depth: number of rounds of play to look into
      :param profile: if to profile nodes expansion
      :return:
      """
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
      # init node expansion counter
      count=[0]
      # get list of legal actions, without STOP
      actions = gameState.getLegalActions(0)
      if len(actions)>1 and Directions.STOP in actions: actions.remove(Directions.STOP)
      # enumerate all possible actions and corresponding Minimax value
      options = [(action,
                  mini_max(1, range(gameState.getNumAgents()), self.depth,
                           gameState.generateSuccessor(0, action),self.evaluationFunction,
                           count))
                 for action in actions]
      # find maximal Minimax value
      act, val = options[0]
      for (a,v) in options: val = max(val, v)

      # collect all choices; more than one actions can yield same Minimax value
      choices = []
      for (a,v) in options:
        if v==val:
          choices.append(a)

      if self.profile: print "total", count[0],"nodes expanded"

      # tie-break randomly
      return choices[randint(1,len(choices)) -1]

def mini_max(agent, agentsList, depth, state, evaluator, nc):
  """
  A Minimax function
  :param agent: Id of the agent
  :param agentsList: list of all agent, only 0 is Max
  :param depth: number of more rounds to look into
  :param state: current game state
  :param evaluator: evaluation function
  :param nc: node expansion value
  :return: Minimax value estimated at depth
  """
  nc[0]=nc[0]+1
  # evaluate at last depth or game already decided
  if depth == 0 or state.isWin() or state.isLose():
    return evaluator(state)

  # agent 0 is the only Max player
  optimizer = max if agent == 0 else min
  # in a round all player should take part; decrease depth value when last agent played
  nextDepth = depth - 1 if agent == agentsList[-1] else depth
  # get next agent
  nextAgent = agentsList[(agent+1) % len(agentsList)]
  # recursively call for all legal actions
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
    count1,count2  = [0],[0]

    # to profile and compare with naive Minimax, also get node expansion count of Minimax
    if self.profile:
      for action in actions:
        mini_max(1, range(gameState.getNumAgents()), self.depth,
                 gameState.generateSuccessor(0, action),self.evaluationFunction,
                 count2)

    # for each legal action, find Minimax value with Alpha-Beta pruning
    for action in actions:
      v = alpha_beta(1, range(gameState.getNumAgents()), alpha, beta,
                       self.depth, gameState.generateSuccessor(0, action),
                       self.evaluationFunction, count1)
      options.append((action,v))
      alpha = max(alpha, v)

    # collect all choices; more than one actions can yield same Minimax value
    choices = []
    for (a,v) in options:
      if v==alpha:
        choices.append(a)

    if self.profile: print (count1[0]*100/count2[0]),"%\t",count1[0],"\t",count2[0]
    # tie-break randomly
    return choices[randint(1,len(choices)) -1]


def alpha_beta(agent, agentsList, alpha, beta, depth, state, evaluator, nc):
  """
  A Minimax algorithm with Alpha-Beta pruning
  :param agent: id of the agent
  :param agentsList: if of all agents
  :param alpha: alpha value
  :param beta: beta value
  :param depth: depth to look forward into
  :param state: game state
  :param evaluator: evaluation function
  :param nc: node expansion counter
  :return: Minimax value
  """
  nc[0]=nc[0]+1
  if depth==0 or state.isWin() or state.isLose():
    return evaluator(state)

  # agent 0 is the only Max agent
  optimizer = max if agent == 0 else min
  # in a round all player should take part; decrease depth value when last agent played
  nextDepth = depth - 1 if agent == agentsList[-1] else depth
  # next agent
  nextAgent = agentsList[(agent+1) % len(agentsList)]

  # default value before evaluating
  val = float("-inf") if agent==0 else float("inf")

  # recursively call for each legal actions
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

