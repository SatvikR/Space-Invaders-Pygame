import sys
import pygame
import random
from pygame.locals import *

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
logo = pygame.image.load('./images/graphics-space-invaders-logo.jpg')
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(logo)
ship = pygame.image.load('./images/ship.png')
laser = pygame.image.load('./images/green_laser.png')
invader_laser = pygame.image.load('./images/red_laser.png')
score_font = pygame.font.Font('./fonts/bitfont.ttf', 40)
ctrl_font = pygame.font.Font('./fonts/bitfont.ttf', 27)
title_font = pygame.font.Font('./fonts/bitfont.ttf', 40)
win_font = pygame.font.Font('./fonts/bitfont.ttf', 60)
shield_img = pygame.image.load('./images/shield.png')
invader1 = pygame.image.load('./images/invader1.png')
invader2 = pygame.image.load('./images/invader2.png')
invader3 = pygame.image.load('./images/invader3.png')
invader_dead = pygame.image.load('./images/invaderkilled.gif')
dead_player = pygame.image.load('./images/explosion.gif')
shoot = pygame.mixer.Sound('./sounds/shoot.wav')
invader_kill = pygame.mixer.Sound('./sounds/invaderkilled.wav')
player_kill = pygame.mixer.Sound('./sounds/explosion.wav')
pygame.mixer.music.load('./sounds/spaceinvaders1.mpeg')
pygame.mixer.music.play(-1)
level = 1


class Player():
    velocity = 3

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.score = 0
        self.lives = 3
        self.is_dead = False
        self.time_dead = 0
        self.img = ship

    def get_width(self) -> int:
        return self.x + (ship.get_width() / 2) - 5

    def draw(self) -> None:
        screen.blit(self.img, (self.x, self.y))

    def draw_lives(self) -> None:
        text = score_font.render("Lives:", True, (0, 255, 0))
        screen.blit(text, (530, 7))
        for i in range(self.lives):
            screen.blit(ship, (530 + text.get_width() + i * 55, 0))


class Bullet():
    def __init__(self, x: int, y: int, img: pygame.Surface, velocity=-7):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.img = img

    def draw(self) -> None:
        screen.blit(self.img, (self.x, self.y))

    def update(self) -> None:
        self.y += self.velocity


class Invader():
    def __init__(self, x: int, y: int, img: pygame.Surface, level: int):
        self.x = x
        self.y = y
        self.img = img
        self.level = level
        self.value = level * 10
        self.is_dead = False
        self.time_dead = 0

    def draw(self) -> None:
        screen.blit(self.img, (self.x, self.y))


class Shield():
    def __init__(self, x: int, y: int, health: int):
        self.x = x
        self.y = y
        self.health = 21

    def draw(self) -> None:
        screen.blit(shield_img, (self.x, self.y))

    def draw_health(self) -> None:
        width = shield_img.get_width() * self.health / 21
        r = min(255, 255 - (255 * ((self.health - (21 - self.health)) / 21)))
        g = min(255, 255 * (self.health / (21 / 2))) # I plagerized these two lines don't sue me
        color = (r, g, 0)
        pygame.draw.rect(screen, color, (self.x, self.y - 10, width, 7), 0)


def update_shield(x: int, shield_list: list) -> None:
    for shield in shield_list:
        if shield.x <= x <= shield.x + shield_img.get_width():
            shield.health -= 1


def draw_bullets(bullet_list: list) -> None:
    for bullet in bullet_list:
        bullet.update()
        if bullet.y < 0 or (bullet.y + bullet.img.get_height()) > 798:
            bullet_list.remove(bullet)
        else:
            bullet.draw()


def draw_sheilds(shield_list: list) -> None:
    for shield in shield_list:
        if shield.health != 0:
            shield.draw()
            shield.draw_health()


def create_shields() -> list:
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


