from Sodku import *


class Sudoku_GUI(Sudoku_structure):
    def __init__(self, dim, difficulty):
        self.dim = int(dim)         
        self.difficulty = difficulty
        self.root = Tk()
        self.root.title("Sudoku")
        self.root.geometry("1270x720")

        self.matrix_entries = {}
        self.Sodku_creator(self.difficulty)
        
        self.create_entries()
        self.root.mainloop()

    def create_entries(self):
        for i in range(self.dim):
            for j in range(self.dim):
                entry = Entry(self.root, width=3, font=("Arial", 12), justify='center')
                entry.grid(row=i, column=j, padx=10, pady=10)
                entry.bind("<Return>", self.on_enter)
                if self.matrix[i, j] != 0:
                    entry.insert(0, str(self.matrix[i, j]))
                    entry.config(state='readonly')  # Make initial numbers read-only
                self.matrix_entries[entry] = (i, j)
                
        self.entries_index = np.array(list(self.matrix_entries.keys()))
        self.entries_index = self.entries_index.reshape(self.dim , self.dim)
        solve_button = Button(self.root, text="Solve", command=lambda : self.solveSudoku(0 , 0 ,False))
        clean_button = Button(self.root , text ="clean" , command = self.clean_matrix)
        sodku_create = Button(self.root , text = "new game" , command = self.create_game)
        
        solve_button.grid(row=self.dim+1, column=self.dim//2, columnspan=self.dim//2)
        clean_button.grid(row=self.dim+1, column=(self.dim//2)+3, columnspan=self.dim//2)
        sodku_create.grid(row=self.dim+1, column=(self.dim//2)+5, columnspan=self.dim//2)

    def on_enter(self, event):
        entry= event.widget 
        entry_value = entry.get()
        index = self.matrix_entries[entry]
        if not entry_value.isdigit() or not (1 <= int(entry_value) <= self.dim):
            entry.delete(0, END)
            entry.config(bg="red")
            self.matrix[index] = 0
            entry.config(bg="white")
            return
        if self.enter_element(index[0], index[1], int(entry_value)):
            self.matrix[self.matrix_entries[entry][0] , self.matrix_entries[entry][1]] = int(entry_value)
            entry.config(bg="white")
        else:
            self.matrix[self.matrix_entries[entry][0] , self.matrix_entries[entry][1]] = int(entry_value)

            entry.config(bg="Salmon1")
            
            
            
            
            
            
    def clean_matrix(self):
        self.matrix = np.zeros((self.dim, self.dim))
        for i in range(self.dim):
            for j in range(self.dim):
                self.entries_index[i, j].config(state='normal')  # Ensure the entry is writable
                self.entries_index[i, j].config(bg="white")
                self.entries_index[i, j].delete(0, END)  # Clear the entry
   
    
   
    def create_game(self):
        self.root.destroy()
        Start_SudokuGUI()
   

class Start_SudokuGUI(Sudoku_GUI):
    def __init__(self):
        self.sudoku_dim_selection()
    def sudoku_dim_selection(self):
        self.start_widget = Tk()
        self.start_widget.title("Select Sudoku Dimension")
        self.start_widget.geometry("200x100")
        puzzle_dims = ["16", "9"]
        self.selected_var = StringVar(value=puzzle_dims[0])

        for index, option in enumerate(puzzle_dims):
            dim = Radiobutton(self.start_widget, text=f"{option}x{option}", variable=self.selected_var, value=option)
            dim.grid(row=index, column=0, padx=10, pady=5)
        
        solve_button = Button(self.start_widget, text="Pick Size", command=self.get_size)
        solve_button.grid(row=len(puzzle_dims), column=0, padx=10, pady=10)
        self.entry = Entry(self.start_widget,width = 10)
        
        self.label = Label(self.start_widget,text = " diffculty level ").grid(row = 0 , column = len(puzzle_dims))
        self.entry.grid(row = 1 , column = len(puzzle_dims))
        self.start_widget.mainloop()

    def get_size(self):
        
        size = self.selected_var.get()
        self.diffculty =self.entry.get() 
        self.start_widget.destroy()
        app = Sudoku_GUI(size,self.diffculty)
                
if __name__ == "__main__":
    app = Start_SudokuGUI()

