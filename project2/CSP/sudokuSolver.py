# SUDOKU SOLVER

import sys
import copy
from time import time
from sudokuUtil import *

# Please implement function solve_puzzle
# input puzzle: 2D list, for example:
# [ [0,9,5,0,3,2,0,6,4]
#   [0,0,0,0,6,0,1,0,0]
#   [6,0,0,0,0,0,0,0,0]
#   [2,0,0,9,0,3,0,0,6]
#   [0,7,6,0,0,0,0,0,3]
#   [3,0,0,0,0,0,0,0,0]
#   [9,0,0,5,0,4,7,0,1]
#   [0,5,0,0,2,1,0,9,0]
#   [0,0,8,0,0,6,3,0,5] ]
# Return a 2D list with all 0s replaced by 1 to 9.
# You can utilize argv to distinguish between algorithms
# (basic backtracking or with MRV and forward checking).
# For example: python sudokuSolver.py backtracking
count = 0
def solve_puzzle(puzzle, argv):
  """
  Solve the sudoku puzzle.
  use --mrv switch to enable Minimum Remaining Value heuristic
  use --cp switch to enable Constraint Propagation

  This function creates a SudokuCSP object and finds a solution by with solve_csp
  """
  mrv,cp = False,False
  for arg in argv:
    if arg == "--mrv":
      mrv = True
    if arg == "--cp":
      cp = True
  csp = SudokuCSP(puzzle, cp)
  global count
  count = 0
  res,csp = solve_csp(csp, mrv)
  print count,"steps taken"
  return csp.grid


def sudoku_check(solution):
  """derived from sudokuChecker.check_solution."""
  # type check
  if not isinstance(solution, list):
    return False
  if len(solution) != 9:
    return False
  for row in solution:
    if not isinstance(row, list):
      return False
    if len(row) != 9:
      return False

  # equality check
  for i in range(9):
    for j in range(9):
      n = solution[i][j]
      if (not isinstance(n, int)) or (n < 1) or (n > 9):
        return False
      if puzzle[i][j] != 0 and puzzle[i][j] != n:
        return False

  # block correctness check
  for x in range(3):
    for y in range(3):
      bit_map = [0] * 9
      for i in range(3):
        for j in range(3):
          n = solution[3*x+i][3*y+j]
          bit_map[n - 1] = 1
      if sum(bit_map) != 9:
        return False

  # row correctness check
  for i in range(9):
    bit_map = [0] * 9
    for j in range(9):
      n = solution[i][j]
      bit_map[n - 1] = 1
    if sum(bit_map) != 9:
      return False

  # column correctness check
  transpose_solution = map(list, zip(*solution))
  for i in range(9):
    bit_map = [0] * 9
    for j in range(9):
      n = transpose_solution[i][j]
      bit_map[n - 1] = 1
    if sum(bit_map) != 9:
      return False

  return True

def blockRange(a):
  """
  given a index a, find the range of indices of the block a is a member of
  :param a: index to find block of
  :return: range of indices in the block
  """
  bs = (a/3)*3
  return range(bs,(bs+3))

class SudokuCSP:
  """
  a class to represent Sudoku as a CSP (compact representation)
  fields are:
    grid: partially filled Sudoku grid
    vars: empty blocks in the Sudoku to fill
    domains: domain of each vars
    cp: if constraint satisfaction is to apply
  """

  def __init__(self, grid, cp):
    """
    construct a SudokuCSP object from given puzzle grid
    :param grid: grid of puzzle
    :param cp: is constraint propagation is to apply
    :return: self
    """
    self.vars = []
    self.domains = {}
    self.grid = grid
    self.cp = cp
    for i in range(9):
      for j in range(9):
        if grid[i][j] == 0:
          position = (i,j)
          domain = range(1, 10)
          self.vars.append(position)
          self.domains[position] = domain

  
  def assign(self, var, value):
    """
    attempts to assign a value to this variable
    :param var: unit in Sudoku to fill
    :param value: number attempting to assign
    :return: return true if can do
    """
    x,y = var

    # check row and column constraint
    for i in range(0,9):
      # propagate constraint and remove this value from connected vars' domains
      if self.cp:
        if (x,i) in self.domains and i != y and value in self.domains[(x,i)]:
          self.domains[(x,i)].remove(value)
        if (i,y) in self.domains and i != x and value in self.domains[(i,y)]:
          self.domains[(i,y)].remove(value)
      # if this value already is in same row or column, fail
      if value == self.grid[x][i] or value == self.grid[i][y]:
        return False

    # check block constraint
    for i in blockRange(x):
      for j in blockRange(y):
        # propagate constraint and remove this value from connected vars' domains
        if self.cp and (i,j) in self.domains and (i,j) != var and value in self.domains[(i,j)]:
          self.domains[(i,j)].remove(value)
      # if this value already is in same block, fail
        if value == self.grid[i][j]:
          return False

    # forward check
    if self.cp:
      for loc in self.vars:
        if loc in self.domains:
          l = len(self.domains[loc])
          if l<1:
            return False

    # all set. can assign
    self.grid[x][y] = value
    return True

  def min_rem_val(self):
    """
    find the variable with minimum remaining value in domain
    :return: mrv
    """
    var, min = None, 10
    for v in self.vars:
      l= len(self.domains[v])
      if l < min and l>0:
        var, min = v,l

    self.vars.remove(var)
    return var

  def isComplete(self):
    """
    check if the grid is completely assigned maintaining all constraints
    :return: True if solution, False otherwise
    """
    return sudoku_check(self.grid)

def solve_csp(csp, mrv):
  """
  general backtracking algorithm, with option to add mrv
  constraint propagation shall be handled by the CSP object
  :param csp: SudokuCSP object
  :param mrv: if to employ mrv
  :return: return True and solved csp or False and failed csp
  """
  # keep track of nodes expanded
  global count

  #if all variables assigned, check if solution
  if len(csp.vars) == 0:
    return csp.isComplete(),csp

  # pick next variable
  var = csp.min_rem_val() if mrv else csp.vars.pop()
  # get domain of the var
  domain = csp.domains[var]
  # a copy of CSP to reseed when backtrack
  cspBak = copy.deepcopy(csp)

  # try each value in domain for the var
  for val in domain:
    csp = copy.deepcopy(cspBak)
    count+=1
    if csp.assign(var,val):
      res,csp = solve_csp(csp,mrv)
      if res :
        return res, csp

  return False, csp





#===================================================#
puzzle = load_sudoku('puzzle.txt')

print "solving ..."
t0 = time()
solution = solve_puzzle(puzzle, sys.argv)
t1 = time()
print "completed. time usage: %f" %(t1 - t0), "secs."

save_sudoku('solution.txt', solution)

