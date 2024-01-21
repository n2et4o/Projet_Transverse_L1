import pygame as pg
pg.init()

# Class du hero
class Hero(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pv = 100
        self.pvmax = 100
        self.attack = 10
        self.vitesse_mouve = 5
        self.image = pg.image.load("Image_du_jeu/hero.gif")
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def move_right(self):
        self.rect.x += self.vitesse_mouve
    def move_left(self):
        self.rect.x -= self.vitesse_mouve

class Game :
    def __init__(self):
        self.hero = Hero()
        self.pressed = {}