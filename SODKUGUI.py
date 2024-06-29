from sudoku_better_version_ import SolveAC  # Replace with your solver import
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

from functools import partial


solver = SolveAC()
class Sudoku_GUI:
    def __init__(self, dim, difficulty):
        solver.domains = {}
        solver.related_cells = {}
        solver.dim = int(dim)
        solver.grid_dim = np.sqrt(int(dim))
        solver.length_values = {}
        solver.solution = list()

        solver.dim = int(dim)
        solver.difficulty = difficulty
        solver.grid_insert(solver.create_sudoku() ,solver.dim)

        self.root = customtkinter.CTk(fg_color = "whitesmoke")

        self.root.title("Sudoku")
        self.root.geometry("860x600")
        self.counter = 0
        self.running = False
        self.time_label = customtkinter.CTkLabel(self.root, text="00:00", font=("arial", 38))
        self.time_label.grid(row=2 , column = 25 )
        self.counter_label = customtkinter.CTkLabel(self.root, text="0", font=("arial", 38))
        self.counter_label.grid(row=4 , column = 25 )
        self.create_entries()

        self.menu_bar()
        self.start_timer()


        self.root.mainloop()

    def create_entries(self):
        self.matrix_entries = {}
        self.entries_index = {}


        subgrid_colors = ['lightskyblue1', 'gray']  # Define colors for the subgrids
        for row in range(solver.dim):
            for col in range(solver.dim):
                subgrid_row_start = (row // solver.grid_dim) * solver.grid_dim
                subgrid_col_start = (col // solver.grid_dim) * solver.grid_dim
                color_index = (subgrid_row_start // solver.grid_dim + subgrid_col_start // solver.grid_dim) % 2

                entry = customtkinter.CTkEntry(
                    self.root,
                    height=50,
                    width=55,
                    font=("Arial", 22),
                    justify='center',
                    border_color=subgrid_colors[color_index],
                    border_width=2,
                    corner_radius=4
                )

                if solver.sudoku[row, col] != 0:
                    entry.insert(0, str(solver.sudoku[row, col]))
                    entry.configure(state='disabled', height=50, width=55, border_width=2, fg_color='lightblue', corner_radius=4)
                else:
                    entry.configure(bg_color='white' , fg_color = 'white')  # Set background color for editable entries

                self.matrix_entries[entry] = (row, col)
                self.entries_index[row, col] = entry


                entry.grid(row=row+4, column=col+4, padx=0, pady=0)  # Adjust padx and pady

                # Use partial to pass the widget to the event handler
                entry.bind("<KeyRelease>", partial(self.on_key_release, widget=entry))


                entry.bind("<FocusIn>", partial(self.on_focus_in, widget=entry))

                entry.bind("<FocusOut>", partial(self.on_focus_out, widget=entry))
        # Create buttons outside the nested loops
        solve_button = customtkinter.CTkButton(self.root, text="Solve", command=self.solve, height=35, width=100, fg_color="green")
        clean_button = customtkinter.CTkButton(self.root, text="Clean", command=self.clean_matrix, height=35, width=100, fg_color='red')
        sudoku_create = customtkinter.CTkButton(self.root, text="New Game", command=self.create_game, height=35, width=100)

        solve_button.grid(row=solver.dim + 30, column=2, columnspan=solver.dim // 2)
        clean_button.grid(row=solver.dim + 30, column=5, columnspan=solver.dim // 2)
        sudoku_create.grid(row=solver.dim + 30, column=8, columnspan=solver.dim // 2)



    def menu_bar(self ):


        # Create a File menu
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        # Adding a file menu
        file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_game)
        file_menu.add_command(label="Save", command=self.save_game)
        file_menu.add_command(label="Exit", command=self.root.destroy)



    def open_game(self):
        self.root.withdraw()

        new_sudoku= open(filedialog.askopenfilename(),'r')


        sudoku = np.zeros((solver.dim ,solver.dim)).astype(int).reshape(solver.dim , solver.dim)

        for grid_values in new_sudoku:

            if 'game dim' in grid_values:
                dim = int(grid_values[len('game dim '):])

            elif 'time' in grid_values:
                self.total_seconds = int(grid_values[len('time'):])

            elif 'step count ' in grid_values:
                self.counter = int(grid_values[len('step count '):])


            else:
                numbers = re.findall(r'\d+', grid_values)

                row , col , values = int(numbers[0]) , int(numbers[1]) , int(numbers[2])

                sudoku[row , col] = values

        solver.grid_insert(sudoku,dim)


        self.create_entries()
        self.root.deiconify()


    def save_game(self):
        self.root.withdraw()

        save_current_game = open(filedialog.asksaveasfilename(),'w')

        save_current_game.write('game dim ' + str(solver.dim)+'\n')
        save_current_game.write('time ' + str(self.total_seconds) +'\n')
        save_current_game.write('step count ' + str(self.counter)+'\n')

        for index in solver.domains:
            if len(solver.domains[index]) == 1 :
                save_current_game.write(f"{index} : {str(solver.domains[index].pop())}\n")


        save_current_game.close()



        self.root.deiconify()




    def solve(self):
        self.game_end()
        solver.grid_insert(solver.create_sudoku_matrix(solver.domains) ,solver.dim)


        exist_solution = solver.Solver()
        if exist_solution:
            num_solutions = len(solver.solved_sudoku)
            self.solution = solver.create_sudoku_matrix(solver.solved_sudoku.pop(0))


            self.solution_count = customtkinter.CTkLabel(self.root, text="Solutions Found: " + str(num_solutions), font=("Arial", 20))
            self.solution_count.grid(row=7 , column = 25 )

        print(exist_solution)
        self.insert_values(0,0,exist_solution)



    def insert_values(self , row , col,exist_solution):
        if row < solver.dim:
            if col < solver.dim:
                if exist_solution:
                    self.entries_index[row,col].delete(0, END)
                    self.entries_index[row,col].insert(0, str(self.solution[row][col]))
                    self.entries_index[row , col].configure(state = 'disabled')
                else :
                    if self.entries_index[row,col].cget('state') != 'disabled':
                        self.entries_index[row,col].configure(fg_color="lightsalmon")

                self.root.after(35, self.insert_values, row, col + 1 , exist_solution)
            else:
                self.root.after(75, self.insert_values, row + 1, 0 , exist_solution)

    def on_focus_in(self, event, widget):
        index = self.matrix_entries[widget]
        row, col = index[0], index[1]
        related_cells = solver.related_cells[(row, col)]
        for cell in related_cells:
            cell_row, cell_col = cell
            entry = self.entries_index[cell_row, cell_col]
            if entry.cget('fg_color') == 'white':
                entry.configure(fg_color='skyblue' ,bg_color ='gray')

    def on_focus_out(self, event, widget):
        index = self.matrix_entries[widget]
        row, col = index[0], index[1]
        related_cells = solver.related_cells[(row, col)]
        for cell in related_cells:
            cell_row, cell_col = cell
            entry = self.entries_index[cell_row, cell_col]
            if entry.cget('fg_color') == 'skyblue':
                entry.configure(fg_color='white' , bg_color = 'white')

    def on_key_release(self, event,widget):
        entry = widget
        entry_value = event.widget.get()

        index = self.matrix_entries[widget]
        if len(entry_value) == 0:
            self.remove_element(index)
            entry.configure(fg_color = 'white')
            return
        # Validate entry
        if not self.is_valid_entry(entry_value):
            self.handle_invalid_entry(entry, index)
            return

        # Check for repeated entry
        repeated = self.is_repeated_entry(index, entry_value)

        # Update solver and UI
        if self.update_solver(index, entry_value):
            entry.configure(fg_color = "palegreen")
        else:
            self.handle_solver_failure(entry, index, entry_value)

        # Update counter if entry is not repeated
        if not repeated:
            self.increment_counter()


    def is_valid_entry(self, entry_value):
        return entry_value.isdigit() and 1 <= int(entry_value) <= solver.dim

    def handle_invalid_entry(self, entry, index):
        entry.configure(fg_color="tomato")
        # Schedule the reset of the background color and deletion of the entry's content after 400 milliseconds
        entry.after(500, lambda: self.reset_entry(entry))

    def reset_entry(self, entry):
        entry.configure(fg_color="white")
        entry.delete(0, 'end')



    def is_repeated_entry(self, index, entry_value):
        return len(solver.domains[index]) == 1 and solver.domains[index] == {int(entry_value)}

    def update_solver(self, index, entry_value):

        return solver.enter_element(solver.domains, solver.length_values, index[0], index[1], int(entry_value))

    def handle_solver_failure(self, entry, index, entry_value):
        solver.domains[index] = {int(entry_value)}
        entry.configure(fg_color="lightsalmon")

    def increment_counter(self):
        self.counter += 1
        self.counter_label.configure(text=str(self.counter))




    def remove_element(self, index):
        solver.domains[index]  =  set(range(1,solver.dim + 1))

        solver.sudoku_reduction()

        solver.length_values[index] = len(solver.domains[index])



    def clean_matrix(self):
        self.matrix = np.zeros((solver.dim, solver.dim))
        for row in range(solver.dim):
            for col in range(solver.dim):
                self.entries_index[row, col].configure(state='normal')  # Ensure the entry is writable
                self.entries_index[row, col].configure(fg_color="white")
                self.entries_index[row, col].delete(0, END)  # Clear the entry

        solver.grid_insert(self.matrix , solver.dim)

    def start_timer(self):
        time_difficulty_relation = {(65, 70): 20, (75, 80): 10, (85, 90): 5}

        self.total_seconds = 60 * time_difficulty_relation[solver.difficulty_category]
        if not self.running:
            self.running = True
            self.update_timer()

    def update_timer(self):

        if self.total_seconds > 0 :
            self.total_seconds -=1
            self.time_label.configure(text = self.format_time())
            self.root.after(1000 , self.update_timer)

        else:
            self.game_end()

    def game_end(self):
        self.total_seconds = 0
        self.time_label.configure(text = "Game Over")
    def format_time(self):
        minutes, seconds = divmod(self.total_seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def create_game(self):
        self.root.destroy()
        Start_SudokuGUI()





class Start_SudokuGUI:
    def __init__(self):
        self.setup_gui()

    def setup_gui(self):
        self.start_widget = customtkinter.CTk()
        self.start_widget.title("Select Sudoku Dimension")
        self.start_widget.geometry("480x240")

        puzzle_dims = ["16", "9"]
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.selected_size = StringVar(value=puzzle_dims[0])
        self.selected_difficulty = StringVar(value=self.difficulties[0])

        # Configure the grid layout
        self.start_widget.columnconfigure(0, weight=1)
        self.start_widget.columnconfigure(1, weight=1)

        for index, option in enumerate(puzzle_dims):
            dim = customtkinter.CTkRadioButton(self.start_widget, text=f"{option}x{option}", variable=self.selected_size, value=option)
            dim.grid(row=index, column=0, padx=10, pady=5, sticky="w")

        for index, option in enumerate(self.difficulties):
            diff = customtkinter.CTkRadioButton(self.start_widget, text=option, variable=self.selected_difficulty, value=option.lower())
            diff.grid(row=index, column=1, padx=30, pady=20, sticky="w")

        solve_button = customtkinter.CTkButton(self.start_widget, text="Start", command=self.get_size)
        solve_button.grid(row=max(len(puzzle_dims), len(self.difficulties)), column=0, columnspan=2, padx=40, pady=20)

        self.start_widget.mainloop()
    def get_size(self):
        size = self.selected_size.get()
        difficulty_pointer = difficulty_ranges = {
                                    "easy": (65, 70),
                                    "medium": (75, 80),
                                    "hard": (85, 90)
                                }
        difficulty = difficulty_pointer[self.selected_difficulty.get().lower()]
        remove_elements = int(random.randint(difficulty[0], difficulty[1]))

        solver.difficulty_category = difficulty

        self.start_widget.destroy()  # Destroy the current window


        # Assuming Sudoku_GUI is defined elsewhere and takes size and difficulty parameters
        app = Sudoku_GUI(size, remove_elements)

if __name__ == "__main__":
    app = Start_SudokuGUI()

