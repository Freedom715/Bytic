import sys

import pygame
import random

pygame.init()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
snake_block = 25
snake_speed = 5
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


class SnakeBody:
    def __init__(self, x, y, head=False):
        self.x = x
        self.y = y
        self.head = head
        if head:
            self.image = pygame.transform.scale(pygame.image.load('head0.jpg').convert(), (snake_block, snake_block))
        else:
            self.image = pygame.transform.scale(pygame.image.load('body0.jpg').convert(), (snake_block, snake_block))

    def move(self):
        screen.blit(self.image, (self.x, self.y))

    def check_direction(self, direction):
        if self.head:
            self.image = pygame.transform.scale(pygame.image.load(f'head{direction}.jpg').convert(), (snake_block, snake_block))
        else:
            self.image = pygame.transform.scale(pygame.image.load(f'body{direction}.jpg').convert(), (snake_block, snake_block))



def your_score(score):
    value = score_font.render("Ваш счёт: " + str(score), True, (255, 255, 0))
    screen.blit(value, [0, 0])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH // 6, HEIGHT // 3])


def game_loop():
    game_over, game_close = False, False
    x1, x1_change = WIDTH // 2, 0
    y1, y1_change = HEIGHT // 2, 0
    snake_list = []
    snake_len = 1
    food_x = random.randint(0, (WIDTH - snake_block) // snake_block) * snake_block
    food_y = random.randint(0, (HEIGHT - snake_block) // snake_block) * snake_block
    direction = 0
    while not game_over:
        while game_close:
            screen.fill((0, 0, 255))
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", (255, 0, 0))
            your_score(snake_len - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and x1 % snake_block == 0:
                if event.key == pygame.K_UP:
                    x1_change, y1_change = 0, -snake_block
                    direction = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change, y1_change = snake_block, 0
                    direction = 1
                elif event.key == pygame.K_LEFT:
                    x1_change, y1_change = -snake_block, 0
                    direction = 2
                elif event.key == pygame.K_DOWN:
                    x1_change, y1_change = 0, snake_block
                    direction = 3
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        screen.fill((0, 0, 255))
        pygame.draw.rect(screen, (0, 255, 0), [food_x, food_y, snake_block, snake_block])
        snake_list.append(SnakeBody(x1, y1, head=True))
        if len(snake_list) > snake_len:
            del snake_list[0]
        for x in snake_list[:-1]:
            x.head = False
            if (x.x, x.y) == (snake_list[-1].x, snake_list[-1].y):
                game_close = True
        snake_list[-1].check_direction(direction)
        if len(snake_list) > 1:
            snake_list[-2].check_direction(direction)
        for elem in snake_list:
            elem.move()
            print(elem.head)
        your_score(snake_len - 1)
        pygame.display.update()
        if x1 == food_x and y1 == food_y:
            food_x = random.randint(0, (WIDTH - snake_block) // snake_block) * snake_block
            food_y = random.randint(0, (HEIGHT - snake_block) // snake_block) * snake_block
            snake_len += 1
        clock.tick(snake_speed)


game_loop()
