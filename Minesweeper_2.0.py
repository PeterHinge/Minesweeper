import random
import itertools
import pygame

import time


class Minefield:

    def __init__(self, width, height, mines, scale=20):
        self.scale = scale
        self.width = width
        self.height = height
        self.mines = mines

        self.display_x = self.width * self.scale
        self.display_y = self.height * self.scale

        self.table = self.setup()

    def __repr__(self):
        print(self.table)

    def setup(self):
        return [[Cell(x, y, self.scale) for x in range(self.width)] for y in range(self.height)]

    def add_mines(self, cell):
        adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
        starting_tiles = adjacent_tiles + [[cell.x, cell.y]]
        for i in range(self.mines):
            is_mine = False
            while not is_mine:
                column = random.randint(0, self.width - 1)
                row = random.randint(0, self.height - 1)
                if not self.is_bomb(column, row) and [column, row] not in starting_tiles:
                    self.table[row][column].val = 9
                    is_mine = True

    def adjust_table(self):
        for row in range(len(self.table)):
            for column in range(len(self.table[row])):
                if self.table[row][column].val == 9:
                    adjacent_tiles = get_adjacent_tiles(column, row)
                    for tile in adjacent_tiles:
                        if self.is_inside_table(tile[0], tile[1]):
                            if not self.is_bomb(tile[0], tile[1]):
                                self.table[tile[1]][tile[0]].val += 1

    def is_inside_table(self, column, row):  # Checks if cell is inside the game table
        return 0 <= column <= self.width - 1 and 0 <= row <= self.height - 1

    def is_bomb(self, column, row):  # Checks if tile is a bomb
        return self.table[row][column].val == 9

    def open_game(self, cell):  # Opens up the game if the clicked on tile has no adjacent mines
        adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
        for tile in adjacent_tiles:
            if self.is_inside_table(tile[0], tile[1]):
                if not self.table[tile[1]][tile[0]].visible and not self.table[tile[1]][tile[0]].flag:
                    self.table[tile[1]][tile[0]].visible = True
                    if self.table[tile[1]][tile[0]].val == 0:  # Recursive step that ensures all white spaces are opened
                        self.open_game(self.table[tile[1]][tile[0]])


class Cell:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.width = x * scale
        self.height = y * scale
        self.rect = pygame.rect.Rect(self.width, self.height, scale, scale)

        self.val = 0
        self.visible = False
        self.flag = False

    def __repr__(self):
        print(self.rect)


def get_adjacent_tiles(x, y):  # Checks and return adjacent tiles
    neighbours = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    adjacent_tiles = []
    for coordinate in neighbours:
        adjacent_tiles.append([x + coordinate[0], y + coordinate[1]])
    return adjacent_tiles


def restart(width, height, mines):  # Restarts game
    game(width, height, mines)


########################################################################################################################
def two_rule_ai(board, cell):  # Rule based AI
    adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
    adjacent_mines = cell.val
    adjacent_unopened_squares = 0
    adjacent_flags = 0

    for tile in adjacent_tiles:
        if board.is_inside_table(tile[0], tile[1]):
            if not board.table[tile[1]][tile[0]].visible:
                adjacent_unopened_squares += 1
            if board.table[tile[1]][tile[0]].flag:
                adjacent_flags += 1

    if adjacent_mines == adjacent_unopened_squares:  # First Rule: Flag if unopened squares and adjacent mines are same
        for tile in adjacent_tiles:
            if board.is_inside_table(tile[0], tile[1]):
                if not board.table[tile[1]][tile[0]].visible:
                    board.table[tile[1]][tile[0]].flag = True

    if adjacent_mines == adjacent_flags:  # Second Rule: Opens squares if adjacent flags and adjacent mines are same
        for tile in adjacent_tiles:
            if board.is_inside_table(tile[0], tile[1]):
                if not board.table[tile[1]][tile[0]].visible and not board.table[tile[1]][tile[0]].flag:
                    board.table[tile[1]][tile[0]].visible = True

    return board


