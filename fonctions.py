import math
import os
import random
import time

import pygame as pg
import pygame.sprite
from pygame.sprite import Group

pg.init()
pg.joystick.init()  # Initialisation du système de joystick


reso_h = 1280
reso_l = 720

clock = pygame.time.Clock()

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
at = trouver_image("hero's_attack.png")
run1 = trouver_image("0.png")
fps_factor = 2
#run0 = trouver_image("run_0.png")
#at = trouver_image("hero's_attack.png")

class Animation(pg.sprite.Sprite):
    def __init__(self, sprite_name):
        super().__init__()
        self.hero = Hero
        self.image = pg.image.load(run1)
        self.image = pg.transform.scale(self.image, (150, 150))
        self.image_current = 0
        self.images = dict_animation.get("walk")
        self.animation = False
        self.dead = False


    def start_animation(self):
        self.animation = True
    def death(self):
        self.dead = True

    def animate(self, direction):
        # Verification de si l'animation est active
        if self.animation:
            # Vérification de la mort du heros et lancement de l'animation de mort
            if self.dead == True:
                self.images = dict_animation.get("death")
                #self.dead = False
                # Passer à l'image suivante
                self.image_current += 1
                # Vérification de la fin de l'animation
                if self.image_current >= len(self.images):
                    # Revenir à l'image de départ
                    self.image_current = 24
                    self.animation = False
                self.image = self.images[self.image_current]
                self.image = pg.transform.scale(self.image, (150, 150))
                if direction == -1:
                    self.image = pg.transform.flip(self.image, True, False)
                #self.dead = False
            else :
                # Passer à l'image suivante
                self.image_current += 1
                # Vérification de la fin de l'animation
                if self.image_current >= len(self.images):
                    # Revenir à l'image de départ
                    self.image_current = 0
                    self.animation = False
                self.image = self.images[self.image_current]
                self.image = pg.transform.scale(self.image, (150, 150))
                if direction == -1:
                    self.image = pg.transform.flip(self.image, True, False)

    def start_attack(self, go):
        if go == True:
            first = self.image
            self.image = pg.image.load(at)
            self.image = pg.transform.scale(self.image, (150, 150))
            self.image = first
            #go = False

def load_animate_image(sprite_name):
    # Charger les images
    images = []
    if sprite_name == "death":
        path = f"Image_du_jeu/{sprite_name}/"
        for num in range(0, 25):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif sprite_name == "walk":
        path = f"Image_du_jeu/{sprite_name}/"
        for num in range(0, 7):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    else:
        path = f"Image_du_jeu/{sprite_name}_items/run_"
        for num in range(0, 7):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    return images

dict_animation = {
    "hero": load_animate_image("hero"),
    "death": load_animate_image("death"),
    "walk": load_animate_image("walk")
}

# Class du hero
class Hero(Animation):
    def __init__(self, Game):
        super().__init__('hero')
        self.game = Game
        self.pv = 100
        self.pvmax = 100
        self.attack = 10
        self.vitesse_mouve = 10 * fps_factor
        #self.image = pg.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 400
        self.all_attack = pg.sprite.Group()
        self.all_trajectoire = pg.sprite.Group()
        self.jump = 0
        self.jump_up = 0
        self.jump_down = 5
        self.nb_jump = 0
        self.jumped = False
        self.direction = 1
        self.t1 , self.t2 = 0,0
        self.delta_temps = 0
        self.get_degats = 0
        keur = trouver_image("keur.png")
        self.image_heart = pg.image.load(keur)
        self.image_heart = pg.transform.scale(self.image_heart, (50,50))

    def nombre_coeurs(self):
        # Admettons que chaque coeur représente 25 points de vie
        return self.pv // 25  # Utilisez la division entière pour obtenir un nombre entier

    def deltas(self, t1,t2,delta_temps):
        delta_temps = t1 - t2
        print("t1 = ",t1)
        print("t2 = ",t2)
        print("delta =",delta_temps)

    def can_attack(self, temps_de_pause):
        self.delta_temps = time.time() - self.t2
        return self.delta_temps >= temps_de_pause

    def jumpe(self):
        if self.jumped:
            if self.jump_up >= 11:
                self.jump_down -= 10 * fps_factor
                self.jump = self.jump_down
            else:
                self.jump_up += 1
                self.jump = self.jump_up

            if self.jump_down < 0:
                self.jump_up = 0
                self.jump_down = 9
                self.jumped = False
        self.rect.y = self.rect.y - (12 * (self.jump / 2))

    def move_right(self):
        # verification de s'il y'a collision
        # if self.game.collision(self,):
        self.rect.x += self.vitesse_mouve

    def move_left(self):
        self.rect.x -= self.vitesse_mouve

    def move_up(self):
        self.rect.y -= self.vitesse_mouve

    # def move_down(self):
    #   self.rect.y += self.vitesse_mouve
    def Attack(self):
        self.all_attack.add(Attack_hero(self))

    def Trajectoire(self):
        self.all_trajectoire.add(Trajectoire_hero(self))

    def update_animation(self, direction):
        self.animate(direction)

    def health_bar(self, surface):
        # Couleur de la barre utilisant le code RGB (R,G,B)
        bar_color = (172, 255, 51)
        # Position de la barre de vie (x,y,width,height)
        bar_position = [ 30,10 , self.pv + 7, 5]
        pg.draw.rect(surface, bar_color, bar_position)
        #bar_position = [self.rect.x + 30, self.rect.y, self.pvmax, 5]