def collision_check_shields(bullet_list: list, shields: list) -> None:
    for bullet in bullet_list:
        x = int(bullet.x + (bullet.img.get_width() / 2))
        y = int(bullet.y - 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y > 600:
                bullet_list.remove(bullet)
                update_shield(x, shields)

def collision_shields_above(bullet_list: list, shields: list) -> None:
    for bullet in bullet_list:
        x = int(bullet.x + (bullet.img.get_width() / 2))
        y = int(bullet.y + bullet.img.get_height() + 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y < 650:
                bullet_list.remove(bullet)
                update_shield(x, shields)


def collision_player(player: Player, bullet_list: list) -> None:
    for bullet in bullet_list:
        x = int(bullet.x + (bullet.img.get_width() / 2))
        y = int(bullet.y + bullet.img.get_height() + 1)
        if screen.get_at((x, y))[:3] == (28, 255, 28):
            if y > 650:
                bullet_list.remove(bullet)
                player.is_dead = True
                player.img = dead_player
                pygame.mixer.Sound.play(player_kill)
                player.lives -= 1


def update_player(player: Player) -> None:
    if player.is_dead == True:
        player.time_dead += 1
        if player.time_dead == 60:
            player.img = ship
            player.time_dead = 0
            player.is_dead = False


def create_invaders(tens: list, twenties: list, thirties: list) -> None:
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


def udpate_invaders(x: int, y: int, invader_list: list, player: Player) -> None:
    for j in range(len(invader_list)):
        invader = invader_list[j]
        if invader.x <= x <= (invader.x + invader.img.get_width()):
            if invader.y <= y <= (invader.y + invader.img.get_height()):
                if not invader.is_dead:
                    invader.is_dead = True
                    invader.img = invader_dead
                    pygame.mixer.Sound.play(invader_kill)
                    player.score += invader.value
                    return

def collision_check_invaders(bullet_list: list, invaders: list, player: Player) -> None:
    for bullet in bullet_list:
        x = int(bullet.x + (laser.get_width() / 2))
        y = int(bullet.y + 1)
        if screen.get_at((x, y))[:3] == (255, 255, 255):
            bullet_list.remove(bullet)
            udpate_invaders(x, y, invaders, player)


def draw_invaders(tens: list) -> None:
    for invader in tens:
        invader.draw()

def move_invaders(invaders: list, v: int) -> None:
    for invader in invaders:
        invader.x += v


def update_all_invaders(tens: list, twenties: list, thirties: list) -> None:
    invader_lists = [tens, twenties, thirties]
    for invaders in invader_lists:
        for invader in invaders:
            if invader.is_dead:
                invader.time_dead += 1
                if invader.time_dead == 60:
                    invaders.remove(invader)



def spawn_bullets(invaders_1: list, invaders_2: list, invaders_3: list, bullet_list: list, level: int) -> None:
    invader_lists = [invaders_1, invaders_2, invaders_3]
    for invaders in invader_lists:
        for invader in invaders:
            chance = random.randint(0, 4000)
            if chance <= 4 * level:
                bullet_list.append(Bullet(invader.x, invader.y, invader_laser, velocity = 7))


def check_win(tens: list, twenties: list, thirties: list) -> bool:
    invader_lists = [tens, twenties, thirties]
    for invaders in invader_lists:
        if len(invaders) != 0:
            return False
    return True


def home() -> None:
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                if event.key == pygame.K_h:
                    how_to_play()


        prompt = title_font.render("Press space to begin...", True, (0, 255, 0))
        how = score_font.render("Press H to see how to play", True, (0, 255, 0))
        screen.blit(prompt, (400 - prompt.get_width() / 2, 400 - prompt.get_height()))
        screen.blit(how, (400 - how.get_width() / 2, 600))
        pygame.display.flip()
        fpsClock.tick(fps)


def win(level: int) -> None:
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
        prompt = title_font.render("Press space to begin level " + str(level) + "...", True, (0, 255, 0))
        screen.blit(prompt, (400 - prompt.get_width() / 2, 400 - prompt.get_height()))
        screen.blit(win, (400 - prompt.get_width() / 2, 200))
        pygame.display.flip()
        fpsClock.tick(fps)


def how_to_play() -> None:
    screen.fill((0, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    home()
        title = title_font.render("How to play:", True, (0, 255, 0))
        prompt = ctrl_font.render("Click to shoot, A and D to move left to right", True, (0, 255, 0))
        prompt_2 = ctrl_font.render("The invaders will shoot red lasers at you, and it is your job", True, (0, 255, 0))
        prompt_3 = ctrl_font.render("to shoot all of them before you loose your lives. Once you kill", True, (0, 255, 0))
        prompt_4 = ctrl_font.render("all the aliens, you will advance to the next level. Each level", True, (0, 255, 0))
        prompt_5 = ctrl_font.render("gets is exponentially harder than the previous. Use your shields to", True, (0, 255, 0))
        prompt_6 = ctrl_font.render("dodge bullets. Press escape to pause.", True, (0, 255, 0))
        back = score_font.render("Press space to go back to menu", True, (0, 255, 0))
        screen.blit(title, (400 - title.get_width() / 2, 200))
        screen.blit(prompt, (400 - prompt.get_width() / 2, 400))
        screen.blit(prompt_2, (400 - prompt_2.get_width() / 2, 450))
        screen.blit(prompt_3, (400 - prompt_3.get_width() / 2, 500))
        screen.blit(prompt_4, (400 - prompt_4.get_width() / 2, 550))
        screen.blit(prompt_5, (400 - prompt_5.get_width() / 2, 600))
        screen.blit(prompt_6, (400 - prompt_6.get_width() / 2, 650))
        screen.blit(back, (400 - back.get_width() / 2, 700))
        pygame.display.flip()
        fpsClock.tick(fps)


def death() -> None:
    global level
    level = 0
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

        win = win_font.render("You Died!", True, (0, 255, 0))
        prompt = title_font.render("Press space to try again...", True, (0, 255, 0))
        screen.blit(prompt, (400 - prompt.get_width() / 2, 400 - prompt.get_height()))
        screen.blit(win, (400 - win.get_width() / 2, 200))
        pygame.display.flip()
        fpsClock.tick(fps)


def game_loop() -> None:
    global level
    player = Player(width / 2 - ship.get_width() / 2, height - ship.get_height())
    bullets = []
    invader_bullets = []
    ten_invaders = []
    twenty_invaders = []
    thirty_invaders = []
    shields = create_shields()
    count = 0
    velocity = 0.5
    pause = False

    create_invaders(ten_invaders, twenty_invaders, thirty_invaders)
    while True:
        if pause:
            screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = False

            message = score_font.render("Press space to resume", True, (0, 255, 0))
            screen.blit(message, (400 - message.get_width() / 2, 400 - message.get_height() / 2))
            pygame.display.flip()
            fpsClock.tick(fps)
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not player.is_dead:
                        pygame.mixer.Sound.play(shoot)
                        bullets.append(Bullet(player.get_width(), player.y - 10, laser))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = True
            key = pygame.key.get_pressed()
            if key[pygame.K_d]:
                if not player.is_dead:
                    if player.x + ship.get_width() < width:
                        player.x += player.velocity
            elif key[pygame.K_a]:
                if not player.is_dead:
                    if player.x > 0:
                        player.x -= player.velocity

            screen.fill((0, 0, 0))
            score = score_font.render("Score: " + str(player.score), True, (0, 255, 0))
            screen.blit(score, (0, 15))
            player.draw_lives()

            player.draw()
            update_player(player)
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
            update_all_invaders(ten_invaders, twenty_invaders, thirty_invaders)

            count += 1
            if count == 100:
                count = 0
                velocity = velocity * -1

            if player.lives == 0:
                death()

            if check_win(ten_invaders, twenty_invaders, thirty_invaders):
                level += 1
                win(level)
            pygame.display.flip()
            fpsClock.tick(fps)


def main() -> None:
    home()


if __name__ == '__main__':
    main()