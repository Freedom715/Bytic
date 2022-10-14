from random import randint

import pygame

SIZE = WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()
CELL_SIZE = 25
SNAKE_SPEED = 10


class SnakeBody:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.head = True
        self.color = (0, 100, 0)
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))


def game_loop():
    x1, x1_change = WIDTH // 2 // CELL_SIZE * CELL_SIZE, 0
    y1, y1_change = HEIGHT // 2 // CELL_SIZE * CELL_SIZE, 0
    snake_list = []
    snake_len = 1
    food_x = randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    food_y = randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and x1 % CELL_SIZE == 0:
                if event.key == pygame.K_UP:
                    x1_change, y1_change = 0, -CELL_SIZE
                elif event.key == pygame.K_RIGHT:
                    x1_change, y1_change = CELL_SIZE, 0
                elif event.key == pygame.K_DOWN:
                    x1_change, y1_change = 0, CELL_SIZE
                elif event.key == pygame.K_LEFT:
                    x1_change, y1_change = -CELL_SIZE, 0
        x1 += x1_change
        y1 += y1_change
        if x1 >= WIDTH:
            x1 = 0
        elif x1 < 0:
            x1 = WIDTH
        if y1 >= HEIGHT:
            y1 = 0
        elif y1 < 0:
            y1 = HEIGHT
        SCREEN.fill((0, 150, 0))
        pygame.draw.rect(SCREEN, (190, 0, 0), [food_x, food_y, CELL_SIZE, CELL_SIZE])
        snake_list.append(SnakeBody(x1, y1))
        if len(snake_list) > snake_len:
            del snake_list[0]
        for elem in snake_list:
            elem.draw()
        if x1 == food_x and y1 == food_y:
            food_x = randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            food_y = randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            snake_len += 1
        pygame.display.update()
        CLOCK.tick(SNAKE_SPEED)


pygame.init()
game_loop()
