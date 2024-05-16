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

class Sound():
    def __init__(self):
        self.theme = pg.mixer_music.load("Musiques_et_sons/Musique.wav")
        self.theme_volume = pg.mixer_music.set_volume(0.7)
        self.theme = pg.mixer_music.play(-1, fade_ms=40000)
        self.death = pg.mixer.Sound("Musiques_et_sons/death.wav")
        self.attack = pg.mixer.Sound("Musiques_et_sons/boule_de_feu_lancement.wav")
        self.up = pg.mixer.Sound("Musiques_et_sons/pop.wav")
        self.stalactite = pg.mixer.Sound("Musiques_et_sons/stalactite.wav")
        self.unsheathed = pg.mixer.Sound("Musiques_et_sons/unsheathed.wav")
sound = Sound()

run0 = trouver_image("run_0.png")
at = trouver_image("hero_attack.png")
run1 = trouver_image("0.png")
keur = trouver_image("keur.png")
fps_factor = 2
boss_phase = 1
counter_animation = 0

lances_side = pg.image.load("Image_du_jeu/spear_side/spear_final.png")
ice_ball = pg.image.load("Image_du_jeu/ice_ball0.png")
groundattack = pg.image.load("Image_du_jeu/queue.png")
stalactite = pg.image.load("Image_du_jeu/stalactite.png")
lances_down = pg.image.load("Image_du_jeu/spear/spear_final.png")

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



def load_animate_image_boss(sprite_name, phase):
    # Charger les images
    images = []
    path = f"Image_du_jeu/{sprite_name}/phase_{phase}/{sprite_name}{phase}_"
    if phase == '1':
        for num in range(1, 6):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '15':
        for num in range(1, 29):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '2':
        for num in range(1, 7):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '25':
        for num in range(1, 21):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '3':
        for num in range(1, 4):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '35':
        for num in range(1, 31):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '245':
        for num in range(1, 11):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '246':
        for num in range(1, 3):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    elif phase == '5':
        for num in range(1, 17):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))

    else:
        for num in range(1, 4):
            images_path = path + str(num) + ".png"
            images.append(pg.image.load(images_path))
    return images

dict_animation_boss = {
    "1": load_animate_image_boss('mob', '1'),
    "2": load_animate_image_boss('mob', '2'),
    "3": load_animate_image_boss('mob', '3'),
    "5": load_animate_image_boss('mob', '5'),
    "15": load_animate_image_boss('mob', '15'),
    "245": load_animate_image_boss('mob', '245'),
    "246": load_animate_image_boss('mob', '246'),
    "25": load_animate_image_boss('mob', '25'),
    "35": load_animate_image_boss('mob', '35'),
}



class Animatesprite(pg.sprite.Sprite):
    def __init__(self, sprite_name):
        super().__init__()
        self.boss = Boss
        self.image = pg.image.load(f'Image_du_jeu/{sprite_name}.png')
        self.image = pg.transform.scale(self.image, (300, 500))
        self.image_current = 0
        self.boss_phase = boss_phase
        self.images = dict_animation_boss.get(str(self.boss_phase))
        self.animation = False
        self.dead = False
        self.counter = 0
        self.music = sound


    def start_animation(self):
        self.animation = True
    def death(self):
        self.dead = True

    def animate(self, boss):
        self.boss = boss
        self.new_phase = self.boss.phase
        if self.new_phase != self.boss_phase:
            # Reset animation variables when phase changes
            self.image_current = 0
            self.boss_phase = self.new_phase
            self.images = dict_animation_boss.get(str(self.boss.phase))
        self.counter += 1
        if self.counter % 5 == 0 and self.boss.phase < 5:
            self.image_current += 1
        if self.counter % 8 == 0 and self.boss.phase == 5:
            self.image_current += 1
        if self.counter % 2 == 0 and self.boss.phase == 15:
            self.image_current += 1
        if self.counter % 2 == 0 and self.boss.phase == 25:
            self.image_current += 1
        if self.counter % 2 == 0 and self.boss.phase == 35:
            self.image_current += 1
        if self.counter % 8 == 0 and self.boss.phase == 245:
            self.image_current += 1
        if self.counter % 4 == 0 and self.boss.phase == 246:
            self.image_current += 1

        # Vérification de la fin de l'animation
        if self.image_current >= len(self.images) and not self.boss.animation_end:
            if self.boss.phase == 15:
                self.boss.change_phase = 2
            if self.boss.phase == 245:
                self.boss.change_phase = 246
                self.boss.fake_death_beggining = pg.time.get_ticks()
            if self.boss.phase == 25:
                self.boss.change_phase = 3
            if self.boss.phase == 35:
                self.boss.change_phase = 3
            if self.boss.phase == 5:
                self.boss.animation_end = True
            # Revenir à l'image de départ
            self.image_current = 1

        if self.boss.animation_end:
            self.image = pg.image.load(f'Image_du_jeu/mob/phase_5/mob5_16.png')
        else:
            self.image = self.images[self.image_current]
        if self.boss.phase == 3 or self.boss.phase == 35 or self.boss.phase == 5:
            self.image = pg.transform.scale(self.image, (250, 450))
            self.boss.rect.x = 1000
            self.boss.rect.y = 250
        elif self.boss.phase == 25:
            self.image = pg.transform.scale(self.image, (240/0.7, 450/0.94))
            self.boss.rect.x = 975
            self.boss.rect.y = 220

        else:
            self.image = pg.transform.scale(self.image, (400, 650))


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
        self.counter = 0


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
                self.counter += 1
                if self.counter % 10:
                    self.image_current += 1
                # Vérification de la fin de l'animation
                if self.image_current >= len(self.images):
                    # Revenir à l'image de départ
                    self.image_current = 24
                    self.game_over = True
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

