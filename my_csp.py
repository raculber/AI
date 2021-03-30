from sudoku import Sudoku
from copy import deepcopy
import numpy as np

class CSP_Solver(object):
    """
    This class is used to solve the CSP with backtracking using the minimum value remaining heuristic.
    HINT: you will likely want to implement functions in the backtracking sudo code in figure 6.5 in the text book.
            We have provided some prototypes that might be helpful. You are not required to use any functions defined
            here and can modify any function other than the solve method. We will test your code with the solve method
            and so it must have no parameters and return the type it says. 
         
    """
    def __init__(self, puzzle_file):
        '''
        Initialize the solver instance. The lower the number of the puzzle file the easier it is. 
        It is a good idea to start with the easy puzzles and verify that your solution is correct manually. 
        You should run on the hard puzzles to make sure you aren't violating corner cases that come up.
        Harder puzzles will take longer to solve.
        :param puzzle_file: the puzzle file to solve 
        '''
        self.sudoku = Sudoku(puzzle_file) # this line has to be here to initialize the puzzle
        # print ("Sudoku", Sudoku.board_str(self.sudoku))
        # print("board", self.sudoku.board) - List of Lists 
        self.num_guesses = 0
        # self.unassigned = deque()
        self.assignment = {}
        
        # make domian the Given Puzzle
        self.domains = deepcopy(self.sudoku.board)
        # Overwrite 0's with their possiblilities.
        for row in range(0,9):
            for col in range(0,9):
                # extract value
                value = self.sudoku.board[row][col]
                if value == 0:
                    self.domains[row][col] = [1,2,3,4,5,6,7,8,9]
                    # add this index to unassigned for faster look ups
                    # self.unassigned.append((row,col))
                else: 
                    self.domains[row][col] = value
                    self.assignment[(row, col)] = value

        vars=[]
        # self.csp = CSP(vars, self.domains)

    ################################################################
    ### YOU MUST EDIT THIS FUNCTION!!!!!
    ### We will test your code by constructing a csp_solver instance
    ### e.g.,
    ### csp_solver = CSP_Solver('puz-001.txt')
    ### solved_board, num_guesses = csp_solver.solve()
    ### so your `solve' method must return these two items.
    ################################################################
    def solve(self):
        '''
        This method solves the puzzle initialized in self.sudoku 
        You should define backtracking search methods that this function calls
        The return from this function NEEDS to match the correct type
        Return None, number of guesses no solution is found
        :return: tuple (list of list (ie [[]]), number of guesses
        '''
        self.backtracking_search()
        print ("board", self.sudoku.board)
        print("num",self.num_guesses)
        return self.sudoku.board, self.num_guesses
    def backtracking_search(self):
        '''
        This function might be helpful to initialize a recursive backtracking search function
        You do not have to use it.
        
        :param sudoku: Sudoku class instance
        :param csp: CSP class instance
        :return: board state (list of lists), num guesses 
        '''

        return self.recursive_backtracking(self.assignment)

    def isSafe(self, arr, elem):
        row = arr[0]
        col = arr[1]
        cols = []
        for c in range(0,9):
            if not (c==col):
                cols.append(self.sudoku.board[row][c])
        if elem in cols:
            return False
        rows = []
        for r in range(0,9):
            if not(r == row):
                rows.append(self.sudoku.board[r][col])
        if elem in rows:
            return False
        colB = 0
        rowB = 0
        if col in [0,1,2]:
            colB = 0
        if col in [3,4,5]:
            colB = 3
        if col in [6,7,8]:
            colB = 6
        if row in [0,1,2]:
            rowB = 0
        if row in [3,4,5]:
            rowB = 3
        if row in [6,7,8]:
            rowB = 6
        square = []
        for colB2 in range(colB, colB+3):
            for rowB2 in range (rowB, rowB+3):
                if not (rowB2 == row) and not(colB2 == col):
                    square.append(self.sudoku.board[rowB2][colB2])
        if elem in square:
            return False
        self.sudoku.board[row][col] = elem
        return True

    def recursive_backtracking(self, assignment):
        '''
        recursive backtracking search function.
        You do not have to use this
        :param sudoku: Sudoku class instance
        :param csp: CSP class instance
        :return: board state (list of lists)
        '''
        # return a solution or failure
        # if assignment is complete then return the assignment
        if self.sudoku.complete():
            return assignment
        MRV = []
        """Find all 0's and assign a MRV based on number of non zeros""" 
        for row in range(0,9):
            for col in range(0,9):
                value = self.sudoku.board[row][col]
                count = 0
                position = (row,col)
                domain = self.domains[row][col]
                if value == 0 and domain == [1,2,3,4,5,6,7,8,9]:
                    for c in range (0,9):
                        value = self.sudoku.board[row][c]
                        if not (value == 0):
                            count += 1
                    for r in range (0,9):
                        value = self.sudoku.board[r][col]
                        if not (value == 0):
                            count += 1
                    colB = 0
                    rowB = 0
                    if col in [0,1,2]:
                        colB = 0
                    if col in [3,4,5]:
                        colB = 3
                    if col in [6,7,8]:
                        colB = 6
                    if row in [0,1,2]:
                        rowB = 0
                    if row in [3,4,5]:
                        rowB = 3
                    if row in [6,7,8]:
                        rowB = 6
                    for colB2 in range(colB, colB+3):
                        for rowB2 in range (rowB, rowB+3):
                            value = self.sudoku.board[rowB2][colB2]
                            if not (value == 0) and not (rowB2 == row) and not(colB2 == col):
                                count += 1
                    MRV.append((count, (row,col)))
        MRV.sort(reverse=True)
        firstElem = MRV[0]
        count = firstElem[0]
        row,col = firstElem[1]
        for num in self.domains[row][col]:
            assignment[(row,col)] = num 
            arr = [row,col]
            self.num_guesses += 1
            if self.isSafe(arr, num):
                visitedStates = self.recursive_backtracking(assignment)
                if visitedStates is not None:
                    return visitedStates
        self.sudoku.board[row][col] = 0
        assignment.pop((row,col))
        return None

            
        



if __name__ == '__main__':
    csp_solver = CSP_Solver('puz-001.txt')
    solution, guesses = csp_solver.solve()