def optimal_choice_ai(board, unopened_cells, unopened_neighbours, mines_left):  # Probabilistic AI

    possible_states = list(itertools.product([True, False], repeat=len(unopened_cells)))
    valid_possible_states = []

    for state in possible_states[1:-1]:

        check_if_valid = True

        possible_board = board
        possible_cells = unopened_cells
        possible_neighbours = unopened_neighbours

        for i in range(len(state)):
            possible_cells[i].flag = state[i]

        for cell in possible_cells:
            possible_board.table[cell.y][cell.x].flag = cell.flag

        for neighbour in possible_neighbours:

            count_flags = 0
            adjacent_tiles = get_adjacent_tiles(neighbour.x, neighbour.y)

            for tile in adjacent_tiles:
                if possible_board.is_inside_table(tile[0], tile[1]):
                    if possible_board.table[tile[1]][tile[0]].flag:
                        count_flags += 1

            if neighbour.val != count_flags:
                check_if_valid = False
                break

        check_for_mine_overflow = 0
        for value in state:
            if value:
                check_for_mine_overflow += 1

        if check_for_mine_overflow > mines_left:
            check_if_valid = False

        if check_if_valid:
            valid_possible_states.append(state)

    if len(valid_possible_states) == 1:

        for state in valid_possible_states:

            for i in range(len(state)):
                unopened_cells[i].flag = state[i]

            for cell in unopened_cells:
                print([cell.x, cell.y])
                board.table[cell.y][cell.x].flag = cell.flag

            print("one solu")
            return board

    lowest_change_of_mine_list = []
    lowest_change_of_mine_cell = (0, 100)

    if len(valid_possible_states) is not 0:
        lowest_change_of_mine_list = [0 for i in range(len(valid_possible_states[0]))]

    for state in valid_possible_states:
        for i, value in enumerate(state):
            if value:
                lowest_change_of_mine_list[i] += 1

    if len(valid_possible_states) is not 0:
        for i, chance in enumerate(lowest_change_of_mine_list):
            for cell in unopened_cells:
                board.table[cell.y][cell.x].flag = False

            if chance == 0:
                board.table[unopened_cells[i].y][unopened_cells[i].x].visible = True
                print("0%: " + str([unopened_cells[i].x, unopened_cells[i].y]))

            if chance == len(valid_possible_states):
                board.table[unopened_cells[i].y][unopened_cells[i].x].flag = True
                print("100%: " + str([unopened_cells[i].x, unopened_cells[i].y]))

            if chance < lowest_change_of_mine_cell[1]:
                lowest_change_of_mine_cell = (i, chance)

        if 0 in lowest_change_of_mine_list or len(valid_possible_states) in lowest_change_of_mine_list:
            return board

        else:
            board.table[unopened_cells[lowest_change_of_mine_cell[0]].y][unopened_cells[lowest_change_of_mine_cell[0]].x].visible = True
            print("50%: " + str([unopened_cells[lowest_change_of_mine_cell[0]].x, unopened_cells[lowest_change_of_mine_cell[0]].y]))
            return board
########################################################################################################################


