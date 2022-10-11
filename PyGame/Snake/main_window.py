import pygame

pygame.init()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
CELL_SIZE = 25


def game_loop():
    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        screen.fill((0, 150, 0))
        pygame.display.update()
        clock.tick(10)



game_loop()
