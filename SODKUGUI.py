import re
from tkinter import *
from Sodku import * 

class Sudoku_GUI(Sudoku_structure):
    def __init__(self,dim,diffculty):
        self.dim = int(dim)         
        self.diffculty = int(diffculty)
        self.root = Tk()
        self.root.title("Sudoku")
        
        self.Sodku_creator(self.diffculty)
        
        self.create_entries()
        


        self.root.mainloop()

            
    def create_entries(self):
        self.matrix_entries = []
        for i in range(self.dim):
            row_entries = []
            for j in range(self.dim):
                entry = Entry(self.root, width=3, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.bind("<Return>",self.on_enter)
                entry.insert(0, str(self.matrix[i, j]) if self.matrix[i, j] != 0 else '')
                
                
                row_entries.append(entry)
        
                
                
            self.matrix_entries.append(row_entries)

        Solve_button = Button(self.root , text ="Solve Sodku" , command = self.solveSudoku)
        Solve_button.grid(row = self.dim+1  , column = self.dim+1 )        
                
    def on_enter(self,event):
        entry = event.widget 
        index = np.unravel_index(int((''.join(re.findall(r'\d', str(event.widget)))))-1,self.matrix.shape)
        
        if self.enter_element(index[0] , index[1] , int(entry.get())):
            self.matrix[index] = entry.get()
        
            
        
        print(self.matrix) 
        
        
        
        
        
        
        
        
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


