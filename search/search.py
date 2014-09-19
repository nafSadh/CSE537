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
  a boolean switch, wPrio denoting if the fringe structure is affected by
  priority values
  """
  def __init__(self, fringeType, wPrio=False):
    self.fringe = fringeType()
    self.wPrio = wPrio

  def add(self, item, priority=0):
    if(self.wPrio): self.fringe.push(item, prio)
    else: self.fringe.push(item)

  def pop(self):
    return self.fringe.pop()

  def isEmpty(self):
    return self.fringe.isEmpty()

class Record:
  def __init__(self, id, state, parentId, action, val=0):
    self.id = id
    self.state = state
    self.parentId = parentId
    self.action = action
    self.val = val

  def prints(self):
    print self.id,":",self.state," | ",self.parentId," | ",self.action

def genericBlindSearch(problem, fringeType, wPrio=False, preserveOrder=False):

  p = problem #shorthand name
  fringe = Fringe(fringeType, wPrio)
  state = p.getStartState()
  #seeded with start state
  fringe.add(state,0)
  visited = [] #marker to do graph search
  parent = {state:()} #keep track of how each node is reached
  #search using the fringe
  while not fringe.isEmpty():
    state = fringe.pop()
    if p.isGoalState(state): break
    if state not in visited :
      visited.append(state)
      successors = p.getSuccessors(state)
      if preserveOrder : successors.reverse()
      for s in successors :
        if s[0] not in parent:
          fringe.add(s[0],s[2])
          parent[s[0]] = (state, s[1])
  #search complete, enum the path from parents list
  path = []
  while state != p.getStartState() :
    path.insert(0,parent[state][1])
    state = parent[state][0]
  return path

class Search:
  Graph = False
  Tree = True
  
  @staticmethod
  def generic(problem, isTree, fringeType, hasPrio=False, preserveOrder=False):
    """
    implements generic iterative search. Behavior can be tuned with parameters:
  
    isTree is boolean switch to turn on tree search, otherwise a graph search will
      execute. Graph search maintains a visited list

    fringeType: e.g. util.Stack, Queue, PriorityQueue
      fringeType shall expose push(), pop() and isEmpty() functions
      push may take one argument if hasPrio false, otherwise two, second being 
      the priority
  
    """
    p = problem #shorthand
    idx=1
    state = p.getStartState()
    fringe = Fringe(fringeType, hasPrio)
    fringe.add((idx,state),0)
    visited = []
    records = {idx:Record(idx, state, 0, None,0)}
    #search
    while not fringe.isEmpty():
      isp = fringe.pop()
      state = isp[1]
      id = isp[0]
      if p.isGoalState(state) : 
        idx = id
        break
      if isTree or state not in visited :
        if not isTree: visited.append(state)
        successors = p.getSuccessors(state)
        if preserveOrder: successors.reverse()
        for s in successors:
          idx+=1
          fringe.add((idx,s[0]),s[2])
          records[idx] = Record(idx,s[0],id,s[1],s[2])
    #search done, enum path
    path = []
    while idx != 1 :
      path.insert(0,records[idx].action)
      idx = records[idx].parentId
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
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  return Search.generic(problem, Search.Graph, util.Stack)

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  return Search.generic(problem, Search.Graph, util.Queue)

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  fringe = util.PriorityQueue()
  wPrio = True
  p = problem #shorthand name
  state = p.getStartState()
  #seeded with start state
  if wPrio: fringe.push(state,0)
  else: fringe.push(state)
  visited = [] #marker to do graph search
  parent = {state:()} #keep track of how each node is reached
  #search using the fringe
  while not fringe.isEmpty():
    state = fringe.pop()
    if p.isGoalState(state): break
    if state not in visited :
      visited.append(state)
      successors = p.getSuccessors(state)
      for s in successors :
        if s[0] not in parent:
          if wPrio: fringe.push(s[0],s[2])
          else : fringe.push(s[0])
          parent[s[0]] = (state, s[1])
  #search complete, enum the path from parents list
  path = []
  while state != p.getStartState() :
    path.insert(0,parent[state][1])
    state = parent[state][0]
  return path

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
