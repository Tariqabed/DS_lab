import numpy as np
import threading

class SolveAC:
    def __init__(self):
        self.related_cells = {}
        self.dim = 0
        self.grid_dim = 0
        self.domains = {}

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
            return self.ac3()
        return False

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
        for x in set(self.domains[xi]):
            if not any(x != y for y in self.domains[xj]):
                self.domains[xi].remove(x)
                revised = True
        return revised

    def unfinished_cells(self):
        index = self.binary_search_first_greater(list(self.domains.values()), 1)
        if index != -1 : return list(self.domains.items())[index]
        return None
    @staticmethod
    def binary_search_first_greater(arr, target):
        left, right = 0, len(arr) - 1
        result = -1  # Default value if no element is greater than target

        while left <= right:
            mid = left + (right - left) // 2
            
            if len(arr[mid]) > target:
                result = mid  # Update result to the current index
                right = mid - 1  # Search the left half
            else:
                left = mid + 1  # Search the right half

        return result

    def remove_element(self, row, col, value):
        if (row, col) in self.domains and value in self.domains[(row, col)]:
            self.domains[(row, col)].remove(value)

    def backtrack(self):
        if self.unfinished_cells() is None:
            return True

        cell = self.unfinished_cells()

        (row, col), possible_values = cell[0], cell[1]

        domains_backup = {k: v.copy() for k, v in self.domains.items()}

        for value in possible_values:
            if self.enter_element(row, col, value):
                if self.backtrack():
                    return True

            self.domains = {k: v.copy() for k, v in domains_backup.items()}
            self.remove_element(row, col, value)

        return False



# Example Sudoku grid
sudoku = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

solver = SolveAC()
solver.grid_insert(sudoku, 9)


solver.backtrack()
print(solver.domains)