# Class du hero
class Hero(Animation):
    def __init__(self, Game):
        super().__init__('hero')
        self.game = Game
        self.pv = 100
        self.pvmax = 100
        self.attack = 100
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
        self.image_heart = pg.image.load(keur)
        self.image_heart = pg.transform.scale(self.image_heart, (50,50))
        self.game_over = False
        self.music = sound

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
        self.music.attack.play()

    def Trajectoire(self):
        self.all_trajectoire.add(Trajectoire_hero(self))

    def update_animation(self, direction):
        self.animate(direction)

    def health_bar(self, surface):
        # Couleur de la barre utilisant le code RGB (R,G,B)
        bar_color = (172, 255, 51)
        # Position de la barre de vie (x,y,width,height)
        bar_position = [30, 5, self.pv, 5]
        #pg.draw.rect(surface, bar_color, bar_position)
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
        self.fps = 60
        self.platform_group = Group()
        self.list_platform = [
            pg.Rect(00, 450, 150, 40), pg.Rect(400, 450, 150, 40), pg.Rect(600, 250, 150, 40),
            pg.Rect(200, 250, 150, 40)
        ]
        self.platform_position = [(0, 449), (400, 449), (600, 249), (200, 249)]
        self.music = sound

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


class Boss(Animatesprite):
    def __init__(self):
        super().__init__("mob")
        self.game = Game
        self.pv = 700
        self.pvmax = 700
        self.attack = 1
        boss_image = trouver_image('3.0.png')
        #self.image = pg.image.load(boss_image)
        #self.image = pg.transform.scale(self.image, (200*1.2, 300*1.2))
        self.rect = self.image.get_rect()
        self.all_attack_boss = pg.sprite.Group()
        self.rect.x = 880
        self.rect.y = 70
        self.last_attack_time = 0
        self.attack_interval = 2
        self.last_remove = pg.time.get_ticks()
        self.phase = boss_phase
        self.change_phase = 0
        self.cooldown = 2700
        self.active = False
        self.fake_death_beggining = 0
        self.animation_end = False

    def update(self, surface, phase):
        # Affichage de la bar de vie
        pygame.draw.rect(surface, (60, 63, 60), [255, 35, self.pvmax + 10, 15])
        pygame.draw.rect(surface, (150, 100, 250), [260, 40, self.pv, 5])
        self.animate(self)
        self.phase = phase

    def update_boss_phase(self):
        self.phase = 3

    def damage(self, amount):
        if self.active:
            self.pv -= amount



    def Attack_boss(self, hero_x, hero_y):
        if self.active:
            rand_attack = 6
            if self.phase == 2:
                rand_attack = random.randint(1, 3)
            if self.phase == 35:
                rand_attack = random.randint(1, 6)

            safe_space_down = random.randint(2, 5)
            safe_space_side = random.randint(2, 3)

            if rand_attack == 1:
                self.all_attack_boss.add(Attack1_boss(self, hero_x, hero_y))
            elif rand_attack == 2:
                self.all_attack_boss.add(GroundAttack(self, hero_x, hero_y))
            elif rand_attack == 3:
                self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
                self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
                self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
                self.all_attack_boss.add(Stalactite(self, hero_x, hero_y))
            elif rand_attack == 4:
                self.all_attack_boss.add(Ice_work(self, hero_x, hero_y))
            elif rand_attack == 5:
                for i in range(0, 5):
                    if i != safe_space_side:
                        self.all_attack_boss.add(Lances_side(self, hero_x, hero_y, i))
            elif rand_attack == 6:
                for i in range(0, 7):
                    if i != safe_space_down:
                        self.all_attack_boss.add(Lances_down(self, hero_x, hero_y, i))



