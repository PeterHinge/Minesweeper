import random

import pygame

pygame.init()


def setup(n, mines):
    table = generate_table(n)
    table = add_mines(table, mines)
    table = adjust_table(table)
    return table


def generate_table(n):
    return [[0] * n for i in range(n)]


def add_mines(table, mines):
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
                    if is_inside_table(table, tile[0], tile[1]):
                        if not is_bomb(table, tile[0], tile[1]):
                            table[tile[0]][tile[1]] += 1

    return table


def get_adjacent_tiles(x, y):
    neighbour = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    adjacent_tiles = []
    for coordinate in neighbour:
        adjacent_tiles.append([x + coordinate[0], y + coordinate[1]])

    return adjacent_tiles


def is_inside_table(table, x, y):
    return 0 <= x <= len(table) - 1 and 0 <= y <= len(table) - 1


def is_bomb(table, x, y):
    return table[x][y] == 9


class Board:
    def __init__(self, board):
        self.board = board

    def __repr__(self):
        print(self.board)
        return "Statement"


class Square:
    def __init__(self, x, y, w, h, board, ij):
        self.rect = pygame.rect.Rect(x, y, w, h)
        i, j = ij
        self.val = board[i][j]
        self.x = x
        self.y = y
        self.visible = False
        self.flag = False


def restart(size, mines):
    game(size, mines)


def open_game(lst, square):
    square.visible = True
    x, y = square.x // 20, square.y // 20
    adjacent_tiles = get_adjacent_tiles(x, y)
    for tile in adjacent_tiles:
        if 0 <= tile[0] <= size_of_board - 1 and 0 <= tile[1] <= size_of_board - 1:
            if not lst[tile[0]][tile[1]].visible and not lst[tile[0]][tile[1]].flag:
                lst[tile[0]][tile[1]].visible = True
                if lst[tile[0]][tile[1]].val == 0:
                    open_game(lst, lst[tile[0]][tile[1]])
    return lst


def game(size, mines):

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

    spil = Board(setup(size, mines))
    w = h = len(spil.board) * 20

    screen = pygame.display.set_mode((w, h))

    lst = [[] for i in range(size)]

    for i in range(0, size * 20, 20):
        for j in range(0, size * 20, 20):
            lst[i // 20] += [Square(i, j, 20, 20, spil.board, (i // 20, j // 20))]
            screen.blit(grey, (i, j))

    exit_game = False
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    exit_game = True
                    restart(size, mines)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for i in lst:
                    for j in i:
                        r = pygame.rect.Rect(pygame.mouse.get_pos(), (1, 1))
                        if j.rect.colliderect(r):
                            if not j.visible:
                                if not j.flag:
                                    j.flag = True
                                elif j.flag:
                                    j.flag = False

        for i in lst:
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

            if open_square_count == size * size - mines:
                exit_game = True
                print("You Win!")
        pygame.display.update()

    for i in lst:
        for j in i:
            if j.val == 9:
                screen.blit(bomb, (j.x, j.y))
    pygame.display.update()

    exit_game = False
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    exit_game = True
                    restart(size, mines)


if __name__ == "__main__":
    print("Welcome to 'Danish Minesweeper' by Peter Hinge.")
    size_of_board = int(input("Please put in how big you want the board to be: "))
    num_of_mines = (size_of_board * size_of_board) // 7
    game(size_of_board, num_of_mines)
