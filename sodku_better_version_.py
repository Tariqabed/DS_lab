
import numpy as np 
import sympy as sp 
import random
from tkinter import * 
import time 
import datetime




class SolveAC:
    def __init__(self):
        self.related_cells = {}
        self.dim = 0
        self.grid_dim = 0
        self.domains = {}
        self.length_values = {}

    def grid_insert(self, sudoku, dim):
        self.initialize_grid(sudoku, dim)
        self.assign_values()
        self.calculate_relations()
        self.ac3()  # Apply AC-3 algorithm

    def initialize_grid(self, sudoku, dim):
        self.dim = dim
        self.grid_dim = int(np.sqrt(dim))
        self.sudoku = np.array(sudoku)

    def assign_values(self):
        self.domains = {(r, c): set(range(1, self.dim + 1)) for r in range(self.dim) for c in range(self.dim)}

        for r in range(self.dim):
            for c in range(self.dim):
                if self.sudoku[r, c] != 0:
                    value = self.sudoku[r, c]
                    self.domains[(r, c)] = {value}
    def calculate_relations(self):
        for r in range(self.dim):
            for c in range(self.dim):
                coords = (r, c)
                self.related_cells[coords] = self.get_related_cells(coords)

    def get_related_cells(self, coords):
        related = set()

        # Add cells in the same row and column
        for i in range(self.dim):
            related.add((i, coords[1]))  # Same row
            related.add((coords[0], i))  # Same column

        # Add cells in the same subgrid
        row_index = (coords[0] // self.grid_dim) * self.grid_dim
        col_index = (coords[1] // self.grid_dim) * self.grid_dim
        for row_iter in range(self.grid_dim):
            for col_iter in range(self.grid_dim):
                related.add((row_iter + row_index, col_iter + col_index))

        related.remove(coords)  # Remove the original cell
        return related
    def remove(self, key , value):
        self.domains[key].remove(value)
        if len(self.domains[key]) > 1 :
            self.length_values[key] = len(self.domains[key])
            return 
        if key in self.length_values:
            del self.length_values[key]
        

    def is_valid(self, row, col, value):
        relation = self.related_cells[(row, col)]
        for index in relation:
            r, c = index[0], index[1]
            if len(self.domains[(r, c)]) == 1:
                if list(self.domains[(r, c)])[0] == value:
                    return False
        return True

    def enter_element(self, row, col, value):
        if self.is_valid(row, col, value):
            self.domains[(row, col)] = {value}
            if (row, col) in self.length_values:
                del self.length_values[(row, col)]
            return self.reduction_related_cells((row, col), value)
        return False

    def reduction_related_cells(self, key, value):
        relation = self.related_cells[key]
        for index in relation:
            if value in self.domains[index]:
                self.remove(index, value)
                if len(self.domains[index]) == 1:
                    single_value = next(iter(self.domains[index]))
                    if self.is_valid(index[0],index[1] , single_value):
                        return self.reduction_related_cells(index, single_value)  # Recursively reduce related cells
        return True
    def ac3(self):
        queue = [(xi, xj) for xi in self.domains for xj in self.related_cells[xi]]
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise_arc(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.related_cells[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise_arc(self, xi, xj):
        revised = False
        elements = set(self.domains[xi])
        for x in elements:
            if not any(x != y for y in self.domains[xj]):
                self.remove(xi, x)
                revised = True
        return revised

    def unfinished_cells(self):
        if len(self.length_values) == 0:
            return None
        key = min(self.length_values, key=self.length_values.get)  # Find key with minimum value

        value = self.domains[key]  # Get corresponding value from domains
        return key, value



    def remove_element(self, row, col, value):
        if (row, col) in self.domains and value in self.domains[(row, col)]:
            self.remove((row, col) ,value)

    def backtrack(self):
        cell = self.unfinished_cells()
        if cell is None:
            return True

        (row, col), possible_values = cell[0], cell[1]
        domains_backup = {k: v.copy() for k, v in self.domains.items()}
        length_values_backup = {k: v for k, v in self.length_values.items()}
        for value in possible_values:
            if self.enter_element(row, col, value):
                if self.backtrack():
                    return True
            self.domains = {k: v.copy() for k, v in domains_backup.items()}
            self.length_values = {k: v for k, v in length_values_backup.items()}
            self.remove_element(row, col, value)

        return False
        
    def print_sudoku(self):
        max_row = max(row for row, col in self.domains)
        max_col = max(col for row, col in self.domains)
    
        for row in range(max_row + 1):
            if row % self.grid_dim == 0 and row != 0:
                print("-" * (max_col * 2 + self.grid_dim + 1))  # Print horizontal divider
    
            row_values = []
            for col in range(max_col + 1):
                if col % self.grid_dim == 0 and col != 0:
                    row_values.append("|")  # Print vertical divider
    
                cell_values = self.domains.get((row, col), set())
                if len(cell_values) == 1:
                    cell_value = next(iter(cell_values))  # Get the single value in the set
                    row_values.append(f" {cell_value} ")
                else:
                    row_values.append(" . ")  # Placeholder for empty cell or multiple possibilities
    
            print("".join(row_values))





import random
import math

def generate_sudoku(dim):
    # Check if dimension is valid (must be a perfect square)
    root = int(math.sqrt(dim))
    if root * root != dim:
        raise ValueError("Dimension must be a perfect square (e.g., 9 for 9x9 or 16 for 16x16).")
    
    # Initialize empty grid
    grid = [[0 for _ in range(dim)] for _ in range(dim)]
    
    # Generate random numbers for the first row to start with
    first_row = random.sample(range(1, dim + 1), dim)
    
    # Fill the first row
    for col in range(dim):
        grid[0][col] = first_row[col]
    
    # Generate complete grid using backtracking
    solve_sudoku(grid, dim)
    
    # Remove numbers to create the puzzle
    remove_count = int(dim * math.sqrt(dim))  # Adjust this number for difficulty
    
    while remove_count > 0:
        row = random.randint(0, dim - 1)
        col = random.randint(0, dim - 1)
        
        if grid[row][col] != 0:
            grid[row][col] = 0
            remove_count -= 1
    
    return grid

def solve_sudoku(grid, dim):
    empty_spot = find_empty_spot(grid, dim)
    
    if not empty_spot:
        return True  # Puzzle solved
    
    row, col = empty_spot
    
    for num in range(1, dim + 1):
        if is_valid(grid, row, col, num, dim):
            grid[row][col] = num
            
            if solve_sudoku(grid, dim):
                return True
            
            grid[row][col] = 0  # Backtrack
            
    return False

def find_empty_spot(grid, dim):
    for i in range(dim):
        for j in range(dim):
            if grid[i][j] == 0:
                return (i, j)
    return None

def is_valid(grid, row, col, num, dim):
    # Check if num is not already in the row
    if num in grid[row]:
        return False
    
    # Check if num is not already in the column
    for i in range(dim):
        if grid[i][col] == num:
            return False
    
    # Check if num is not already in the box
    box_size = int(math.sqrt(dim))
    start_row, start_col = box_size * (row // box_size), box_size * (col // box_size)
    for i in range(start_row, start_row + box_size):
        for j in range(start_col, start_col + box_size):
            if grid[i][j] == num:
                return False
    
    return True

# Example usage
if __name__ == "__main__":
    sudoku_grid_16x16 = generate_sudoku(16)
    solver = SolveAC()
    solver.grid_insert(sudoku_grid_16x16,16)
    solver.backtrack()
    solver.print_sudoku()
    
