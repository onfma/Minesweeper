import datetime
from tkinter import *
from game_logic import *
from datetime import timedelta, datetime as dt

# Global variables for Minesweeper game
dimX, dimY, numMines = 9, 9, 10             # Dimensions and number of mines for the game board
game_started = False                        # Flag to track whether the game has started
game_board = initialization(dimX, dimY)     # Initial game board state
custom_timer = 0                            # Custom timer setting for the game (0 means no timer)

class MinesweeperStartPage(Frame):
    def __init__(self, master=None):
        """
        Initializes the MinesweeperStartPage.
        :param master: The Tkinter master window.
        """
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        """
        Initializes the MinesweeperStartPage window layout.
        """
        self.master.title("Minesweeper")

        window_width = 800
        window_height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        for i in range(4):
            self.master.columnconfigure(i, weight=1)
        self.master.rowconfigure(0, minsize=10)
        self.master.rowconfigure(1, minsize=5)

        label = Label(self.master, text="Minesweeper", font=("Arial", 24, "bold"), fg="black")
        label.grid(row=0, column=0, columnspan=5, pady=50, padx=20)

        menu_frame = Frame(self.master)
        menu_frame.grid(row=1, column=0, columnspan=5, padx=20)

        difficulty_label = Label(menu_frame, text="Choose the game board:", font=("Arial", 10), fg="black")
        difficulty_label.grid(row=0, column=0, columnspan=4, pady=10)
        self.difficulty_var = StringVar(value="easy")

        timer_label = Label(menu_frame, text="Additionally, set a timer for your game: \n (in seconds)",
                            font=("Arial", 10), fg="black")
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
        """
        Starts the Minesweeper game based on the selected difficulty settings.
        """
        global dimX, dimY, numMines, custom_timer
        selected_difficulty = self.difficulty_var.get()

        difficulty_settings = {
            "easy": (9, 9, 10),
            "medium": (16, 16, 40),
            "hard": (16, 30, 99),
            "custom": (
                int(self.custom_width_spinner.get()),
                int(self.custom_height_spinner.get()),
                int(self.custom_mines_spinner.get()),
            ),
        }

        dimX, dimY, numMines = difficulty_settings.get(selected_difficulty, (9, 9, 10))
        custom_timer = int(self.custom_timer_spinner.get())

        print(f"Game started with {selected_difficulty}")

        self.master.destroy()

        root = Tk()
        app = MinesweeperGamePage(root)
        root.mainloop()

