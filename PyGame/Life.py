import pygame
from copy import deepcopy


class Board:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.left_border, self.top_border = 10, 10
        self.cell_size = 15
        self.board = [[0] * self.width for _ in range(self.height)]

    def on_click(self, cell):
        self.board[cell[0]][cell[1]] = (self.board[cell[0]][cell[1]] + 1) % 2

    def drawing(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, (25, 25, 25),
                                 (x * self.cell_size + self.left_border, y * self.cell_size + self.top_border,
                                  self.cell_size, self.cell_size), 1)
                if self.board[x][y] == 1:
                    pygame.draw.rect(screen, pygame.Color("green"),
                                     (x * self.cell_size + self.left_border, y * self.cell_size + self.top_border,
                                      self.cell_size, self.cell_size))

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left_border) // self.cell_size
        cell_y = (mouse_pos[1] - self.top_border) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def check_neighbours(self, board, cell):
        counter = 0
        if board[(cell[0] + 1) % self.height][cell[1]] == 1:
            counter += 1
        if board[(cell[0] + 1) % self.height][(cell[1] + 1) % self.width] == 1:
            counter += 1
        if board[(cell[0] + 1) % self.height][(cell[1] - 1) % self.width] == 1:
            counter += 1
        if board[cell[0] % self.height][(cell[1] - 1) % self.width] == 1:
            counter += 1
        if board[cell[0] % self.height][(cell[1] + 1) % self.width] == 1:
            counter += 1
        if board[(cell[0] - 1) % self.height][cell[1] % self.width] == 1:
            counter += 1
        if board[(cell[0] - 1) % self.height][(cell[1] + 1) % self.width] == 1:
            counter += 1
        if board[(cell[0] - 1) % self.height][(cell[1] - 1) % self.width] == 1:
            counter += 1
        return counter

    def next_move(self):
        board_copy = deepcopy(self.board)
        for y in range(self.height):
            for x in range(self.width):
                if self.check_neighbours(board_copy, (x, y)) == 3 and board_copy[x][y] == 0:
                    self.board[x][y] = 1
                elif self.check_neighbours(board_copy, (x, y)) < 2 or self.check_neighbours(
                        board_copy, (x, y)) > 3:
                    self.board[x][y] = 0


cells_size = 50
fps = 15
board = Board(cells_size, cells_size)
size = cells_size * board.cell_size + board.left_border * 2, \
       cells_size * board.cell_size + board.top_border * 2
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

running = True
game_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT and not game_started:
                board.get_click(event.pos)
            if event.button == pygame.BUTTON_WHEELUP:
                fps += 1
            if event.button == pygame.BUTTON_WHEELDOWN:
                fps -= 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_started = not game_started
    if game_started:
        clock.tick(fps)
        board.next_move()
    else:
        clock.tick(60)
    screen.fill((0, 0, 0))
    board.drawing()
    pygame.display.flip()

pygame.init()
pygame.quit()
