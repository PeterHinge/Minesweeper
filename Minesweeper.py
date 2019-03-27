import random

import pygame


pygame.init()
pygame.display.set_caption("Danish Minesweeper")


def setup(n, mines):  # Sets up underlying game table
    table = generate_table(n)
    table = add_mines(table, mines)
    table = adjust_table(table)
    return table


def generate_table(n):  # Creates a table with the specified parameters
    return [[0] * n for i in range(n)]


def add_mines(table, mines):  # Add mines randomly to the table
    for i in range(mines):
        is_mine = False
        while not is_mine:
            x = random.randint(0, len(table) - 1)
            y = random.randint(0, len(table) - 1)
            if table[x][y] != 9:
                table[x][y] = 9
                is_mine = True
    return table


def adjust_table(table):  # Checks the surrounding cells clockwise and adjusts their respective values:
    for x in range(len(table)):
        for y in range(len(table[x])):
            if table[x][y] == 9:
                adjacent_tiles = get_adjacent_tiles(x, y)
                for tile in adjacent_tiles:
                    if is_inside_table(len(table), tile[0], tile[1]):
                        if not is_bomb(table, tile[0], tile[1]):
                            table[tile[0]][tile[1]] += 1

    return table


def get_adjacent_tiles(x, y):  # Checks and return adjacent tiles
    neighbours = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    adjacent_tiles = []
    for coordinate in neighbours:
        adjacent_tiles.append([x + coordinate[0], y + coordinate[1]])

    return adjacent_tiles


def is_inside_table(table_length, x, y):  # Checks if tile is inside the game table
    return 0 <= x <= table_length - 1 and 0 <= y <= table_length - 1


def is_bomb(table, x, y):  # Checks if tile is a bomb
    return table[x][y] == 9


class Board:
    def __init__(self, board):
        self.board = board

    def __repr__(self):
        print(self.board)


class Square:
    def __init__(self, x, y, w, h, board, ij):
        self.rect = pygame.rect.Rect(x, y, w, h)
        i, j = ij
        self.val = board[i][j]
        self.x = x
        self.y = y
        self.visible = False
        self.flag = False


def restart(size, mines):  # Restarts game
    game(size, mines)


def open_game(lst, square):  # Opens up the game if the clicked on tile has no adjacent mines
    square.visible = True
    x, y = square.x // 20, square.y // 20
    adjacent_tiles = get_adjacent_tiles(x, y)
    for tile in adjacent_tiles:
        if is_inside_table(size_of_board, tile[0], tile[1]):
            if not lst[tile[0]][tile[1]].visible and not lst[tile[0]][tile[1]].flag:
                lst[tile[0]][tile[1]].visible = True
                if lst[tile[0]][tile[1]].val == 0:  # Recursive step that ensures all whites spaces are opened
                    open_game(lst, lst[tile[0]][tile[1]])
    return lst


def ai_player(lst, square):  # Rule based AI
    x, y = square.x // 20, square.y // 20
    adjacent_tiles = get_adjacent_tiles(x, y)
    adjacent_mines = square.val
    adjacent_unopened_squares = 0
    for tile in adjacent_tiles:
        if is_inside_table(size_of_board, tile[0], tile[1]):
            if not lst[tile[0]][tile[1]].visible:
                adjacent_unopened_squares += 1
    if adjacent_mines == adjacent_unopened_squares:  # First Rule: Flag if unopened squares and adjacent mines are same
        for tile in adjacent_tiles:
            if is_inside_table(size_of_board, tile[0], tile[1]):
                if not lst[tile[0]][tile[1]].visible:
                    pygame.mouse.set_pos([tile[0] * 20 + 10, tile[1] * 20 + 10])
                    lst[tile[0]][tile[1]].flag = True
    adjacent_flags = 0
    for tile in adjacent_tiles:
        if is_inside_table(size_of_board, tile[0], tile[1]):
            if lst[tile[0]][tile[1]].flag:
                adjacent_flags += 1
    if adjacent_mines == adjacent_flags:  # Second Rule: Opens squares if adjacent flags and adjacent mines are same
        for tile in adjacent_tiles:
            if is_inside_table(size_of_board, tile[0], tile[1]):
                if not lst[tile[0]][tile[1]].visible and not lst[tile[0]][tile[1]].flag:
                    pygame.mouse.set_pos([tile[0] * 20 + 10, tile[1] * 20 + 10])
                    lst[tile[0]][tile[1]].visible = True
    return lst


