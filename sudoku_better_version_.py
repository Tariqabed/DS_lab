import numpy as np
import sympy as sp
import random
from tkinter import *
import time
import datetime
from tkinter import *
import math
import os
import multiprocessing
from multiprocessing import Pool
import copy
import time
from CTkMenuBar import *
import re
import customtkinter
from tkinter import filedialog
import threading



class SolveAC:
    def __init__(self):
        self.related_cells = {}
        self.dim = 0
        self.grid_dim = 0
        self.domains = {}
        self.length_values = {}
    def grid_insert(self, sudoku,dim):
        self.initialize_grid(sudoku, dim)
        self.assign_values()
        self.calculate_relations()
        self.sudoku_reduction()

    def initialize_grid(self, sudoku, dim):
        self.dim = dim
        self.grid_dim = int(np.sqrt(int(dim)))
        self.sudoku = np.array(sudoku)

    def assign_values(self):
        self.domains = {(r, c): set(range(1, self.dim + 1)) for r in range(self.dim) for c in range(self.dim)}
        for r in range(self.dim):
            for c in range(self.dim):
                if self.sudoku[r, c] != 0:
                    value = self.sudoku[r, c]
                    self.domains[(r, c)] = {value}

    def is_valid_sudoku(self, board):
        def is_valid_group(group):
            """Helper function to check if a group (row, column, or sub-grid) is valid."""
            group = [num for num in group if num != 0]  # Remove empty cells
            return len(group) == len(set(group))  # Check for duplicates

        # Check rows
        for row in board:
            if not is_valid_group(row):
                return False

        # Check columns
        for col in zip(*board):
            if not is_valid_group(col):
                return False

        # Check sub-grids
        for i in range(0, self.dim, self.grid_dim):
            for j in range(0, self.dim, self.grid_dim):
                block = [board[x][y] for x in range(i, i + self.grid_dim) for y in range(j, j + self.grid_dim)]
                if not is_valid_group(block):
                    return False

        return True


    def calculate_relations(self):
        for r in range(self.dim):
            for c in range(self.dim):
                coords = (r, c)
                self.related_cells[coords] = self.get_related_cells(coords)

    def get_related_cells(self, coords):
        related = set()
        for i in range(self.dim):
            related.add((i, coords[1]))
            related.add((coords[0], i))
        subgrid_row_start = (coords[0] // self.grid_dim) * self.grid_dim
        subgrid_col_start = (coords[1] // self.grid_dim) * self.grid_dim
        for row_iter in range(subgrid_row_start, subgrid_row_start + self.grid_dim):
            for col_iter in range(subgrid_col_start, subgrid_col_start + self.grid_dim):
                related.add((row_iter, col_iter))
        related.remove(coords)
        return related

    def remove(self, domains, length_values, key, value):
        domains[key].remove(value)
        if len(domains[key]) > 1:
            length_values[key] = len(domains[key])
            return
        if key in length_values:
            del length_values[key]

    def is_valid(self, domains, row, col, value):
        relation = self.related_cells[(row, col)]

        for index in relation:
            r, c = index[0], index[1]
            if len(domains[(r, c)]) == 1:
                if list(domains[(r, c)])[0] == value:
                    return False
        return True



    def enter_element(self, domains, length_values, row, col, value):
        if self.is_valid(domains, row, col, value):
            domains[(row, col)] = {value}
            if (row, col) in length_values:
                del length_values[(row, col)]

            return self.reduction_related_cells(domains, length_values, (row, col), value, self.related_cells[(row, col)])
        return False



    def enter_element_machine(self, domains, length_values, row, col, value):
        if value in domains[(row , col)]:
            domains[(row, col)] = {value}
            if (row, col) in length_values:
                del length_values[(row, col)]

            return self.reduction_related_cells(domains, length_values, (row, col), value, self.related_cells[(row, col)])
        return False

    def reduction_related_cells(self, domains, length_values, key, value, relation):
        for index in relation:
            if value in domains[index]:
                self.remove(domains, length_values, index, value)
                if len(domains[index]) == 1:
                    single_value = next(iter(domains[index]))
                    if self.is_valid(domains, index[0], index[1], single_value):
                        if not self.reduction_related_cells(domains, length_values, index, single_value, self.related_cells[index]):
                            return False
                    else:
                        return False
        return True

    def sudoku_reduction(self):
        for row in range(self.dim):
            for col in range(self.dim):
                if len(self.domains[(row, col)]) == 1:
                    value = next(iter(self.domains[(row, col)]))
                    for index in self.related_cells[(row, col)]:
                        if value in self.domains[index] and len(self.domains[index]) > 1:
                            self.remove(self.domains, self.length_values, index, value)

    def unfinished_cells(self, domains, length_values):
        if len(length_values) == 0:
            return None
        key = min(length_values, key=length_values.get)
        value = domains[key]
        return key, value

    def remove_element(self, domains, length_values, row, col, value):
        if (row, col) in domains and value in domains[(row, col)]:
            self.remove(domains, length_values, (row, col), value)

    def Solver(self):

        if self.is_valid_sudoku(self.create_sudoku_matrix(self.domains)):
            self.solved_sudoku = list()
            return self.parallel_backtrack(self.domains, self.length_values)
        return False


    def parallel_backtrack(self, domains, length_values):
        cell = self.unfinished_cells(domains, length_values)
        if cell is None:
            return domains
        (row, col) , possible_values = cell[0] , cell[1]
        results = list()

        num_cores = multiprocessing.cpu_count()
        with multiprocessing.Pool(num_cores) as exe:
            for value in possible_values:
                result = exe.apply_async(self.enter_in_parllel , args = (row , col , value , domains , length_values))
                results.append(result)


            while results and len(self.solved_sudoku) < 1: # Allowing only N number of sloutions

                for result in results:

                    if result.ready():  # Check if the task is complete

                        output = result.get()  # Get the result




                        results.remove(result)  # Remove the processed result from the list


                        self.solved_sudoku.append(output)

                        return True  # Exit the loop to check the next set of results
            return False



    def enter_in_parllel(self, row, col, value, domains, length_values):
        if self.enter_element_machine(domains, length_values, row, col, value):
            return self.try_value(domains, length_values)






    def try_value(self, domains, length_values):
        cell = self.unfinished_cells(domains, length_values)

        if cell is None:
            return domains


        (row, col), possible_values = cell[0], cell[1]
        # Backup the current state of domains and length_values

        domains_backup = {k: v.copy() for k, v in domains.items()}
        length_values_backup = {k: v for k, v in length_values.items()}
        for value in possible_values:
            if self.enter_element_machine(domains, length_values, row, col, value):
                result = self.try_value(domains, length_values)

                if result:
                    return result

            # Restore the state before trying a new value
            domains = {k: v.copy() for k, v in domains_backup.items()}
            length_values = {k: v for k, v in length_values_backup.items()}
            self.remove_element(domains, length_values, row, col, value)
        return False




    def create_sudoku_matrix(self, domains):
        max_row = max(row for row, col in domains)
        max_col = max(col for row, col in domains)
        sudoku_matrix = np.zeros((max_row + 1, max_col + 1), dtype=int)
        for row in range(max_row + 1):
            for col in range(max_col + 1):
                cell_values = domains.get((row, col), set())
                if len(cell_values) == 1:
                    cell_value = next(iter(cell_values))
                    sudoku_matrix[row, col] = cell_value
                else:
                    sudoku_matrix[row, col] = 0



        return sudoku_matrix
    def create_sudoku(self):
        # Initialize the matrix with zeros
        self.matrix = np.zeros((self.dim, self.dim)).astype(int)

        # Generate a random sequence for the first row
        numbers = np.arange(1, self.dim + 1)
        first_row = np.random.choice(numbers, size=len(numbers), replace=False)

        # Generate a random sequence for the first column, shifted by one
        first_col_shifted = np.random.choice(numbers - 1, size=len(numbers), replace=False)

        # Place the first row values into the matrix using the shifted indices
        self.matrix[(first_row - 1).astype(int), first_col_shifted] = first_row
        # Solve the Sudoku to fill the matrix

        self.grid_insert(self.matrix,self.dim)

        self.Solver()

        self.matrix = np.array(self.create_sudoku_matrix(self.solved_sudoku.pop(0)))

        # Determine the number of elements to remove based on the difficulty level
        difficulty_level = int(self.difficulty)
        num_elements_to_remove = int(self.matrix.size * difficulty_level / 100)
        
        # Select random indices to remove elements from the matrix
        random_indices = np.random.choice(self.matrix.size, size=num_elements_to_remove, replace=False)
        
        row_indices, col_indices = np.unravel_index(random_indices, self.matrix.shape)
        
        # Remove elements to create the puzzle
        self.matrix[row_indices, col_indices] = 0
        return self.matrix



if __name__ == "__main__":
    solver = SolveAC()
    solver.difficulty = 50
    solver.dim = 9
    sudoku_puzzle = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    solver.grid_insert(sudoku_puzzle , solver.dim)
    print(solver.Solver())

