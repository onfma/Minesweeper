import numpy
import random
from colorama import Fore, Style, init
init(autoreset=True)



blank_cell = -1
mine_cell = 0

start_cell = -1     # celula apasata la inceputul jocului (mereu goala)
coverd_cell = 0     # celula neatinsa inca de player in timpul jocului
uncoverd_cell = 1   # celula atinsa de player in timpul jocului
marked_cell = 2     # celula marcata de player ca fiind mine

game_over_state = -1
still_going_state = 0
game_won_state = 1



def print_game(tabela):
    for row in tabela:
        for element in row:
            if element[1] == start_cell:
                # color = Fore.GREEN
                color = Fore.WHITE
            elif element[0] == mine_cell:
                # color = Fore.RED
                color = Fore.WHITE
            elif element[0] == blank_cell:
                # color = Fore.BLACK
                color = Fore.WHITE
            else:
                # color = Fore.YELLOW
                color = Fore.WHITE

            if  element[1] == coverd_cell:
                print(f'{color}{"*":2}{Style.RESET_ALL} | ', end='')
            else:
                print(f'{color}{element[0]:2}{Style.RESET_ALL} | ', end='')

        print()

def verify_state(tabela):
    win = True
    for row in tabela:
        for element in row:
            if element[0] == mine_cell:
                if element[1] != marked_cell:
                    win = False
                elif element[1] == uncoverd_cell:
                    return game_over_state
            elif element[0] > 1 and element[1] == coverd_cell:
                return still_going_state
    if win:
        return game_won_state

def mines_assignation(tabela, num_mines):
    directii = [-1, 0, 1]
    start_vecinity = []
    for x in range(len(tabela)):
        for y in range(len(tabela[0])):
            if tabela[x][y][1] == start_cell:
                start_vecinity.append((x, y))
                for i in directii:
                    for j in directii:
                        if 0 <= x + i < len(tabela) and 0 <= y + j < len(tabela[0]):
                            start_vecinity.append((x+i, y+j))
            
    all_coordinates = [(x, y) for x in range(len(tabela)) for y in range(len(tabela[0])) if (x,y) not in start_vecinity]
    mine_coordinates = random.sample(all_coordinates, num_mines)

    for x, y in mine_coordinates:
        tabela[x][y] = (mine_cell, coverd_cell)

def value_assignation(tabela):
    directii = [-1, 0, 1]
    for x in range(len(tabela)):
        for y in range(len(tabela[0])):
            vecini = 0
            if tabela[x][y][0] != mine_cell:
                for i in directii:
                    for j in directii:
                        if 0 <= x + i < len(tabela) and 0 <= y + j < len(tabela[0]):
                            if tabela[x + i][y + j][0] == mine_cell:
                                vecini += 1
                if vecini:
                    tabela[x][y] = (vecini, tabela[x][y][1])

def uncover_area(tabela, x, y):
    tabela[x][y] = (tabela[x][y][0], uncoverd_cell)
    directii = [-1, 0, 1]
    for i in directii:
        for j in directii:
            if 0 <= x + i < len(tabela) and 0 <= y + j < len(tabela[0]):
                if tabela[x+i][y+j][1] == coverd_cell:
                    if tabela[x+i][y+j][0] != blank_cell:
                        tabela[x+i][y+j] = (tabela[x+i][y+j][0], uncoverd_cell)
                    else:
                        uncover_area(tabela, x+i, y+j)

def start_initialization(tabela, num_mines, start_cell_poz):
    tabela[start_cell_poz[0]][start_cell_poz[1]] = (blank_cell, start_cell)
    mines_assignation(tabela, num_mines)
    value_assignation(tabela)
    uncover_area(tabela, start_cell_poz[0], start_cell_poz[1])
    return tabela

def initialization(dimX, dimY):
    tabela = [[(blank_cell, coverd_cell) for y in range(dimY)] for x in range(dimX)]
    return tabela
    

def minesweeper():
    dimX = 9
    dimY = 9
    num_mines = 10
    game_board = initialization(dimX, dimY)
    start_cell_poz = (4,3)
    game_board = start_initialization(game_board, num_mines, start_cell_poz)
    print_game(game_board)
    if verify_state(game_board) == still_going_state:
        print("aaaa")

    if verify_state(game_board) == game_over_state:
        print("OPS! You just hit a mine... Game Over :(")
    elif verify_state(game_board) == game_won_state:
        print("Congrats! You found all the mines :)")

minesweeper()