def game(width, height, mines):  # Main game

    pygame.init()
    pygame.display.set_caption("Danish Minesweeper")

    board = Minefield(width, height, mines)  # Initializes board

    screen = pygame.display.set_mode((board.display_x, board.display_y))  # Initializes screen

    first_move = True

    ai_on = False

    ai_visited_cells = []

    exit_game = False
    while not exit_game:

        open_cell_count = 0

        flag_count = 0

        for row in board.table:  # Counts open (visible) cells
            for cell in row:
                if cell.visible and cell.val != 9:
                    open_cell_count += 1

                if cell.flag is True:
                    flag_count += 1

            if open_cell_count == width * height - mines:  # Checks if all non-mine squares are open (win)
                exit_game = True
                print("You Win!")
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quit game event
                exit_game = True
                pygame.quit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:  # Restart game event
                    exit_game = True
                    restart(width, height, mines)

                elif event.key == pygame.K_c:  # Turn AI on/off event
                    if not ai_on:
                        ai_on = True
                    elif ai_on:
                        ai_on = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:  # Left mouse-click event

                    for row in board.table:
                        for cell in row:
                            r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if cell.rect.colliderect(r):
                                if first_move is True:
                                    board.add_mines(cell)
                                    board.adjust_table()
                                    first_move = False
                                if not cell.flag:
                                    if cell.val == 9:
                                        print("Game over!")
                                        print("Press 'r' to try again or close the window to exit!")
                                        exit_game = True
                                    cell.visible = True
                                    if cell.val == 0:
                                        board.open_game(cell)

                elif event.button == 3:  # Right mouse-click event
                    for row in board.table:
                        for cell in row:
                            r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if cell.rect.colliderect(r):
                                if not cell.visible:
                                    if not cell.flag:
                                        cell.flag = True
                                    elif cell.flag:
                                        cell.flag = False

        if ai_on:  # AI play

            if first_move is True:
                board.add_mines(board.table[height // 2][width // 2])
                board.adjust_table()
                board.table[height // 2][width // 2].visible = True
                first_move = False

            for row in board.table:
                for cell in row:
                    if cell not in ai_visited_cells:
                        if cell.visible:

                            if cell.val != 0:
                                two_rule_ai(board, cell)

                            elif cell.val == 0:
                                board.open_game(cell)

                            check_adjacent_tiles = True
                            adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
                            for tile in adjacent_tiles:
                                if board.is_inside_table(adjacent_tiles[0][0], adjacent_tiles[0][1]):
                                    if not board.table[tile[1]][tile[0]].visible and not board.table[tile[1]][tile[0]].flag:
                                        check_adjacent_tiles = False

                            if check_adjacent_tiles:
                                ai_visited_cells.append(cell)

                        if cell.flag:

                            check_adjacent_tiles = True
                            adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
                            for tile in adjacent_tiles:
                                if board.is_inside_table(adjacent_tiles[0][0], adjacent_tiles[0][1]):
                                    if not board.table[tile[1]][tile[0]].visible and not board.table[tile[1]][tile[0]].flag:
                                        check_adjacent_tiles = False

                            if check_adjacent_tiles:
                                ai_visited_cells.append(cell)

            current_open_cell_count = 0
            current_flag_count = 0

            for row in board.table:
                for cell in row:
                    if cell.visible:
                        current_open_cell_count += 1
                    if cell.flag:
                        current_flag_count += 1

            if current_open_cell_count == open_cell_count and current_flag_count == flag_count:

                time.sleep(3)

                if current_flag_count == mines and len(ai_visited_cells) != width_of_board * height_of_board:
                    print("surrounded by mines")
                    for row in board.table:
                        for cell in row:
                            if not cell.visible and not cell.flag:
                                cell.visible = True

                mines_left = num_of_mines - current_flag_count
                unopened_cells = []
                unopened_neighbours = []

                for row in board.table:
                    for cell in row:
                        if cell not in ai_visited_cells:
                            if not cell.visible and not cell.flag:
                                adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
                                for tile in adjacent_tiles:
                                    if board.is_inside_table(tile[0], tile[1]):
                                        if board.table[tile[1]][tile[0]].visible:
                                            if cell not in unopened_cells:
                                                unopened_cells.append(cell)
                                            if board.table[tile[1]][tile[0]] not in unopened_neighbours:
                                                unopened_neighbours.append(board.table[tile[1]][tile[0]])

                unopened_groups = []
                unopened_neighbour_groups = []

                if len(unopened_cells) < 15:
                    unopened_groups = [unopened_cells]
                    unopened_neighbour_groups = [unopened_neighbours]

                else:
                    current_group = []
                    while len(unopened_cells) != 0:
                        current_group.append(unopened_cells[0])
                        unopened_cells.remove(unopened_cells[0])
                        if len(current_group) == 15:
                            unopened_groups.append(current_group)
                            current_group = []

                    unopened_groups.append(current_group)

                for group in unopened_groups:
                    current_neighbour_group = []
                    for cell in group:
                        adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
                        for tile in adjacent_tiles:
                            if board.is_inside_table(tile[0], tile[1]):
                                if board.table[tile[1]][tile[0]].visible:
                                    if board.table[tile[1]][tile[0]] not in current_neighbour_group:
                                        current_neighbour_group.append(board.table[tile[1]][tile[0]])
                    unopened_neighbour_groups.append(current_neighbour_group)

                """
                # Second way of separating
                
                unopened_neighbour_groups = []

                while len(unopened_neighbours) != 0:
                    current_neighbour_group = [unopened_neighbours[0]]
                    current_cell = None

                    while len(current_neighbour_group) < 15 and current_cell != current_neighbour_group[-1]:
                        current_cell = current_neighbour_group[-1]
                        adjacent_tiles = get_adjacent_tiles(current_neighbour_group[-1].x, current_neighbour_group[-1].y)
                        for tile in adjacent_tiles:
                            if board.is_inside_table(tile[0], tile[1]):
                                if board.table[tile[1]][tile[0]] in unopened_neighbours:
                                    current_neighbour_group.append(board.table[tile[1]][tile[0]])

                    unopened_neighbour_groups.append(current_neighbour_group)
                    for cell in unopened_neighbours:
                        if cell in unopened_neighbour_groups[-1]:
                            unopened_neighbours.remove(cell)

                unopened_groups = []

                for group in unopened_neighbour_groups:
                    current_group = []
                    for cell in group:
                        adjacent_tiles = get_adjacent_tiles(cell.x, cell.y)
                        for tile in adjacent_tiles:
                            if board.is_inside_table(tile[0], tile[1]):
                                if board.table[tile[1]][tile[0]] in unopened_cells:
                                    if board.table[tile[1]][tile[0]] not in current_group:
                                        current_group.append(board.table[tile[1]][tile[0]])
                    unopened_groups.append(current_group)
                """

                for i in range(len(unopened_groups)):
                    print(len(unopened_groups[i]))
                    print(len(unopened_neighbour_groups[i]))

                for i, group in enumerate(unopened_groups):
                    optimal_choice_ai(board, group, unopened_neighbour_groups[i], mines_left)
                    for row in board.table:
                        for cell in row:
                            if cell.visible and cell.val == 9:
                                print("Game over!")
                                print("Press 'r' to try again or close the window to exit!")
                                exit_game = True

        for row in board.table:  # Displays board
            for cell in row:

                if board.scale is 20:

                    if cell.visible:
                        screen.blit(numbers[cell.val], (cell.width, cell.height))

                    elif cell.flag:
                        screen.blit(flag, (cell.width, cell.height))

                    elif not cell.flag and not cell.visible:
                        screen.blit(grey, (cell.width, cell.height))

                else:

                    if cell.visible:
                        screen.blit(numbers[cell.val], (cell.width, cell.height))

                    if cell.flag:
                        screen.blit(flag, (cell.width, cell.height))

                    if not cell.flag and not cell.visible:
                        screen.blit(grey, (cell.width, cell.height))

    for row in board.table:  # Displays final board
        for cell in row:
            if cell.val == 9:
                screen.blit(bomb, (cell.width, cell.height))
            if cell.flag:
                screen.blit(flag, (cell.width, cell.height))
    pygame.display.update()

    exit_game = False
    while not exit_game:  # Waiting screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    exit_game = True
                    restart(width, height, mines)


########################################################################################################################
grey = pygame.image.load("grey.png")

bomb = pygame.image.load("bomb.png")
flag = pygame.image.load("flag.png")
emtpy = pygame.image.load("white.png")

one = pygame.image.load("1.png")
two = pygame.image.load("2.png")
three = pygame.image.load("3.png")
four = pygame.image.load("4.png")
five = pygame.image.load("5.png")
six = pygame.image.load("6.png")
seven = pygame.image.load("7.png")
eight = pygame.image.load("8.png")

numbers = [emtpy, one, two, three, four, five, six, seven, eight, bomb]
########################################################################################################################

if __name__ == "__main__":  # Main initialize
    print("Welcome to 'Danish Minesweeper' by Peter Hinge.")
    width_of_board = int(input("Please put in how wide you want the board to be: "))
    height_of_board = int(input("Please put in how high you want the board to be: "))
    num_of_mines = (width_of_board * height_of_board) // 7
    game(width_of_board, height_of_board, num_of_mines)
