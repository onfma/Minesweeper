# Constants
blank_cell = -1         # Representation for an empty cell in the game
mine_cell = 0           # Representation for a cell containing a mine in the game

start_cell = -1         # The cell pressed at the beginning of the game (always empty)
coverd_cell = 0         # The cell untouched by the player during the game
uncoverd_cell = 1       # The cell touched by the player during the game
marked_cell = 2         # The cell marked by the player as a mine

game_over_state = -1    # Game state indicating the game is over
still_going_state = 0   # Game state indicating the game is still in progress
game_won_state = 1      # Game state indicating the game is won

click_type = 0          # Type of move: clicking on a cell
mark_type = 1           # Type of move: marking a cell as a mine
