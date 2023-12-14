import datetime
from tkinter import *
import tkinter as tk
from game_logic import *
from datetime import timedelta, datetime as dt

dimX, dimY, numMines = 9, 9, 10
game_started = False
game_board = initialization(dimX, dimY)
custom_timer = 0

class MinesweeperStartPage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
    
    def init_window(self):
        self.master.title("Minesweeper")

        window_width = 800
        window_height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1) 
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(0, minsize=10)
        self.master.rowconfigure(1, minsize=5)

        label = Label(self.master, text="Minesweeper", font=("Arial", 24, "bold"), fg="black")
        label.grid(row=0, column=0, columnspan=5, pady=50, padx=20)

        menu_frame = Frame(self.master)
        menu_frame.grid(row=1, column=0, columnspan=5, padx=20)

        difficulty_label = Label(menu_frame, text="Choose the game board:", font=("Arial", 10), fg="black")
        difficulty_label.grid(row=0, column=0, columnspan=4, pady=10)
        self.difficulty_var = StringVar(value="easy")

        timer_label = Label(menu_frame, text="Additionaly, set a timer for your game: \n (in seconds)", font=("Arial", 10), fg="black")
        timer_label.grid(row=6, column=0, columnspan=4, pady=10)
        self.custom_timer_spinner = Spinbox(menu_frame, from_=0, to=1000000, width=15)
        self.custom_timer_spinner.grid(row=7, column=0, columnspan=4)

        height_label = Label(menu_frame, text="Height", font=("Arial", 8), fg="black")
        width_label = Label(menu_frame, text="Width", font=("Arial", 8), fg="black")
        mines_label = Label(menu_frame, text="Mines", font=("Arial", 8), fg="black")
        height_label.grid(row=1, column=1)
        width_label.grid(row=1, column=2)
        mines_label.grid(row=1, column=3)

        easy_button = Radiobutton(menu_frame, text="Easy", variable=self.difficulty_var, value="easy")
        easy_height_label = Label(menu_frame, text="9", fg="black")
        easy_width_label = Label(menu_frame, text="9", fg="black")
        easy_mines_label = Label(menu_frame, text="10", fg="black")
        easy_button.grid(row=2, column=0, sticky="w")
        easy_height_label.grid(row=2, column=1)
        easy_width_label.grid(row=2, column=2)
        easy_mines_label.grid(row=2, column=3)

        medium_button = Radiobutton(menu_frame, text="Medium", variable=self.difficulty_var, value="medium")
        medium_height_label = Label(menu_frame, text="16", fg="black")
        medium_width_label = Label(menu_frame, text="16", fg="black")
        medium_mines_label = Label(menu_frame, text="40", fg="black")
        medium_button.grid(row=3, column=0, sticky="w")
        medium_height_label.grid(row=3, column=1)
        medium_width_label.grid(row=3, column=2)
        medium_mines_label.grid(row=3, column=3)

        hard_button = Radiobutton(menu_frame, text="Hard", variable=self.difficulty_var, value="hard")
        hard_height_label = Label(menu_frame, text="16", fg="black")
        hard_width_label = Label(menu_frame, text="30", fg="black")
        hard_mines_label = Label(menu_frame, text="99", fg="black")
        hard_button.grid(row=4, column=0, sticky="w")
        hard_height_label.grid(row=4, column=1)
        hard_width_label.grid(row=4, column=2)
        hard_mines_label.grid(row=4, column=3)

        custom_button = Radiobutton(menu_frame, text="Custom", variable=self.difficulty_var, value="custom")
        self.custom_height_spinner = Spinbox(menu_frame, from_=4, to=40, width=4)
        self.custom_width_spinner = Spinbox(menu_frame, from_=4, to=40, width=4)
        self.custom_mines_spinner = Spinbox(menu_frame, from_=1, to=99, width=4)
        custom_button.grid(row=5, column=0, sticky="w")
        self.custom_height_spinner.grid(row=5, column=1)
        self.custom_width_spinner.grid(row=5, column=2)
        self.custom_mines_spinner.grid(row=5, column=3)

        start_button = Button(self.master, text="Start Game", bg="yellow", command=self.start_game)
        start_button.grid(row=2, columnspan=4, pady=50)

    def start_game(self):
        global dimX, dimY, numMines, custom_timer
        selected_difficulty = self.difficulty_var.get()

        if selected_difficulty == "easy":
            dimX = 9
            dimY = 9
            numMines = 10
        elif selected_difficulty == "medium":
            dimX = 16
            dimY = 16
            numMines = 40
        elif selected_difficulty == "hard":
            dimX = 16
            dimY = 30
            numMines = 99
        elif selected_difficulty == "custom":
            dimX = int(self.custom_width_spinner.get())
            dimY = int(self.custom_height_spinner.get())
            numMines = int(self.custom_mines_spinner.get())

        custom_timer = int(self.custom_timer_spinner.get())

        print(f"Game started with {selected_difficulty}")

        self.master.destroy()

        root = Tk()
        app = MinesweeperGamePage(root)
        root.mainloop()

