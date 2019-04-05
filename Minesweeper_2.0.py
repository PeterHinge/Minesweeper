import random

import pygame


pygame.init()
pygame.display.set_caption("Danish Minesweeper")


class Table:

    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.scale = 20
        self.table = self.setup()

    def __repr__(self):
        print(self.table)

    def setup(self):
        table = [[[] for i in range(self.width)] for i in range(self.height)]

        for x in range(0, len(table)):
            for y in range(0, len(table[x])):
                table[x][y] = Cell(x, y, self.scale)

        for i in range(self.mines):
            is_mine = False
            while not is_mine:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if table[x][y].val is not 9:
                    table[x][y].val = 9
                    is_mine = True

        for x in range(len(table)):
            for y in range(len(table[x])):
                if table[x][y].val == 9:
                    adjacent_tiles = get_adjacent_tiles(x, y)
                    for tile in adjacent_tiles:
                        if self.is_inside_table(tile[0], tile[1]):
                            if not is_bomb(table, tile[0], tile[1]):
                                table[tile[0]][tile[1]].val += 1

        return table

    def restart(self):  # Restarts game
        self.setup()

    def is_inside_table(self, x, y):  # Checks if cell is inside the game table
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def open_game(self, cell):  # Opens up the game if the clicked on tile has no adjacent mines
        cell.visible = True
        x, y = cell.x, cell.y
        adjacent_tiles = get_adjacent_tiles(x, y)
        for tile in adjacent_tiles:
            if self.table.is_inside_table(tile[0], tile[1]):
                if not self.table[tile[0]][tile[1]].visible and not self.table[tile[0]][tile[1]].flag:
                    table[tile[0]][tile[1]].visible = True
                    if self.table[tile[0]][tile[1]].val == 0:  # Recursive step that ensures all white spaces are opened
                        open_game(self.table, self.table[tile[0]][tile[1]])


class Cell:
    def __init__(self, x, y, scale):
        self.x = x * scale
        self.y = y * scale
        self.rect = pygame.rect.Rect(x, y, scale, scale)

        self.val = 0
        self.visible = False
        self.flag = False


def get_adjacent_tiles(x, y):  # Checks and return adjacent tiles
    neighbours = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    adjacent_tiles = []
    for coordinate in neighbours:
        adjacent_tiles.append([x + coordinate[0], y + coordinate[1]])
    return adjacent_tiles


def is_bomb(table, x, y):  # Checks if tile is a bomb
    return table[x][y] == 9


def game(width, height, mines):  # Main game

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

    board = Table(width, height, mines)  # Initializes board

    screen = pygame.display.set_mode((board.width, board.height))

    for x in range(0, board.width * board.scale, board.scale):  # Creates graphical cover of grey squares
        for y in range(0, board.height * board.scale, board.scale):
            screen.blit(grey, (x, y))

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
                    board.restart()

                elif event.key == pygame.K_c:  # Turn AI on/off event
                    if not ai_on:
                        ai_on = True
                    elif ai_on:
                        ai_on = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # Mouse-click event

                if event.button == 1:  # Left mouse-click event
                    for i in board.table:
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
                                        j.visible = board.table.open_game(j)
                                        j.visible = True

                elif event.button == 3:  # Right mouse-click event
                    for i in board.table:
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

        for i in board.table:  # Displays board
            for j in i:
                if j.visible:
                    screen.blit(numbers[j.val], (j.x, j.y))

                if j.flag:
                    screen.blit(flag, (j.x, j.y))

                if not j.flag and not j.visible:
                    screen.blit(grey, (j.x, j.y))

        open_square_count = 0
        for i in board.table:
            for j in i:
                if j.visible and j.val != 9:
                    open_square_count += 1

            if open_square_count == width * height - mines:  # Checks if all non-mine squares are open
                exit_game = True
                print("You Win!")
        pygame.display.update()

    for i in board.table:
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
    width_of_board = int(input("Please put in how wide you want the board to be: "))
    height_of_board = int(input("Please put in how high you want the board to be: "))
    num_of_mines = (width_of_board * height_of_board) // 7
    game(width_of_board, height_of_board, num_of_mines)