class Game:
    def __init__(self):
        self.hero = Hero(self)
        self.boss = Boss()
        self.bosssprite = pg.sprite.Group()
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
            pg.Rect(00, 450, 150, 40), pg.Rect(400, 450, 150, 40), pg.Rect(600, 250, 150, 40),
            pg.Rect(200, 250, 150, 40)
        ]
        if self.boss.pv > 0:
            self.spawnboss()

    def spawnboss(self):
        self.boss = Boss()
        self.bosssprite.add(self.boss)

    def collision(self, sprite, Group):
        return pg.sprite.spritecollide(sprite, Group, False, sprite.collide_mask)

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


class Trajectoire_hero(pg.sprite.Sprite):
    def __init__(self, hero):
        super().__init__()
        self.vitesse = 50  # Vitesse initiale du projectile
        self.hero = hero
        self.angle = math.radians(45)  # Angle de lancement en radians

        projectile = trouver_image("fire.png")
        self.image = pg.image.load(projectile)
        self.image = pg.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        self.direction = hero.direction
        self.set_position()

        self.start_ticks = pg.time.get_ticks()  # Sauvegarde le moment du lancement

    def set_position(self):
        if self.direction == 1:  # Direction droite
            self.rect.x = self.hero.rect.x + self.hero.rect.width
        else:  # Direction gauche
            self.rect.x = self.hero.rect.x - self.image.get_width()
            self.image = pg.transform.flip(self.image, True, False)
        self.rect.y = self.hero.rect.y + self.hero.rect.height // 2
        self.x_init = self.rect.x
        self.y_init = self.rect.y

    def remove_trajectoire(self):
        self.hero.all_trajectoire.remove(self)

    def move_trajectoire(self, screen):
        ticks = pg.time.get_ticks()
        temps = (ticks - self.start_ticks) / 1000  # Temps en secondes

        # Calcul de la position x en utilisant la vitesse initiale et l'angle

        # Calcul de la position y en prenant en compte la gravité
        g = 9.81  # Accélération due à la gravité (en m/s^2, ajustez pour votre échelle)

        temps_accelere = temps * 10  # Multiplier le temps par un facteur pour accélérer
        self.rect.x = self.x_init + self.vitesse * math.cos(self.angle) * temps_accelere * self.direction
        self.rect.y = self.y_init - (self.vitesse * math.sin(self.angle) * temps_accelere - 0.5 * g * temps_accelere ** 2)

        if self.rect.x < 0 or self.rect.x > screen.get_width() or self.rect.y > screen.get_height():
            self.remove_trajectoire()
            #print("fire ball supprimé")

class Attack_hero(pg.sprite.Sprite):
    def __init__(self, hero):
        super(Attack_hero, self).__init__()
        self.vitesse_attack = 15
        self.hero = hero
        projectile = trouver_image("fire_2.png")
        self.image = pg.image.load(projectile)
        self.image = pg.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.y = hero.rect.y + 60
        self.direction = hero.direction
        if self.direction == -1:
            self.rect.x = hero.rect.x - 51
            self.image = pg.transform.flip(self.image, True, False)
        else:
            self.rect.x = hero.rect.x + 130

    def remouve(self):
        self.hero.all_attack.remove(self)

    def mouv_attack(self, screen):
        if self.direction == 1:  # Direction droite
            self.rect.x += self.vitesse_attack
        else:  # Direction gauche
            self.rect.x -= self.vitesse_attack

        # Verification et suppression de l'attaque si celle-ci est en dehors de l'écran
        if self.rect.x > screen.get_width() or self.rect.x < 0:
            self.remouve()


