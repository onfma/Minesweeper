import random
from predef import *
from colorama import Fore, Style, init
init(autoreset=True)

def get_val_from_poz(tabela, x, y):
     return tabela[x][y][0]

def print_game(tabela):
    for row in tabela:
        for element in row:
            if element[1] == start_cell:
                color = Fore.GREEN
                # color = Fore.WHITE
            elif element[0] == mine_cell:
                color = Fore.RED
                # color = Fore.WHITE
            elif element[0] == blank_cell:
                # color = Fore.BLACK
                color = Fore.WHITE
            else:
                color = Fore.YELLOW
                # color = Fore.WHITE

            if  element[1] == coverd_cell:
                print(f'{color}{"*":2}{Style.RESET_ALL} | ', end='')
            else:
                print(f'{color}{element[0]:2}{Style.RESET_ALL} | ', end='')

        print()

def make_move(tabela, move_type, x, y):
    if move_type == click_type:
        if tabela[x][y][0] == blank_cell:
            uncover_area(tabela, x, y)
        else:
            tabela[x][y] = (tabela[x][y][0], uncoverd_cell)
    elif move_type == mark_type:
        tabela[x][y] = (tabela[x][y][0], marked_cell)

def verify_state(tabela):
    win = True
    for x in range(len(tabela)):
        for y in range(len(tabela[0])):
            if tabela[x][y][0] == mine_cell and tabela[x][y][1] == uncoverd_cell:
                return game_over_state
            elif (tabela[x][y][0] == -1 or tabela[x][y][0] > 0) and (tabela[x][y][1] == coverd_cell or tabela[x][y][1] == marked_cell):
                win = False
    
    if win:
        return game_won_state
    else:
        return still_going_state

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
