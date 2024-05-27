import numpy as np 
import sympy as sp 
import random
from tkinter import * 
import time 
import datetime


class Sudoku_structure:  
    def unique_elements( self ,array ):
        array = array[array != 0]

        elements , index , count = np.unique( array , return_index = True  , return_counts = True)
        if np.any(count>1):
            return  False ,elements , count 

        return True ,elements
    
    def used_in_matrix(self, start_row, start_col, num=-1):
        elements = list()
        for i in range(int(np.sqrt(self.dim))):
            for j in range(int(np.sqrt(self.dim))):
                
                if self.matrix[i + start_row][j + start_col] == num:
                    elements.append(self.matrix[i + start_row][j + start_col])
                    return True , elements
        return False, elements
    
    def enter_element(self, row, col, num , Sodku_creator = False):           
        if np.any(self.matrix[row] == num):
            return False 
        if np.any(self.matrix[:,col] == num):
            return False
        if not self.used_in_matrix(row - row % int(np.sqrt(self.dim)), col - col % int(np.sqrt(self.dim)), num)[0]:
            return True
        return False



    def Sodku_creator(self,diffculty_level):
        self.matrix = np.zeros((self.dim , self.dim)).astype(int)
        numbers1_self_dim = np.arange(1, self.dim + 1)
        array1= np.random.choice(numbers1_self_dim, size=len(numbers1_self_dim), replace=False)
        array2 = np.random.choice(numbers1_self_dim-1, size=len(numbers1_self_dim), replace=False)
        self.matrix[(array1 - np.ones(self.dim)).astype(int),array2] = array1
        self.solveSudoku()


        diffculty_level=int(diffculty_level)
        num_elements = int(self.matrix.size * diffculty_level / 100)

        random_indices = np.random.choice(self.matrix.size, size=num_elements, replace=False)
        row_indices, col_indices = np.unravel_index(random_indices, self.matrix.shape)
    
        self.matrix[row_indices, col_indices] = 0
    def elements_set(self, row, col):
        """Determines the possible elements that can be placed in a cell at (row, col)."""
        all_elements = set(range(1, self.dim + 1))

        # Get unique elements in the row
        row_elements = set(self.unique_elements(self.matrix[row])[1])

        # Get unique elements in the column
        col_elements = set(self.unique_elements(self.matrix[:, col])[1])

        # Get unique elements in the subgrid
        sqrt_dim = int(np.sqrt(self.dim))
        subgrid_start_row = row - row % sqrt_dim
        subgrid_start_col = col - col % sqrt_dim
        subgrid_elements = set(self.used_in_matrix(subgrid_start_row, subgrid_start_col)[1])

        # Determine possible elements for the cell by excluding used elements
        used_elements = row_elements.union(col_elements).union(subgrid_elements)
        possible_elements = list(all_elements.difference(used_elements))

        return possible_elements
        
    
    def allowed_in_cell(self):
        self.allowed_numbers = np.zeros((self.dim , self.dim)).astype(list)
        
        for i in range(self.dim):
            for j in range(self.dim):
                self.allowed_numbers[i,j] = self.elements_set(i, j)
                
        return self.allowed_numbers
                
    def solveSudoku(self, row=0, col=0,creator=True):
        if row == self.dim - 1 and col == self.dim: return True 
            
        if col == self.dim: row, col = row + 1, 0
        
        if self.matrix[row][col] != 0:
            
            return self.solveSudoku(row, col + 1,creator)
                ## A trick to make the matrix more reasonable in terms of time complexity##
        possible_elements = self.elements_set(row , col)

        for num in possible_elements:
            
            if self.enter_element(row, col, num):
                if creator is False :
                    self.entries_index[row , col].insert(0,str(num))
                self.matrix[row][col] = num

                if self.solveSudoku(row, col + 1,creator):
                    return True
                
            if creator is False : self.entries_index[row , col].delete(0,END)
            self.matrix[row][col] = 0
                
        return False
