import sys
import pygame
import random
from pygame.locals import *

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Invaders")
ship = pygame.image.load('ship.png')
laser = pygame.image.load('green_laser.png')
invader_laser = pygame.image.load('red_laser.png')
score_font = pygame.font.SysFont('Consolas', 20, True)
title_font = pygame.font.SysFont('Consolas', 40, True)
win_font = pygame.font.SysFont('Consolas', 60, True)
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
    def __init__(self, x, y, img, velocity=-7):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.img = img

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        self.y += self.velocity


class Invader():
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
        if bullet.y < 0 or (bullet.y + bullet.img.get_height()) > 798:
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


def collision_check_shields(bullet_list, shields):
    for bullet in bullet_list:
        x = int(bullet.x + (bullet.img.get_width() / 2))
        y = int(bullet.y - 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y > 600:
                bullet_list.remove(bullet)
                update_shield(x, shields) 

def collision_shields_above(bullet_list, shields):
    for bullet in bullet_list:
        x = int(bullet.x + (bullet.img.get_width() / 2))
        y = int(bullet.y + bullet.img.get_height() + 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y < 650:
                bullet_list.remove(bullet)
                update_shield(x, shields)


def collision_player(player, bullet_list):
    for bullet in bullet_list:
        x = int(bullet.x + (bullet.img.get_width() / 2))
        y = int(bullet.y + bullet.img.get_height() + 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y > 650:
                bullet_list.remove(bullet)
                player.lives -= 1


def create_invaders(tens, twenties, thirties):
    y_space = 10
    x_space = (700 - invader3.get_width() * 11) / 10
    for i in range(11):
        x = int(25 + x_space * i + invader3.get_width() * i)
        y = 75
        thirties.append(Invader(x, y, invader3, 3))

    for i in range(2):
        for j in range(11):
            x_space = (700 - invader2.get_width() * 11) / 10
            y_space = 10
            x = int(25 + x_space * j + invader2.get_width() * j)
            y = int(116 + y_space * i + invader2.get_height() * i)
            twenties.append(Invader(x, y, invader2, 2))

    for i in range(2):
        for j in range(11):
            x_space = (700 - invader1.get_width() * 11) / 10
            y_space = 10
            x = int(25 + x_space * j + invader1.get_width() * j)
            y = int(188 + y_space * i + invader1.get_height() * i)
            tens.append(Invader(x, y, invader1, 1))


def udpate_invaders(x, y, invader_list, player):
    for j in range(len(invader_list)):
        invader = invader_list[j]
        if invader.x <= x <= (invader.x + invader.img.get_width()):
            if invader.y <= y <= (invader.y + invader.img.get_height()):
                invader_list.remove(invader)
                player.score += invader.value
                return

def collision_check_invaders(bullet_list, invaders, player):
    for bullet in bullet_list:
        x = int(bullet.x + (laser.get_width() / 2))
        y = int(bullet.y + 1)
        if screen.get_at((x, y))[:3] == (255, 255, 255):
            bullet_list.remove(bullet)
            udpate_invaders(x, y, invaders, player)


def draw_invaders(tens):
    for invader in tens:
        invader.draw()

def move_invaders(invaders, v):
    for invader in invaders:
        invader.x += v


def spawn_bullets(invaders_1, invaders_2, invaders_3, bullet_list, level):
    invader_lists = [invaders_1, invaders_2, invaders_3]
    for invaders in invader_lists:
        for invader in invaders:
            chance = random.randint(0, 4000)
            if chance <= 4 * level:
                bullet_list.append(Bullet(invader.x, invader.y, invader_laser, velocity = 7))


def check_win(tens, twenties, thirties):
    invader_lists = [tens, twenties, thirties]
    for invaders in invader_lists:
        if len(invaders) != 0:
            return False
    return True


def home():
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()


        prompt = title_font.render("Press space to begin...", True, (0, 255, 0))
        screen.blit(prompt, (400 - prompt.get_width() / 2, 400 - prompt.get_height()))
        pygame.display.flip()
        fpsClock.tick(fps)


def win(level):
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level += 1
                    game_loop()

        win = win_font.render("You Win!!!", True, (0, 255, 0))
        prompt = title_font.render("Begin level " + str(level) + "...", True, (0, 255, 0))
        screen.blit(prompt, (400 - prompt.get_width() / 2, 400 - prompt.get_height()))
        screen.blit(win, (400 - prompt.get_width() / 2, 200))
        pygame.display.flip()
        fpsClock.tick(fps)


def game_loop():
    player = Player(width / 2 - ship.get_width() / 2, height - ship.get_height())
    bullets = []
    invader_bullets = []
    ten_invaders = []
    twenty_invaders = []
    thirty_invaders = []
    shields = create_shields()
    count = 0
    velocity = 0.5
    level = 1
    create_invaders(ten_invaders, twenty_invaders, thirty_invaders)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.get_width(), player.y - 10, laser))

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
        collision_check_shields(bullets, shields)
        collision_shields_above(invader_bullets, shields)

        spawn_bullets(ten_invaders, twenty_invaders, thirty_invaders, invader_bullets, level)
        draw_bullets(invader_bullets)
        draw_bullets(bullets)
        collision_player(player, invader_bullets)

        move_invaders(ten_invaders, velocity)
        draw_invaders(ten_invaders)
        collision_check_invaders(bullets, ten_invaders, player)

        move_invaders(twenty_invaders, velocity)
        draw_invaders(twenty_invaders)
        collision_check_invaders(bullets, twenty_invaders, player)

        move_invaders(thirty_invaders, velocity)
        draw_invaders(thirty_invaders)
        collision_check_invaders(bullets, thirty_invaders, player)

        count += 1
        if count == 100:
            count = 0
            velocity = velocity * -1
        
        if player.lives == 0:
            home()

        if check_win(ten_invaders, twenty_invaders, thirty_invaders):
            level += 1
            win(level)
        pygame.display.flip()
        fpsClock.tick(fps)



def main():
    home()


if __name__ == '__main__':
    main()
