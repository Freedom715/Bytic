import os
import sys
from itertools import product
from random import randint

import pygame


def load_image(name, colorkey=None):
    """
    Function for loading pictures from Images folders
    :param name: name of image which need to load
    :param colorkey: background color
    :return: loaded image
    """
    image = pygame.image.load(name).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Main:
    def __init__(self):
        self.size = self.WIDTH, self.HEIGHT = 850, 700
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.game_fon = pygame.transform.scale(pygame.image.load('game_fon.png').convert(), (self.WIDTH, self.HEIGHT))
        self.menu_fon = pygame.transform.scale(pygame.image.load('menu_fon.jpg').convert(), (self.WIDTH, self.HEIGHT))
        self.all_sprites = pygame.sprite.Group()
        self.enemy_group, self.player_sprite = pygame.sprite.Group(), pygame.sprite.Group()
        self.bullets, self.buttons = pygame.sprite.Group(), pygame.sprite.Group()
        self.cell_size, self.player_size_x, self.player_size_y = 50, 50, 50
        self.row, self.col = 1, 11
        self.player = Hero((self.WIDTH // 2) - 50, 11 * self.cell_size, self)
        self.running = True
        self.game_running, self.menu_running = None, None
        self.enemies = []
        self.enemies_counter = 0
        self.mouse_pos = (0, 0)
        self.menu_cycle()

    def menu_cycle(self, menu=True):
        self.menu_running = True
        self.game_running = False
        while self.running and self.menu_running:
            self.screen.blit(self.menu_fon, (0, 0))
            if menu:
                for button in self.buttons.sprites():
                    self.buttons.remove(button)
                Button(200, 300, self, "Buttons/start_black.png", "Buttons/start_red.png", self.game_cycle)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for elem in self.buttons:
                        elem.check_click(event.pos)
            for button in self.buttons:
                button.check_mouse_pos(self.mouse_pos)
            self.buttons.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

    def game_cycle(self):
        counter = 0
        self.menu_running = False
        self.game_running = True
        self.enemy_group.remove(self.enemy_group.sprites())
        for j in range(self.row):
            self.enemies.append([Enemy(50 * i + 50 + 50 * (j % 2), j * 50 + 25, self) for i in range(0, self.col, 2)])
        while self.running and self.game_running:
            self.screen.blit(self.game_fon, (0, 0))
            self.all_sprites.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()

            for indx in range(self.row - 1, -1, -1):
                if self.enemies[indx][0].check_collision() or self.enemies[indx][-1].check_collision():
                    for elem in self.enemies[indx]:
                        elem.check_collision()
                        elem.move(y=True)
                else:
                    for elem in self.enemies[indx]:
                        elem.check_collision()
                        elem.move()

            for elem in self.bullets:
                elem.move()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-1)
            elif keys[pygame.K_RIGHT]:
                self.player.move(1)
            elif keys[pygame.K_UP]:
                if counter >= FPS:
                    self.bullets.add(Bullet(self.player.x + 35, self.player.y, self))
                    counter = 0
            if self.enemies_counter == 0:
                self.__init__()
            counter += 2
            pygame.display.flip()
            self.clock.tick(FPS)


class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y, main):
        super().__init__(main.player_sprite, main.all_sprites)
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, x + 100, y + 25)
        self.image = pygame.transform.scale(load_image('hero.png', -1), (100, 25))
        self.main = main

    def move(self, direction):
        if 0 <= self.x + direction * 25 <= self.main.WIDTH - 100:
            self.x += direction * 25
            self.rect.x, self.rect.y = self.x, self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, main):
        super().__init__(main.enemy_group, main.all_sprites)
        self.x, self.y = x, y
        self.main = main
        self.main.enemies_counter += 1
        self.image = pygame.transform.scale(load_image('enemy.jpg', -1), (50, 50))
        rct = pygame.Rect(x, y, 50, 50)
        self.rect = rct
        self.counter = 0
        self.hp = 10
        self.direction = 1

    def check_collision(self):
        if 0 < self.x + self.direction * 25 < self.main.WIDTH - 50:
            return False
        if pygame.sprite.spritecollideany(self, self.main.bullets):
            print("Ouch!")
        return True

    def upd_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self, y=False):
        if self.counter >= FPS:
            if y:
                self.y += 25
                self.direction *= -1
                if self.y + 75 >= 600:
                    self.main.__init__()
            self.x += 25 * self.direction
            self.upd_rect()
            self.counter = 0
        self.counter += 5


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, main):
        super().__init__(main.bullets, main.all_sprites)
        self.x, self.y = x, y
        self.main = main
        self.image = pygame.Surface((25, 25))
        self.counter = 0
        self.image.fill((0, 255, 0))
        rct = pygame.Rect(x, y, 25, 25)
        self.rect = rct

    def upd_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        if self.counter >= FPS:
            self.y -= 5
            self.counter = 0
            self.upd_rect()
        if pygame.sprite.spritecollideany(self, self.main.enemy_group):
            pygame.sprite.spritecollide(self, self.main.enemy_group, True)
            self.kill()
            self.main.enemies_counter -= 1
        self.counter += 15


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, main, image, selected_image, clicked_func):
        super().__init__(main.buttons)
        self.x, self.y = x, y
        self.main = main
        self.not_selected_image = pygame.transform.scale(load_image(image, -1), (300, 100))
        self.selected_image = pygame.transform.scale(load_image(selected_image, -1), (300, 100))
        self.image = self.not_selected_image
        self.rect = self.image.get_rect().move(x, y)
        self.clicked_func = clicked_func
        self.selected = False
        if self.selected:
            self.image = self.selected_image
        else:
            self.image = self.not_selected_image

    def check_mouse_pos(self, pos):
        if self.rect.collidepoint(pos):
            self.image = self.selected_image
            self.selected = True
        else:
            self.image = self.not_selected_image
            self.selected = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            if self.clicked_func():
                return True


FPS = 60
pygame.init()

app = Main()

pygame.quit()
