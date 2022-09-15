from random import randint
from pygame.display import *
from pygame import *
import pygame
import sys
from time import sleep
init()
img = image.load
canvas = set_mode((480, 700), 0, 32)
set_caption("飞机大战")
speed = 8
enemies = sprite.Group()
bullets = sprite.Group()
hero = sprite.Group()
enemyBullets = sprite.Group()


class Background(object):
    def __init__(self):
        self.image = img("images/background.png")

    def draw(self, x, y):
        canvas.blit(self.image, (x, y))


class Hero(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img("images/me1.png")
        self.rect = self.image.get_rect()
        self.rect.x = 189
        self.rect.y = 425
        self.game_state = False

    def draw(self, x, y):
        canvas.blit(self.image, (x, y))
        self.rect.x = x
        self.rect.y = y

    def explode(self):
        bomb = []
        for x in range(1, 5):
            bomb.append(img("images/me_destroy_" + str(x) + ".png"))
        for b in range(0, 4):
            canvas.blit(bomb[b], (self.rect.x, self.rect.y))
        hero.remove(self)


class Enemy(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img("images/enemy1.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.state = "right"

    def explode(self):
        bomb = []
        for x in range(1, 5):
            bomb.append(img("images/enemy1_down" + str(x) + ".png"))
        for b in range(0, 4):
            canvas.blit(bomb[b], (self.rect.x, self.rect.y))
        enemies.remove(self)


class Bullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img("images/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class EnemyBullet(sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = img("images/bullet2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        canvas.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.y += 6
        if self.rect.y >= 700:
            enemyBullets.remove(self)

class Setting(object):
    def __init__(self):
        self.regame = img("images/again.png")
        self.gameover = img("images/gameover.png")
        self.spacing = 10

    def paint(self):
        canvas.blit(self.regame, (240 - self.regame.get_width() / 2, 300))
        canvas.blit(self.gameover, (240 - self.regame.get_width() / 2, 370))

class Manager(object):
    def __init__(self):
        self.bg_y = 0
        self.bg_y1 = -700
        self.hero_x = 189
        self.hero_y = 425
        self.score = 0
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def background_move(self):
        Background().draw(0, self.bg_y)
        Background().draw(0, self.bg_y1)
        self.bg_y += 2.5
        self.bg_y1 += 2.5
        if self.bg_y >= 700:
            self.bg_y = -700
        if self.bg_y1 >= 700:
            self.bg_y1 = -700

    def key_ctrl(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_DOWN]:
            self.hero_y -= speed
        if key_pressed[K_a] or key_pressed[K_DOWN]:
            self.hero_x -= speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.hero_y += speed
        if key_pressed[K_d] or key_pressed[K_DOWN]:
            self.hero_x += speed
        for bullet in bullets:
            canvas.blit(bullet.image, (bullet.rect.x, bullet.rect.y))
            bullet.rect.y -= 10
            if bullet.rect.y <= -11:
                bullet.kill()

    def add_enemy(self):
        if randint(0, 80) == 0:
            enemies.add(Enemy(randint(0, 423), randint(-360, -60)))
        for enemy in enemies:
            if enemy.rect.y >= 700:
                enemy.rect.y = -600
            for h in hero:
                if sprite.groupcollide(hero, enemies, False, False):
                    h.explode()
                    enemy.explode()
                for bullet in enemyBullets:
                    bullet.draw()
                    if sprite.groupcollide(hero, enemyBullets, False, True):
                        h.explode()
            if randint(0, 140) == 0:
                enemyBullets.add(EnemyBullet(enemy.rect.x + 22, enemy.rect.y + 42))
            if enemy.state == "right":
                enemy.rect.x += 4
            elif enemy.state == "left":
                enemy.rect.x -= 4
            if enemy.rect.x >= 420:
                enemy.state = "left"
            if enemy.rect.x <= 0:
                enemy.state = "right"
            canvas.blit(enemy.image, (enemy.rect.x, enemy.rect.y))
            enemy.rect.y += 4
            if sprite.groupcollide(enemies, bullets, False, True):
                enemy.explode()
                self.score += 10
    
    def add_bullet(self):
        bullets.add(Bullet(self.hero_x + 50, self.hero_y - 9))

    def show_score(self):
        font = pygame.font.Font("font/font.ttf", 42)
        text = f"score:{self.score}"
        score = font.render(text, True, (255, 255, 255))
        canvas.blit(score, (10, 0))

    def main(self):
        hero.add(Hero())        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.add_bullet()

            canvas.fill((255, 255, 255))

            self.background_move()
            self.add_enemy()
            self.key_ctrl()

            for h in hero:
                h.draw(self.hero_x, self.hero_y)
            if self.hero_x > 480:
                self.hero_x = -102
            if self.hero_x < -102:
                self.hero_x = 480
            print(f"{self.mouse_x}, {self.mouse_x}")
            self.show_score()
            update()
            sleep(0.01)


if __name__ == "__main__":
    Manager().main()