class MinesweeperGamePage(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.cell_label = [[Label() for y in range(dimY)] for x in range(dimX)]
        self.boolean_cell_label = [[False for y in range(dimY)] for x in range(dimX)]
        self.numMinesView = Label()

        self.timer_label = Label()
        self.start_time = None

        self.init_window()
    
    def init_window(self):
        self.master.title("Minesweeper")

        window_width = 800
        window_height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1) 
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.rowconfigure(0, minsize=10)
        self.master.rowconfigure(1, minsize=5)

        label = Label(self.master, text="Minesweeper", font=("Arial", 24, "bold"), fg="black")
        label.grid(row=0, column=0, columnspan=5, pady=50, padx=20)

        main_frame = Frame(self.master, width=400, height=300)
        main_frame.grid(row=1, column=0, columnspan=5, padx=20)

        menu_frame = Frame(main_frame, width=400, height=40)
        menu_frame.grid(row=1, pady=20)

        self.numMinesView = Label(menu_frame, text="Mines: " + str(numMines), font=("Arial", 10), fg="black", bg="yellow")
        self.numMinesView.grid(row=0, column=0, padx=20)

        restart = Button(menu_frame, text="Restart", bg="yellow", command=self.restart_game)
        restart.grid(row=0, column= 1, padx=20)

        self.timer_label = Label(menu_frame, text="00:00:00", font=("Arial", 10), fg="black", bg="yellow")
        self.timer_label.grid(row=0, column= 2, padx=20)

        game_frame = Frame(main_frame, width=400, height=260, bd=5, relief="solid", borderwidth=5)
        game_frame.grid(row=0)

        self.cell_label = [[Label(game_frame, text="", width=2, height=1, bg="lightgrey", relief="raised") for y in range(dimY)] for x in range(dimX)]
        self.boolean_cell_label = [[True for y in range(dimY)] for x in range(dimX)]
        for x in range(dimX):
            for y in range(dimY):
                self.cell_label[x][y].grid(row=x, column=y, padx=1, pady=1)
                self.cell_label[x][y].bind("<Button-1>", lambda event, x=x, y=y: self.click_cell(x, y))
                self.cell_label[x][y].bind("<Button-3>", lambda event, x=x, y=y: self.mark_cell(x, y))

    def restart_game(self):
        global game_started
        game_started = False
        self.master.destroy()
        root = Tk()
        app = MinesweeperStartPage(root)
        root.mainloop()

    def click_cell(self, x, y):
        global game_started, game_board

        # afisare valoare box din mapa de joc
        if not game_started: var = ""
        else:
            var = get_val_from_poz(game_board, x, y)
            if var == -1:
                var = ""
            else:
                var = str(var)
        self.boolean_cell_label[x][y] = False
        self.cell_label[x][y].destroy()
        new_label = Label(self.cell_label[x][y].master, text=var, width=2, height=1)
        new_label.grid(row=x, column=y, padx=1, pady=1)

        # first game move
        if not game_started:
            game_started = True
            self.start_game(x, y)

        # game move
        else:
            make_move(game_board, click_type, x, y)
        
        self.state_verifier()

    def mark_cell(self, x, y):
        global numMines
        if game_started:
            make_move(game_board, mark_type, x, y)
            self.cell_label[x][y] = Label(self.cell_label[x][y].master, text="", width=2, height=1, bg="red", relief="raised")
            self.cell_label[x][y].grid(row=x, column=y, padx=1, pady=1)
            self.cell_label[x][y].bind("<Button-3>", lambda event, x=x, y=y: self.unmark_cell(x, y))
            numMines -= 1
            self.state_verifier()

    def unmark_cell(self, x, y):
        global numMines
        if game_started:
            make_move(game_board, mark_type, x, y)
            self.cell_label[x][y] = Label(self.cell_label[x][y].master, text="", width=2, height=1, bg="lightgrey", relief="raised")
            self.cell_label[x][y].grid(row=x, column=y, padx=1, pady=1)
            self.cell_label[x][y].bind("<Button-1>", lambda event, x=x, y=y: self.click_cell(x, y))
            self.cell_label[x][y].bind("<Button-3>", lambda event, x=x, y=y: self.mark_cell(x, y))
            numMines +=1
            self.state_verifier()

    def state_verifier(self):
        if verify_state(game_board) == still_going_state:
            self.numMinesView = Label(self.numMinesView.master, text="Mines: " + str(numMines), font=("Arial", 10), fg="black", bg="yellow")
            self.numMinesView.grid(row=0, column=0, padx= 20)

            for x in range(dimX):
                for y in range(dimY):
                    if game_board[x][y][1] == uncoverd_cell and self.boolean_cell_label[x][y]:
                        self.click_cell(x, y)

        elif verify_state(game_board) == game_over_state:
            self.stop_timer()
            game_over_window = Toplevel(self.master)
            game_over_window.title("Game Over")

            game_over_label = Label(game_over_window, text="OPS! You just hit a mine... Game Over :(", fg="red")
            game_over_label.pack(pady=10)

            reset_lost_game_button = Button(game_over_window, text="New Game", command=lambda: self.reset_lost_game(game_over_window))
            reset_lost_game_button.pack(pady=10)

            game_over_window.protocol("WM_DELETE_WINDOW", lambda: None)

            x = self.master.winfo_x() + (self.master.winfo_width() - game_over_window.winfo_reqwidth()) // 2
            y = self.master.winfo_y() + (self.master.winfo_height() - game_over_window.winfo_reqheight()) // 2
            game_over_window.geometry("+{}+{}".format(x, y))

        elif verify_state(game_board) == game_won_state:
            self.stop_timer()
            game_win_window = Toplevel(self.master)
            game_win_window.title("Game Won")

            game_win_label = Label(game_win_window, text="Congrats! You found all the mines :)", fg="green")
            game_win_label.pack(pady=10)

            reset_lost_game_button = Button(game_win_window, text="New Game", command=lambda: self.reset_lost_game(game_win_window))
            reset_lost_game_button.pack(pady=10)

            game_win_window.protocol("WM_DELETE_WINDOW", lambda: None)

            x = self.master.winfo_x() + (self.master.winfo_width() - game_win_window.winfo_reqwidth()) // 2
            y = self.master.winfo_y() + (self.master.winfo_height() - game_win_window.winfo_reqheight()) // 2
            game_win_window.geometry("+{}+{}".format(x, y))

    def start_game(self, x, y):
        global dimX, dimY, numMines, game_board
        game_board = start_initialization(initialization(dimX, dimY), numMines, (x,y))
        print_game(game_board)
        self.start_timer()

    def start_timer(self):
        self.start_time = datetime.datetime.now()

        self.update_timer()

    def stop_timer(self):
        if self.start_time is not None:
            self.start_time = None

    def update_timer(self):
        global custom_timer
        if custom_timer == 0:
            if self.start_time is not None:
                current_time = datetime.datetime.now()
                elapsed_time = current_time - self.start_time
                elapsed_seconds = int(elapsed_time.total_seconds())
                formatted_time = str(datetime.timedelta(seconds=elapsed_seconds)).split(".")[0]
                self.timer_label.config(text=formatted_time)
                self.master.after(1000, self.update_timer)
        elif custom_timer > 0:
            current_time = datetime.datetime.now()
            elapsed_time = current_time - self.start_time
            elapsed_seconds = int(elapsed_time.total_seconds())
            formatted_time = str(datetime.timedelta(seconds=elapsed_seconds)).split(".")[0]
            self.timer_label.config(text=formatted_time)

            if elapsed_seconds == custom_timer:
                self.stop_timer()
                finish_timer_window = Toplevel(self.master)
                finish_timer_window.title("Game Won")

                game_win_label = Label(finish_timer_window, text="OPS! The time was not enaught.. ", fg="red")
                game_win_label.pack(pady=10)

                reset_lost_game_button = Button(finish_timer_window, text="New Game", command=lambda: self.reset_lost_game(finish_timer_window))
                reset_lost_game_button.pack(pady=10)

                finish_timer_window.protocol("WM_DELETE_WINDOW", lambda: None)

                x = self.master.winfo_x() + (self.master.winfo_width() - finish_timer_window.winfo_reqwidth()) // 2
                y = self.master.winfo_y() + (self.master.winfo_height() - finish_timer_window.winfo_reqheight()) // 2
                finish_timer_window.geometry("+{}+{}".format(x, y))
            else:
                self.master.after(1000, self.update_timer)

    def reset_lost_game(self, game_over_window):
        game_over_window.destroy()
        self.restart_game()
    
if __name__ == "__main__":
    root = Tk()
    app = MinesweeperStartPage(root)
    root.mainloop()
