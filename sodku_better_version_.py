import numpy as np
import heapq

class SolveAC:
    def grid_insert(self, sudoku, dim):
        self.dim = dim
        self.sudoku = np.array(sudoku)
        self.variables = [(r, c) for r in range(self.dim) for c in range(self.dim)]
        self.domains = {v: set(range(1,self.dim)) for v in self.variables}
        self.assigned = {}
        self.sudoku_reduction()
        
        for i in range(self.dim):
            for j in range(self.dim):
                if self.sudoku[i, j] != 0:
                    self.domains[(i, j)] = {self.sudoku[i, j]}
                    self.assigned[(i, j)] = self.sudoku[i, j]

        self.sudoku_reduction()

        # Solve the puzzle using backtracking algorithm
        self.priority_queue()
        self.backtrack_algorithm()

    def is_valid(self, row, col, value):
        # Check if the value is valid in the row and column
        for i in range(self.dim):
            if (i, col) in self.assigned and self.assigned[(i, col)] == value:
                return False
            if (row, i) in self.assigned and self.assigned[(row, i)] == value:
                return False
        
        # Check if the value is valid in the 3x3 subgrid
        box_start_row, box_start_col = row - row % int(np.sqrt(self.dim)), col - col % int(np.sqrt(self.dim))
        return not self.used_in_matrix(box_start_row, box_start_col, value)

    def used_in_matrix(self, start_row, start_col, num):
        for i in range(int(np.sqrt(self.dim))):
            for j in range(int(np.sqrt(self.dim))):
                if self.sudoku[start_row + i, start_col + j] == num:
                    return True
        return False

    def sudoku_reduction(self):
        for (row, col), value in self.assigned.items():
            # Reduce the domain for the row
            for j in range(self.dim):
                if j != col and value in self.domains[(row, j)]:
                    self.domains[(row, j)].remove(value)
        
            # Reduce the domain for the column
            for i in range(self.dim):
                if i != row and value in self.domains[(i, col)]:
                    self.domains[(i, col)].remove(value)
        
            # Reduce the domain for the subgrid
            box_start_row, box_start_col = row - row % int(np.sqrt(self.dim)), col - col % int(np.sqrt(self.dim))
            for i in range(int(np.sqrt(self.dim))):
                for j in range(int(np.sqrt(self.dim))):
                    cell = (box_start_row + i, box_start_col + j)
                    if cell != (row, col) and value in self.domains[cell]:
                        self.domains[cell].remove(value)

    def insert_num(self, row, col, num):
        # Check if the cell is already assigned
        if (row, col) in self.assigned:
            return False
        
        # Check if the number is in the domain of the cell
        if num not in self.domains[(row, col)]:
            return False
        
        # Check if the number is valid in the current context
        if self.is_valid(row, col, num):
            # Remove the number from the domains of related variables
            for i in range(self.dim):

                if num in self.domains[(row, i)]:
                    self.domains[(row, i)].remove(num)
                if num in self.domains[(i, col)]:
                    self.domains[(i, col)].remove(num)
            
            # Remove the number from the domain of the subgrid variables
            box_start_row, box_start_col = row - row % int(np.sqrt(self.dim)), col - col % int(np.sqrt(self.dim))
            for i in range(int(np.sqrt(self.dim))):
                for j in range(int(np.sqrt(self.dim))):
                    if num in self.domains[(box_start_row + i, box_start_col + j)]:
                        self.domains[(box_start_row + i, box_start_col + j)].remove(num)
            
            # Assign the number
            self.sudoku[row, col] = num
            self.assigned[(row, col)] = num
            self.domains[(row, col)] = {num}
            return True
        return False

    def priority_queue(self):
        self.priority = []
        for key, value in self.domains.items():
            if len(value) != 1:
                heapq.heappush(self.priority, (len(value), key, value))
        
    def backtrack_algorithm(self):
        if len(self.priority) == 0 :
            self.priority_queue()
        try:
            # Get the next element with the fewest possibilities
            
            current_element = heapq.heappop(self.priority)
            row, col = current_element[1]

            # Try each possible value for the current element
            for value in current_element[2]:
                # Attempt to insert the value
                if self.insert_num(row, col, value):
                    # If successful, move to the next element
                    if self.backtrack_algorithm():
                        return True
                    # If the current branch leads to a dead end, backtrack
                    self.remove_num(row, col)

            # If no valid number can be inserted, backtrack
            return False
        except:
            return False

            return False

sudoku_puzzle = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]
 
# Create the solver instance and initialize the grid
test = SolveAC()
test.grid_insert(sudoku_puzzle, 9)
test.backtrack_algorithm()
print(test.domains)

