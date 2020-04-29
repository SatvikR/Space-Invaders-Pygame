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
invader1 = pygame.image.load('invader1.png')
invader2 = pygame.image.load('invader2.png')
invader3 = pygame.image.load('invader3.png')


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
    def __init__(self, x, y, velocity=-7):
        self.x = x
        self.y = y
        self.velocity = velocity

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

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


class Shield():
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = 21

    def draw(self):
        screen.blit(shield_img, (self.x, self.y))

    def draw_health(self):
        width = shield_img.get_width() * self.health / 21
        r = min(255, 255 - (255 * ((self.health - (21 - self.health)) / 21)))
        g = min(255, 255 * (self.health / (21 / 2)))
        color = (r, g, 0)
        pygame.draw.rect(screen, color, (self.x, self.y - 10, width, 7), 0)


def update_shield(x, shield_list):
    for shield in shield_list:
        if shield.x <= x <= shield.x + shield_img.get_width():
            shield.health -= 1


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
            shield.draw()
            shield.draw_health()


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


def collision_check(bullet_list, shields):
    for bullet in bullet_list:
        x = int(bullet.x + (laser.get_width() / 2))
        y = int(bullet.y + 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y > 600:
                bullet_list.remove(bullet)
                update_shield(x, shields) 


def create_invaders(tens):
    for i in range(2):
        for j in range(11):
            x_space = (700 - invader1.get_width() * 11) / 10
            y_space = 7
            x = int(50 + x_space * j + invader1.get_width() * j)
            y = int(75 + y_space * i + invader1.get_height() * i)
            tens.append(Invader(x, y, invader1, 1))


def draw_invaders(tens):
    for invader in tens:
        invader.draw()


def game_loop():
    player = Player(width / 2 - ship.get_width() / 2, height - ship.get_height())
    bullets = []
    ten_invaders = []
    twenty_invaders = []
    thirty_invaders = []
    shields = create_shields()
    create_invaders(ten_invaders)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.get_width(), player.y - 10))

        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            if player.x + ship.get_width() < width:
                player.x += player.velocity
        elif key[pygame.K_LEFT]:
            if player.x > 0:
                player.x -= player.velocity

        screen.fill((0, 0, 0))
        score = score_font.render("Score: " + str(player.score), True, (0, 255, 0))
        screen.blit(score, (0, 15))
        player.draw_lives()

        player.draw()
        draw_sheilds(shields)
        collision_check(bullets, shields)
        draw_bullets(bullets)

        draw_invaders(ten_invaders)

        pygame.display.flip()
        fpsClock.tick(fps)


def main():
    game_loop()


if __name__ == '__main__':
    main()