# Classe du Sol
class Ground(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pg.Rect(0, 650, 1280, 170)

    def afficher_sol(self, surface):
        pg.draw.rect(surface, (51, 204, 255), self.rect)


class Ground_up(pg.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect

    def afficher_platform(self, surface):
        pg.draw.rect(surface, (51, 246, 255), self.rect)


class Boss(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.game = Game
        self.pv = 500
        self.pvmax = 700
        self.attack = 1
        boss_image = trouver_image('mob.png')
        self.image = pg.image.load(boss_image)
        self.image = pg.transform.scale(self.image, (500, 500))
        self.rect = self.image.get_rect()
        self.all_attack_boss = pg.sprite.Group()
        self.rect.x = 820
        self.rect.y = 200
        self.last_attack_time = 0
        self.attack_interval = 2
        self.last_remove = pg.time.get_ticks()
        self.phase = 1
        self.actif = True
        self.cooldown = 800

    def update_health_bar(self, surface):
        # Affichage de la bar de vie
        pygame.draw.rect(surface, (60, 63, 60), [260, 40, self.pvmax, 5])
        pygame.draw.rect(surface, (100, 0, 200), [260, 40, self.pv, 5])

    def damage(self, amount):
        self.pv -= amount
        if self.pv <= self.pvmax / 2 and self.phase == 1:
            self.phase = 2
        if self.pv <= 0:
            self.phase = 3

    def Attack_boss(self, hero_x, hero_y):
        rand_attack = random.randint(0, 3)
        if rand_attack == 0:
            self.all_attack_boss.add(GroundAttack(self, hero_x, hero_y))
        if rand_attack == 1:
            self.all_attack_boss.add(Attack1_boss(self, hero_x, hero_y))
        if rand_attack == 2:
            self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
            self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
            self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
            self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
        if rand_attack == 4:
            for i in range (0, 5):
                if i != random.randint(2, 4):
                    x = i
                    #self.all_attack_boss.add(Lances_down(self, hero_x, hero_y, i))
        if rand_attack == 5:
            for i in range (0, 10):
                if i != random.randint(2, 8):
                    x = i
                    #self.all_attack_boss.add(Lances_down(self, hero_x, hero_y, i))

class Attack1_boss(pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y):
        super(Attack1_boss, self).__init__()
        self.boss = boss
        self.image = pg.image.load("Image_du_jeu/fire.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = boss.rect.x
        self.rand_parameter = random.randint(0, 1)
        self.rect.y = boss.rect.y
        if self.rand_parameter == 1:
            self.rect.y = hero_y + 25
        self.up_or_down = random.choice([-1, 1])
    ''' start_position = 150
        if self.rand_parameter == 1:
            start_position = random.choice([0, 150, 350])
        self.rect.y = boss.rect.y + start_position'''


    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        # Paramètres de la sinusoidale (vitesse_horizontale, amplitude, fréquence) pour faire des trajectoires intéréssantes
        sinusoidal_parameters = [[7, 30, self.up_or_down * 0.01], [10, 30, self.up_or_down * 0.03]]
        self.vitesse_attack = sinusoidal_parameters[self.rand_parameter][0]
        self.rect.x -= self.vitesse_attack
        # Paramètres de la trajectoire sinusoidale
        print(self.rand_parameter)
        amplitude = 30  # Amplitude de la sinusoidale
        frequence = 0.01  # Fréquence angulaire de la sinusoidale
        self.rect.y += sinusoidal_parameters[self.rand_parameter][1] * math.sin(sinusoidal_parameters[self.rand_parameter][2] * self.rect.x)

        #self.rect.y =((0.5*self.rect.x) /(self.vitesse_attack * math.cos(45))) + (self.vitesse_attack * self.rect.x * math.tan(45)) + self.rect.y
        # Verification et suppression de l'attaque si celle-ci est en dehors de l'écran
        if self.rect.x < 0:
            self.remouve()

class GroundAttack(pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y):
        super(GroundAttack, self).__init__()
        self.boss = boss
        #queue = trouver_image("queue.png")
        self.image = pg.image.load("Image_du_jeu/queue.png")
        self.image = pg.transform.scale(self.image, (150, 550))
        self.rect = self.image.get_rect()
      # self.rect.x = boss.rect.x - random.choice([170, 370, 570])
        self.rect.x = hero_x + 50   # Positions initiales sous le sol
        self.rect.y = 670
        self.speed = 120
        self.state = "grounded"  # État initial : l'arme est cachée sous le sol
        self.last_show_time = time.time()

    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self, screen):
        if self.state == "grounded":
            # La queue monte progressivement du sol
            current_time = time.time()
            if current_time - self.last_show_time >= 0.55:
                self.state = "up"

        elif self.state == "up":
            # La queue sort complètement du sol
            self.rect.y -= self.speed
            if self.rect.y <= 269:  # Hauteur maximale atteinte par la queue
                self.state = "waiting"

        elif self.state == "waiting":
            # Attente avant de commencer à descendre
            current_time = time.time()
            if current_time - self.last_show_time >= 2:
                self.state = "down"

        elif self.state == "down":
            # La queue redescend lentement
            self.rect.y += self.speed / 1.5
            if self.rect.y >= 1000:
                self.remouve()


class Stalactite (pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y):
        super(Stalactite, self).__init__()
        self.boss = boss
        self.image = pg.image.load("Image_du_jeu/fire.png")
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([150, 400, 650])
        self.rect.y = random.randint(-500, 0)
        self.vitesse_attack = 18


    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        self.rect.y += self.vitesse_attack
        if self.rect.y > 900:
            self.remouve()