class MinesweeperGamePage(Frame):
    """
    This class represents the main page for the Minesweeper game. It includes the game grid, timer, and various controls.
    For an overview of how the game works, refer to the comments provided in each method below.
    """
    def __init__(self, master=None):
        """
        Constructor for the MinesweeperGamePage class. Initializes the game page with a grid, timer, and other elements.
        :param master: The master widget (usually a Tkinter window) that this page belongs to.
        """
        super().__init__(master)
        self.master = master
        self.cell_label = [[Label() for y in range(dimY)] for x in range(dimX)]
        self.boolean_cell_label = [[False for y in range(dimY)] for x in range(dimX)]
        self.num_mines_view = Label()

        self.timer_label = Label()
        self.start_time = None

        self.init_window()

    def init_window(self):
        """
        Initializes the window layout, including labels, buttons, and the game grid.
        """
        self.master.title("Minesweeper")

        window_width = 800
        window_height = 700
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        for i in range(4):
            self.master.columnconfigure(i, weight=1)

        for i in range(2):
            self.master.rowconfigure(i, minsize=10)

        label = Label(self.master, text="Minesweeper", font=("Arial", 24, "bold"), fg="black")
        label.grid(row=0, column=0, columnspan=4, pady=50, padx=20)

        main_frame = Frame(self.master, width=400, height=300)
        main_frame.grid(row=1, column=0, columnspan=4, padx=20)

        menu_frame = Frame(main_frame, width=400, height=40)
        menu_frame.grid(row=1, pady=20)

        self.num_mines_view = Label(menu_frame, text="Mines: " + str(numMines), font=("Arial", 10), fg="black", bg="yellow")
        self.num_mines_view.grid(row=0, column=0, padx=20)

        restart = Button(menu_frame, text="Restart", bg="yellow", command=self.restart_game)
        restart.grid(row=0, column=1, padx=20)

        self.timer_label = Label(menu_frame, text="00:00:00", font=("Arial", 10), fg="black", bg="yellow")
        self.timer_label.grid(row=0, column=2, padx=20)

        game_frame = Frame(main_frame, width=400, height=260, bd=5, relief="solid", borderwidth=5)
        game_frame.grid(row=0)

        self.cell_label = [
            [Label(game_frame, text="", width=2, height=1, bg="lightgrey", relief="raised") for y in range(dimY)]
            for x in range(dimX)
        ]
        self.boolean_cell_label = [[True for y in range(dimY)] for x in range(dimX)]

        for x in range(dimX):
            for y in range(dimY):
                self.cell_label[x][y].grid(row=x, column=y, padx=1, pady=1)
                self.cell_label[x][y].bind("<Button-1>", lambda event, x=x, y=y: self.click_cell(x, y))
                self.cell_label[x][y].bind("<Button-3>", lambda event, x=x, y=y: self.mark_cell(x, y))

    def restart_game(self):
        """
        Restarts the Minesweeper game by destroying the current window and creating a new one.
        """
        global game_started
        game_started = False
        self.master.destroy()
        root = Tk()
        app = MinesweeperStartPage(root)
        root.mainloop()

    def start_game(self, x, y):
        """
        Starts the Minesweeper game with the specified dimensions and number of mines.
        :param x: X-coordinate of the first click.
        :param y: Y-coordinate of the first click.
        """
        global dimX, dimY, numMines, game_board
        game_board = start_initialization(initialization(dimX, dimY), numMines, (x, y))
        print_game(game_board)
        self.start_timer()

    def click_cell(self, x, y):
        """
        Handles the left-click event on a Minesweeper cell.
        :param x: X-coordinate of the clicked cell.
        :param y: Y-coordinate of the clicked cell.
        """
        global game_started, game_board

        if not game_started:
            var = ""
        else:
            var = get_val_from_poz(game_board, x, y)
            var = "" if var == -1 else str(var)

        self.boolean_cell_label[x][y] = False
        self.cell_label[x][y].destroy()
        new_label = Label(self.cell_label[x][y].master, text=var, width=2, height=1)
        new_label.grid(row=x, column=y, padx=1, pady=1)

        if not game_started:
            game_started = True
            self.start_game(x, y)
        else:
            make_move(game_board, click_type, x, y)

        self.state_verifier()

    def mark_cell(self, x, y):
        """
        Marks a Minesweeper cell with a flag using right-click.
        :param x: X-coordinate of the flagged cell.
        :param y: Y-coordinate of the flagged cell.
        """
        global numMines
        if game_started:
            make_move(game_board, mark_type, x, y)
            self.cell_label[x][y] = Label(self.cell_label[x][y].master, text="", width=2, height=1, bg="red", relief="raised")
            self.cell_label[x][y].grid(row=x, column=y, padx=1, pady=1)
            self.cell_label[x][y].bind("<Button-3>", lambda event, x=x, y=y: self.unmark_cell(x, y))
            numMines -= 1
            self.state_verifier()

    def unmark_cell(self, x, y):
        """
        Unmarks a Minesweeper cell, removing the flag.
        :param x: X-coordinate of the unmarked cell.
        :param y: Y-coordinate of the unmarked cell.
        """
        global numMines
        if game_started:
            make_move(game_board, mark_type, x, y)
            self.cell_label[x][y] = Label(self.cell_label[x][y].master, text="", width=2, height=1, bg="lightgrey", relief="raised")
            self.cell_label[x][y].grid(row=x, column=y, padx=1, pady=1)
            self.cell_label[x][y].bind("<Button-1>", lambda event, x=x, y=y: self.click_cell(x, y))
            self.cell_label[x][y].bind("<Button-3>", lambda event, x=x, y=y: self.mark_cell(x, y))
            numMines += 1
            self.state_verifier()

    def state_verifier(self):
        """
        Verifies the current state of the Minesweeper game and takes appropriate actions.
        """
        if verify_state(game_board) == still_going_state:
            self.num_mines_view = Label(self.num_mines_view.master, text="Mines: " + str(numMines), font=("Arial", 10), fg="black", bg="yellow")
            self.num_mines_view.grid(row=0, column=0, padx=20)

            for x in range(dimX):
                for y in range(dimY):
                    if game_board[x][y][1] == uncoverd_cell and self.boolean_cell_label[x][y]:
                        self.click_cell(x, y)

        elif verify_state(game_board) == game_over_state:
            self.stop_timer()
            self.show_game_over_window()

        elif verify_state(game_board) == game_won_state:
            self.stop_timer()
            self.show_game_won_window()

    def show_game_over_window(self):
        """
        Displays a popup window when the game is over.
        """
        game_over_window = Toplevel(self.master)
        game_over_window.title("Game Over")

        game_over_label = Label(game_over_window, text="OPS! You just hit a mine... Game Over :(", fg="red")
        game_over_label.pack(pady=10)

        reset_lost_game_button = Button(game_over_window, text="New Game", command=lambda: self.reset_lost_game(game_over_window))
        reset_lost_game_button.pack(pady=10)

        game_over_window.protocol("WM_DELETE_WINDOW", lambda: None)

        self.center_window(game_over_window)

    def show_game_won_window(self):
        """
        Displays a popup window when the game is won.
        """
        game_win_window = Toplevel(self.master)
        game_win_window.title("Game Won")

        game_win_label = Label(game_win_window, text="Congrats! You found all the mines :)", fg="green")
        game_win_label.pack(pady=10)

        reset_lost_game_button = Button(game_win_window, text="New Game", command=lambda: self.reset_lost_game(game_win_window))
        reset_lost_game_button.pack(pady=10)

        game_win_window.protocol("WM_DELETE_WINDOW", lambda: None)

        self.center_window(game_win_window)

    def reset_lost_game(self, game_over_window):
        """
        Resets the game after a loss.
        :param game_over_window: The window displaying the game-over message.
        """
        game_over_window.destroy()
        self.restart_game()

    def start_timer(self):
        """
        Starts the game timer.
        """
        self.start_time = datetime.datetime.now()
        self.update_timer()

    def stop_timer(self):
        """
        Stops the game timer.
        """
        if self.start_time is not None:
            self.start_time = None

    def update_timer(self):
        """
        Updates the game timer based on elapsed time.
        """
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
                self.show_finish_timer_window()
            else:
                self.master.after(1000, self.update_timer)

    def show_finish_timer_window(self):
        """
        Displays a pop-up window when the game timer reaches zero.
        This window indicates that the player has run out of time to complete the Minesweeper game.
        Provides an option to start a new game.
        """
        finish_timer_window = Toplevel(self.master)
        finish_timer_window.title("Game Over")

        finish_timer_label = Label(finish_timer_window, text="OPS! The time was not enough.. ", fg="red")
        finish_timer_label.pack(pady=10)

        reset_lost_game_button = Button(finish_timer_window, text="New Game", command=lambda: self.reset_lost_game(finish_timer_window))
        reset_lost_game_button.pack(pady=10)

        finish_timer_window.protocol("WM_DELETE_WINDOW", lambda: None)

        self.center_window(finish_timer_window)

    def center_window(self, window):
        """
        Centers a given window on the screen relative to the MinesweeperGamePage's master window.
        :param window: The Tkinter window to be centered.
        """
        x = self.master.winfo_x() + (self.master.winfo_width() - window.winfo_reqwidth()) // 2
        y = self.master.winfo_y() + (self.master.winfo_height() - window.winfo_reqheight()) // 2
        window.geometry("+{}+{}".format(x, y))
   
if __name__ == "__main__":
    root = Tk()
    app = MinesweeperStartPage(root)
    root.mainloop()
