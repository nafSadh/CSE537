# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import sys


class Ascertain:
  def __init__(self, expression):
    self.expression = expression
  
  def otherwise(self, message, abort=True):
    if not self.expression:
      print "ASSERTION:", message, "!"
      if abort: sys.exit(1)
  

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).

  You do not need to change anything in this class, ever.
  """

  def getStartState(self):
     """
     Returns the start state for the search problem
     """
     util.raiseNotDefined()

  def isGoalState(self, state):
     """
       state: Search state

     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state

     For a given state, this should return a list of triples,
     (successor, action, stepCost), where 'successor' is a
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take

     This method returns the total cost of a particular sequence of actions.  
     The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


class Fringe:
  """
  Fringe class wraps the fringe containers. The constructor takes a container
  class type (e.g. util.Stack, util.Queue, util.PriorityQueue) as argument, and
  a boolean switch, withPriority denoting if the fringe structure is affected by
  priority values
  """
  HAS_PRIORITY = True
  NO_PRIORITY = False

  def __init__(self, fringeType, withPriority=NO_PRIORITY):
    self.fringe = fringeType()
    self.withPriority = withPriority

  def add(self, item, priority=0):
    if self.withPriority: self.fringe.push(item, priority)
    else: self.fringe.push(item)

  def pop(self):
    return self.fringe.pop()

  def isEmpty(self):
    return self.fringe.isEmpty()


class Search:
  """
  This class implements search logic 
  """
  GRAPH = True
  TREE = False
  GREEDY = True
  OPTIMAL = False
  
  class Record:
    def __init__(self, idx, state, parentId, action, 
                 stepCost=1, g=1, h=0, val=0):
      self.idx = idx
      self.state = state
      self.parentId = parentId
      self.action = action
      self.val = val
      self.stepCost = stepCost
      self.g = g
      self.h = h


  @staticmethod
  def isAcyclicSuccessor(records, idx, state):
    assert isinstance(records, {})
    while idx!=1:
      if state==records[idx].state : return False
      idx = records[idx].parentId
    return True


  @staticmethod
  def generic(problem, graphSearch, fringeType, hasPriority=Fringe.NO_PRIORITY,
              heuristic=None, greedySearch = OPTIMAL,
              preserveOrder=False):
    """
    This function implements generic iterative search. Behavior can be tuned
    with parameters:

    graphSearch: boolean switch to turn on graph search, otherwise a tree search
      will be executed. GRAPH search maintains a list of visited nodes.

    fringeType: e.g. util.Stack, util.Queue, util.PriorityQueue
      fringeType class shall expose push(), pop() and isEmpty() functions.
      push may take one argument if hasPriority=false, otherwise two, second 
      being the priority.

    hasPriority: boolean switch saying whether fringe behavior depends on some
      priority function

    heuristic: a Heuristic function to estimate h()

    greedySearch: if true then f(n)=h(n) otherwise f(n)=g(n)+h(n)

    preserveOrder: boolean switch, if on then successors are added to fringe
      preserving the order
    """
    p = problem #shorthand
    i=1; state = p.getStartState() #start state
    fringe = Fringe(fringeType, hasPriority); fringe.add((i,state),0)
    visited = {}
    records = {i:Search.Record(i, state, 0, None, 0,0)}
    #search
    while not fringe.isEmpty():
      idx,state = fringe.pop()
      g = records[idx].g
      if p.isGoalState(state): i = idx; break
      #if state in visited : print "skip state",id,state
      if state not in visited:
        if graphSearch: visited[state]=True;
        successors = p.getSuccessors(state)
        if preserveOrder: successors.reverse()
        for s in successors:
          i+=1; stt,act,cost=s
          if graphSearch or Search.isAcyclicSuccessor(records, idx, stt):
            h = 0 if heuristic is None else heuristic(stt,p)
            f = h if greedySearch else g+cost+h
            fringe.add((i,stt),f)
            records[i] = Search.Record(i,stt,idx,act,cost, g+cost,h)
    #print "fringe:",fringe.isEmpty(), "Goal:",p.isGoalState(state)
    Ascertain(p.isGoalState(state)).otherwise(
      "Search failed: fringe emptied before reaching any goal state.")
    #search done, enum path
    #for r in records: records[r].prints()
    path = []
    while records[i].parentId != 0:
      path.insert(0,records[i].action)
      i = records[i].parentId
    return path



def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].

  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:

  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start successors:", problem.getSuccessors(problem.getStartState())
  """
  return Search.generic(problem, Search.GRAPH, util.Stack)


def breadthFirstSearch(problem):
  """Search the shallowest nodes in the search tree first. [p 81]"""
  return Search.generic(problem, Search.GRAPH, util.Queue)

def uniformCostSearch(problem):
  """Search the node of least total cost first. """
  return Search.generic(problem, Search.GRAPH, 
                        util.PriorityQueue, Fringe.HAS_PRIORITY)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  """Search the node that has the lowest combined cost and heuristic first."""
  return Search.generic(problem, Search.GRAPH, 
                        util.PriorityQueue, Fringe.HAS_PRIORITY,
                        heuristic)


def greedyBestFirstSearch(problem, heuristic=nullHeuristic):
  """Search the node that has the lowest combined cost and heuristic first."""
  return Search.generic(problem, Search.GRAPH, 
                        util.PriorityQueue, Fringe.HAS_PRIORITY,
                        heuristic, Search.GREEDY)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
greedy = greedyBestFirstSearch
