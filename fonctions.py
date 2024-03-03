import pygame as pg
pg.init()
import os, time, sys
from pygame.sprite import Group

# Adaptation du chemin d'accès à n'importe quel appareil
def trouver_image(nom_image):
    # Récupérer le répertoire racine du projet
    repertoire_racine = os.getcwd()
    # Parcourir récursivement le système de fichiers à partir du répertoire racine
    for dossier_racine, sous_repertoires, fichiers in os.walk(repertoire_racine):
        # Vérifier si l'image recherchée se trouve dans les fichiers du dossier courant
        if nom_image in fichiers:
            chemin_image = os.path.join(dossier_racine, nom_image)
            return chemin_image
    # Si l'image n'est pas trouvée, retourner None
    return None


run0 = trouver_image("run_0.png")


# Class du hero
class Hero(pg.sprite.Sprite):
    def __init__(self, Game):
        super().__init__()
        self.game = Game
        self.pv = 100
        self.pvmax = 100
        self.attack = 10
        self.vitesse_mouve = 11
        self.image = pg.image.load(run0)
        self.image = pg.transform.scale(self.image, (150,150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400
        self.all_attack = pg.sprite.Group()
        self.animation = Animation("hero")
        self.jump = 0
        self.jump_up = 0
        self.jump_down = 5
        self.nb_jump = 0
        self.jumped = False
        self.direction = 1

    def jumpe(self):
        if self.jumped:
            if self.jump_up >= 10:
                self.jump_down -= 10
                self.jump = self.jump_down
            else:
                self.jump_up += 1
                self.jump = self.jump_up

            if self.jump_down < 0:
                self.jump_up = 0
                self.jump_down = 9
                self.jumped = False
        self.rect.y = self.rect.y - (12 * (self.jump/2))

    def move_right(self):
        #verification de s'il y'a collision
        #if self.game.collision(self,):
        self.rect.x += self.vitesse_mouve
    def move_left(self):
        self.rect.x -= self.vitesse_mouve
    def move_up(self):
        self.rect.y -= self.vitesse_mouve
    #def move_down(self):
     #   self.rect.y += self.vitesse_mouve
    def Attack(self):
        self.all_attack.add(Attack_hero(self))
    def update_animation(self):
        self.animation.animate()
        self.image = self.animation.image
    def health_bar(self, surface):
        # Couleur de la barre utilisant le code RGB (R,G,B)
        bar_color = (172, 255, 51)
        # Position de la barre de vie (x,y,width,height)
        bar_position = [self.rect.x + 30,self.rect.y,self.pv,5]
        #heart = trouver_image("keur.png")
        #self.image = pg.image.load(heart)
        #self.image = pg.transform.scale(self.image, (50, 50))
        pg.draw.rect(surface,bar_color,bar_position)
        bar_position = [self.rect.x + 30, self.rect.y,self.pvmax, 5]
class Game :
    def __init__(self):
        self.hero = Hero(self)
        self.pressed = {}
        self.gravite = 10
        self.resistance = 0
        self.ground = Ground()
        self.collision_ground = False
        self.rect_limite = pg.Rect(0, 0, 1280, 720)
        self.clock = pg.time.Clock()
        self.fps = 30
        self.platform_group = Group()
        self.list_platform = [
            pg.Rect(00,450,150,40),pg.Rect(400,450,150,40),pg.Rect(600,250,150,40),pg.Rect(200,250,150,40)
        ]

    def collision(self,sprite,Group):
        return pg.sprite.spritecollide(sprite,Group,False, sprite.collide_mask)
    def application_gravite(self):
        self.hero.rect.y += self.gravite + self.resistance
        # Vérification d'une collision entre le sol et joueur
        if self.ground.rect.colliderect(self.hero.rect):
            self.resistance = -10
            self.collision_ground = True
            self.hero.nb_jump = 0
        else:
            self.resistance = 0
        if self.hero.jumped and self.collision_ground:
            if self.hero.nb_jump < 2:
                self.hero.jumpe()
        if self.hero.rect.y < 0:
            self.hero.rect.y = 0


class Attack_hero(pg.sprite.Sprite):
    def __init__(self,hero):
        super(Attack_hero, self).__init__()
        self.vitesse_attack = 10
        self.hero = hero
        projectile = trouver_image("projectile.png")
        self.image = pg.image.load(projectile)
        self.image = pg.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.x = hero.rect.x + 130
        self.rect.y = hero.rect.y + 60
        self.direction = hero.direction
    def remouve(self):
        self.hero.all_attack.remove(self)
    def mouv_attack(self,screen):
        self.rect.x += self.vitesse_attack * self.direction
        #self.rect.y =((0.5*self.rect.x) /(self.vitesse_attack * math.cos(45))) + (self.vitesse_attack * self.rect.x * math.tan(45)) + self.rect.y
        # Verification et suppression de l'attque si celui-ci est en dehors de l'ecran
        if self.rect.x > screen.get_width():
            self.remouve()


class Animation(pg.sprite.Sprite):
    def __init__(self,sprite_name):
        super().__init__()
        self.image = pg.image.load(f'Image_du_jeu/{sprite_name}_items/run_0.png')
        self.image_current = 0
        self.images = dict_animation.get("hero")
    def animate(self):

        # Passer à l'image suivante
        self.image_current += 1
        # Vérification de la fin de l'animation
        if self.image_current >= len(self.images) :
            # Revenir à l'image de départ
            self.image_current = 0
        self.image = self.images[self.image_current]
def load_animate_image(sprite_name):
    # Charger les images
    images = []
    path = f"Image_du_jeu/{sprite_name}_items/run_"
    for num in range(0,6):
        images_path = path + str(num) + ".png"
        images.append(pg.image.load(images_path))

    return images

dict_animation = {
    "hero" : load_animate_image("hero")
}

# Classe du Sol
class Ground(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pg.Rect(0,650,1280,170)
    def afficher_sol(self,surface):
        pg.draw.rect(surface,(0,255,0), self.rect)

class Ground_up(pg.sprite.Sprite):
    def __init__(self,rect):
        super().__init__()
        self.rect = rect
    def afficher_platform(self,surface):
        pg.draw.rect(surface,(51, 246, 255), self.rect)