def game(size, mines):  # Main game

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

    spil = Board(setup(size, mines))  # Initializes game
    w = h = len(spil.board) * 20

    screen = pygame.display.set_mode((w, h))

    lst = [[] for i in range(size)]

    for i in range(0, size * 20, 20):  # Creates graphical cover of grey squares
        for j in range(0, size * 20, 20):
            lst[i // 20] += [Square(i, j, 20, 20, spil.board, (i // 20, j // 20))]
            screen.blit(grey, (i, j))

    ai_on = False

    exit_game = False
    while not exit_game:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Quit game event
                exit_game = True
                pygame.quit()

            elif event.type == pygame.KEYDOWN:  # Keyboard pressed event

                if event.key == pygame.K_r:  # Restart game event
                    exit_game = True
                    restart(size, mines)

                elif event.key == pygame.K_c:  # Turn AI on/off event
                    if not ai_on:
                        ai_on = True
                    elif ai_on:
                        ai_on = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse-click event

                if event.button == 1:  # Left mouse-click event
                    for i in lst:
                        for j in i:
                            r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if j.rect.colliderect(r):
                                if not j.flag:
                                    if j.val == 9:
                                        print("Game over!")
                                        print("Press 'r' to try again or close the window to exit!")
                                        exit_game = True
                                    j.visible = True
                                    if j.val == 0:
                                        j.visible = open_game(lst, j)
                                        j.visible = True

                elif event.button == 3:  # Right mouse-click event
                    for i in lst:
                        for j in i:
                            r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                            if j.rect.colliderect(r):
                                if not j.visible:
                                    if not j.flag:
                                        j.flag = True
                                    elif j.flag:
                                        j.flag = False

        if ai_on:  # AI play
            start_board = lst
            end_board = lst
            for i in lst:
                for j in i:
                    if j.visible:
                        end_board = ai_player(lst, j)
            if start_board == end_board:
                start_board = end_board
                print(start_board)
                open_random = lst[random.randint(0, size_of_board - 1)][random.randint(0, size_of_board - 1)]
                if not open_random.visible and not open_random.flag:
                    open_random.visible = True
                    if open_random.val == 9:
                        print("Game over!")
                        print("Press 'r' to try again or close the window to exit!")
                        exit_game = True

        for i in lst:  # Displays board
            for j in i:
                if j.visible:
                    screen.blit(numbers[j.val], (j.x, j.y))

                if j.flag:
                    screen.blit(flag, (j.x, j.y))

                if not j.flag and not j.visible:
                    screen.blit(grey, (j.x, j.y))

        open_square_count = 0
        for i in lst:
            for j in i:
                if j.visible and j.val != 9:
                    open_square_count += 1

            if open_square_count == size * size - mines:  # Checks if all non-mine squares are open
                exit_game = True
                print("You Win!")
        pygame.display.update()

    for i in lst:
        for j in i:
            if j.val == 9:
                screen.blit(bomb, (j.x, j.y))
            if j.flag:
                screen.blit(flag, (j.x, j.y))
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
                    restart(size, mines)


if __name__ == "__main__":  # Main initialize
    print("Welcome to 'Danish Minesweeper' by Peter Hinge.")
    size_of_board = int(input("Please put in how big you want the board to be: "))
    num_of_mines = (size_of_board * size_of_board) // 7
    game(size_of_board, num_of_mines)
