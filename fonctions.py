import pygame as pg
pg.init()

# Class du hero
class Hero(pg.sprite.Sprite):
    def __init__(self,Game):
        super().__init__()
        self.game = Game
        self.pv = 100
        self.pvmax = 100
        self.attack = 10
        self.vitesse_mouve = 5
        self.image = pg.image.load(r"C:\Users\20220848\PycharmProjects\Projet_Transverse_L1\Image_du_jeu\hero_items\mouv_0.png")
        self.image = pg.transform.scale(self.image,(200,200))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 500
        self.all_attack = pg.sprite.Group()

    def move_right(self):
        #verification de s'il y'a collision
        #if self.game.collision(self,):
        self.rect.x += self.vitesse_mouve
    def move_left(self):
        self.rect.x -= self.vitesse_mouve
    def move_up(self):
        self.rect.y -= self.vitesse_mouve
    def move_down(self):
        self.rect.y += self.vitesse_mouve
    def Attack(self):
        self.all_attack.add(Attack_hero(self))
    def health_bar(self, surface):
        # Couleur de la barre utilisant le code RGB (R,G,B)
        bar_color = (172, 255, 51)
        # Position de la barre de vie (x,y,width,height)
        bar_position = [self.rect.x + 30,self.rect.y,self.pv,5]
        pg.draw.rect(surface,bar_color,bar_position)
        bar_position = [self.rect.x + 30, self.rect.y,self.pvmax, 5]
class Game :
    def __init__(self):
        self.hero = Hero(self)
        self.pressed = {}
    def collision(self,sprite,Group):
        return pg.sprite.spritecollide(sprite,Group,False, sprite.collide_mask)

class Attack_hero(pg.sprite.Sprite):
    def __init__(self,hero):
        super(Attack_hero, self).__init__()
        self.vitesse_attack = 5
        self.hero = hero
        self.image = pg.image.load(r"C:\Users\20220848\PycharmProjects\Projet_Transverse_L1\Image_du_jeu\PygameAssets-main\projectile.png")
        self.image = pg.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x + 150
        self.rect.y = hero.rect.y + 150
    def remouve(self):
        self.hero.all_attack.remove(self)
    def mouv_attack(self):
        self.rect.x += self.vitesse_attack

        # Verification et suppression de l'attque si celui-ci est en dehors de l'ecran
        if self.rect.x > 1080:
            self.remouve

class Animation(pg.sprite.Sprite):
    def __init__(self,sprite_name):
        super().__init__()
        self.image = pg.image.load(f'Image_du_jeu/ {sprite_name}.png')
def load_animate_image(sprite_name):
    # Charger les images
    images = []

