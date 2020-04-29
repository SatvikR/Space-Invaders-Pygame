import sys
import pygame
from pygame.locals import *

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
ship = pygame.image.load('ship.png')
laser = pygame.image.load('green_laser.png')
score_font = pygame.font.SysFont('Consolas', 20, True)
shield_img = pygame.image.load('shield.png')


class Player():
    velocity = 3
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.lives = 3

    def get_width(self):
        return self.x + (ship.get_width() / 2) - 5

    def draw(self):
        screen.blit(ship, (self.x, self.y))

    def draw_lives(self):
        text = score_font.render("Lives:", True, (0, 255, 0))
        screen.blit(text, (570, 15))
        for i in range(self.lives):
            screen.blit(ship, (570 + text.get_width() + i * 55, 0))


class Bullet():
    velocity = -5
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(laser, (self.x, self.y))

    def update(self):
        self.y += self.velocity


class Invader():
    velocity = 2
    def __init__(self, x, y, img, level):
        self.x = x
        self.y = y
        self.img = img
        self.level = level
        self.value = level * 10


class Shield():
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health



def draw_bullets(bullet_list):
    for bullet in bullet_list:
        bullet.update()
        if bullet.y < 0:
            bullet_list.remove(bullet)
        else:
            bullet.draw()


def draw_sheilds(shield_list):
    for i, shield in enumerate(shield_list):
        if shield.health != 0:
            screen.blit(shield_img, (shield.x, shield.y))


def create_shields():
    shield_list = []
    h = 600
    for i in range(3):
        if i == 0:
            shield_list.append(Shield(158, h, 21))
        elif i == 1:
            shield_list.append(Shield(372, h, 21))
        elif i == 2:
            shield_list.append(Shield(586, h, 21))
    return shield_list



def game_loop():
    player = Player(width / 2 - ship.get_width() / 2, height - ship.get_height())
    bullets = []
    shields = create_shields()
    print(screen.get_at((165, 602))[:3])
    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.get_width(), player.y))


        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.x -= player.velocity
        elif key[pygame.K_RIGHT]:
            player.x += player.velocity

        player.draw()
        draw_sheilds(shields)
        pos = pygame.mouse.get_pos()
        color = score_font.render(str(screen.get_at(pos)[:3]), True, (0, 255, 0))
        screen.blit(color, (300, 0))
        score = score_font.render("Score: " + str(player.score), True, (0, 255, 0))
        player.draw_lives()
        screen.blit(score, (0, 15))
        draw_bullets(bullets)
        pygame.display.flip()
        fpsClock.tick(fps)


def main():
    game_loop()

if __name__ == '__main__':
    main()