class Attack1_boss(pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y):
        super(Attack1_boss, self).__init__()
        self.boss = boss
        self.image = ice_ball
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = boss.rect.x
        self.rand_parameter = random.randint(0, 1)
        self.rect.y = boss.rect.y
        start_position = 150
        self.up_or_down = 1
        if self.rand_parameter == 0:
            start_position = random.choice([0, 150, 350])
            self.rect.y += start_position
            if start_position != 0:
                self.up_or_down = random.choice([-1, 1])
        if self.rand_parameter == 1:
            self.rect.y = hero_y + 25
            self.up_or_down = random.choice([-1, 1])


    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        # Paramètres de la sinusoidale (vitesse_horizontale, amplitude, fréquence) pour faire des trajectoires intéréssantes
        sinusoidal_parameters = [[7, 30, self.up_or_down * 0.01], [10, 30, self.up_or_down * 0.03]]
        self.vitesse_attack = sinusoidal_parameters[self.rand_parameter][0]
        self.rect.x -= self.vitesse_attack
        # Paramètres de la trajectoire sinusoidale
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
        self.image = groundattack
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
        self.image = stalactite
        self.image = pg.transform.scale(self.image, (30, 100))
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([150, 400, 650])
        self.rect.y = random.randint(-500, 0)
        self.vitesse_attack = 18


    def remouve(self):
        sound.stalactite.set_volume(0.3)
        sound.stalactite.play()
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        self.rect.y += self.vitesse_attack
        if self.rect.y > 800:
            self.remouve()


class Lances_down (pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y, n):
        super(Lances_down, self).__init__()
        self.boss = boss
        self.image = lances_down
        self.image = pg.transform.scale(self.image, (75, 250))
        self.rect = self.image.get_rect()
        positions = [0, 150, 300, 450, 600, 750, 900]
        self.rect.x = positions[n]
        self.rect.y = -50
        self.vitesse_attack = 25
        self.state = "waiting"  # État initial : l'arme est cachée sous le sol
        self.last_show_time = time.time()


    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        if self.state == "waiting":
            current_time = time.time()
            sound.unsheathed.set_volume(0.025)
            sound.unsheathed.play()
            current_time = time.time()
            if current_time - self.last_show_time >= 0.9:
                self.state = "down"
        if self.state == "down":
            self.rect.y += self.vitesse_attack
            if self.rect.y > 900:
                self.remouve()


class Lances_side (pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y, n):
        super(Lances_side, self).__init__()
        self.boss = boss
        self.image = lances_side
        self.image = pg.transform.scale(self.image, (250, 75))
        self.rect = self.image.get_rect()
        positions = [-20, 150, 320, 490, 660]
        self.rect.x = boss.rect.x
        self.rect.y = positions[n]
        self.vitesse_attack = 25
        self.state = "waiting"  # État initial : l'arme est cachée sous le sol
        self.last_show_time = time.time()


    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        if self.state == "waiting":
            current_time = time.time()
            sound.unsheathed.set_volume(0.025)
            sound.unsheathed.play()
            if current_time - self.last_show_time >= 0.6:
                self.state = "side"
        if self.state == "side":
            self.rect.x -= self.vitesse_attack
            if self.rect.x < -150:
                self.remouve()

class Ice_work (pg.sprite.Sprite):
    def __init__(self, boss, hero_x, hero_y):
        super(Ice_work, self).__init__()
        self.boss = boss
        self.image = ice_ball
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = boss.rect.x
        position = random.choice([320, 490])
        self.rect.y = position
        self.vitesse_attack = 18
        self.state = "waiting"  # État initial : l'arme est cachée sous le sol
        self.last_show_time = time.time()


    def remouve(self):
        cross = random.choice([1, 2])
        position = self.rect.y
        sound.stalactite.set_volume(0.3)
        sound.stalactite.play()
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)
        for i in range(0, 4):
            self.boss.all_attack_boss.add(Ice_ball(self.boss, i, position, cross))

    def mouv_attack(self,screen):
        self.rect.x -= self.vitesse_attack
        if self.rect.x < 400:
            self.remouve()

class Ice_ball (pg.sprite.Sprite):
    def __init__(self, boss, n, position, cross):
        super(Ice_ball, self).__init__()
        self.boss = boss
        self.image = ice_ball
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = position
        if cross == 1:
            self.vitesse_attack = 14
        else:
            self.vitesse_attack = 20
        self.directionx = 1
        self.directiony = 1
        if n == 0:
            self.directionx = -1
            if cross == 1:
                self.directiony = -1
            else:
                self.directiony = 0
        if n == 1:
            if cross == 1:
                self.directionx = -1
            else:
                self.directionx = 0
        if n == 2:
            self.directiony = -1
            if cross == 2:
                self.directionx = 0
        if n == 3:
            if cross == 2:
                self.directiony = 0


    def remouve(self):
        self.boss.last_remove = pg.time.get_ticks()
        self.boss.all_attack_boss.remove(self)

    def mouv_attack(self,screen):
        self.rect.x += self.vitesse_attack * self.directionx
        self.rect.y += self.vitesse_attack * self.directiony
        if self.directiony == 1:
            if self.rect.y > reso_l:
                self.remouve()
        elif self.directiony == -1:
            if self.rect.y < -50:
                self.remouve()
        else:
            if self.directionx == 1:
                if self.rect.x > reso_h-100:
                    self.remouve()
            else:
                if self.rect.x < -50:
                    self.remouve()
