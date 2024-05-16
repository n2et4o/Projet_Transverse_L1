import time

import pygame as pg
from pygame import Surface, SurfaceType
from fonctions import *

# Initialisation de Pygame
pg.init()
pg.joystick.init()  # Initialisation du système de joystick

# Fenêtre du jeu
pg.display.set_caption("Winter Grief")
reso_h = 1280
reso_l = 720
screen = pg.display.set_mode((reso_h, reso_l))
background_path = trouver_image("bg_2.png")
background = pg.image.load(background_path)
background = pg.transform.scale(background,(reso_h,reso_l))
background = pg.transform.scale(background, (reso_h, reso_l))
boss = Boss()
sound = Sound()
played = True
beginning_cooldown = 1000
start_cooldown = 4000
fake_death_cooldown = 4000
last_attack_boss = pg.time.get_ticks()
last_attack_hero = 0
hero_attack_cooldown = 250
# Variables permettant au héros d'avoir un peu d'invicibilité après s'être fait toucher
invicibility_cooldown = 2000
last_hit_hero = pg.time.get_ticks()
bg = pg.image.load("Image_du_jeu/background.png")
bg = pg.transform.scale(bg, (reso_h, reso_l))
win = pg.image.load("Image_du_jeu/win_screen.png")
win = pg.transform.scale(win, (reso_h, reso_l))
game_keys = pg.image.load("Image_du_jeu/game_keys.png")
game_keys = pg.transform.scale(game_keys, (192*2, 128*2))
lose = pg.image.load("Image_du_jeu/game_over.png")
lose = pg.transform.scale(lose, (reso_h, reso_l))
platformdraw = pg.image.load("Image_du_jeu/plateforme_main.png")
platformdraw = pg.transform.scale(platformdraw, (150, 41))
beginning = True
end = False


# Chargement du jeu
game = Game()

at = trouver_image("hero_attack.png")
keur = trouver_image("keur.png")

# Temps entre chaque attaque du hero
temps_de_pause = 0.1

# Vérifiez s'il y a au moins une manette connectée
if pg.joystick.get_count() > 0:
    joystick = pg.joystick.Joystick(0)  # Créez une instance de la première manette
    joystick.init()  # Initialisez la manette
    go = True
    print("Manette détectée")
else:
    go = False
    print("Aucune manette détectée")

# Boucle du jeu
running = True
while running:

    time_now = pg.time.get_ticks()
    # Initilisation de t1
    game.hero.t1 = time.time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Pression sur une touche
        elif event.type == pg.KEYDOWN:
            game.pressed[event.key] = True

            # Pression sur la touche 'a' pour réaliser une attaque
            if game.pressed.get(pg.K_a) and time_now - last_attack_hero > hero_attack_cooldown and start_cooldown == 0:
                first = game.hero.image
                game.hero.image = pg.image.load(at)
                game.hero.image = pg.transform.scale(game.hero.image, (150, 150))
                game.hero.Attack()
                last_attack_hero = pg.time.get_ticks()
                if game.hero.delta_temps >= 2:
                    game.hero.image = first

                if game.hero.direction == -1:
                    game.hero.image = pg.transform.flip(game.hero.image, True, False)
                    game.hero.Attack()
                    if game.hero.delta_temps >= 2:
                        game.hero.image = first

                # Initialisation de t2
                game.hero.t2 = time.time()  # Mise à jour de t2 après l'attaque
                #print(" delta = ", game.hero.delta_temps)

            # Pression sur la touche 'e' pour réaliser une attaque parabolique
            if event.key == pg.K_e and game.hero.can_attack(temps_de_pause) and time_now - last_attack_hero > hero_attack_cooldown and start_cooldown == 0:
                #print("Touche T pressée")
                try:
                    nouveau_projectile = Trajectoire_hero(game.hero)
                    game.hero.all_trajectoire.add(nouveau_projectile)
                    last_attack_hero = pg.time.get_ticks()
                    #print("Projectile ajouté avec succès")
                except Exception as e:
                    print(f"Erreur lors de l'ajout du projectile: {e}")

            # Pression sur la touche (up) pour effectuer un saut
            if event.key == pg.K_UP:
                sound.up.play()
                game.hero.jumped = True
                game.hero.nb_jump += 1
                if game.hero.rect.y == 0:
                    game.hero.jumped = False
            # Pression sur la touche (down) pour descendre des plateformes et descente du sol
            if event.key == pg.K_DOWN and game.hero.rect.y <= 500:
                game.resistance = 0

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False

        # Pression d'une touche sur la manette
        if event.type == pg.JOYBUTTONDOWN:
            temps_de_pause = 0.1
            # Exemple pour un bouton (le bouton X de la PS5 pour sauter)
            if event.button == 0:  # Supposons que le bouton 0 soit le bouton X
                game.hero.jumped = True
                game.hero.nb_jump += 1
                if game.hero.rect.y == 0:
                    game.hero.jumped = False

            if joystick.get_button(2) and time_now - last_attack_hero > hero_attack_cooldown and start_cooldown == 0:  # Supposons que le bouton 2 soit le bouton "Carré"
                first = game.hero.image
                game.hero.image = pg.image.load(at)
                game.hero.image = pg.transform.scale(game.hero.image, (150, 150))
                game.hero.Attack()
                if game.hero.delta_temps >= 2:
                    game.hero.image = first

                if game.hero.direction == -1:
                    game.hero.image = pg.transform.flip(game.hero.image, True, False)
                    game.hero.Attack()
                    if game.hero.delta_temps >= 2:
                        game.hero.image = first

            if joystick.get_button(1) and time_now - last_attack_hero > hero_attack_cooldown and start_cooldown == 0:  # Supposons que le bouton 1 soit le bouton "Cercle"
                nouveau_projectile = Trajectoire_hero(game.hero)
                game.hero.all_trajectoire.add(nouveau_projectile)
            # Vers le bas
            if joystick.get_button(12) > 0.1 and game.hero.rect.y <= 500:
                game.resistance = 0

            if joystick.get_button(5):
                pygame.joystick.quit()

        elif event.type == pg.JOYBUTTONUP:
            pass
            #print("Bouton relâché")

    # Vérification que la touche est pressée et que le hero ne sorte pas du cadre de l'écran
    if game.pressed.get(pg.K_RIGHT) and game.hero.rect.x + game.hero.rect.width < screen.get_width():
        game.hero.move_right()
        game.hero.start_animation()
        game.hero.direction = 1
    elif game.pressed.get(pg.K_LEFT) and game.hero.rect.x > 0:
        game.hero.move_left()
        game.hero.direction = -1
        game.hero.start_animation()

    if go:
        # Implementation de l'utilisation d'une manette
        # Lecture des entrées du joystick
        left_stick_x = joystick.get_axis(0)
        left_stick_y = joystick.get_axis(1)

        # Déplacement du héros avec le stick gauche
        if left_stick_x > 0.1 and game.hero.rect.x + game.hero.rect.width < screen.get_width():  # Déplacez à droite
            game.hero.move_right()
            game.hero.start_animation()
            game.hero.direction = 1
        elif left_stick_x < -0.1 and game.hero.rect.x > 0:  # Déplacez à gauche
            game.hero.move_left()
            game.hero.start_animation()
            game.hero.direction = -1



    # Application de gravite
    game.application_gravite()

    # Affichage du sol
    game.ground.afficher_sol(screen)

    # Affichage de l'arrière-plan
    screen.blit(background, (0, 0))

    # Mise à jour de la barre de vie du boss et de sa phase
    game.boss.update(screen, game.boss.phase)

    # Création et affichage du des platformes
    for rectangle in game.list_platform:
        platform = Ground_up(rectangle)
        game.platform_group.add(platform)
        # Conditions pour marcher sur la plateforme
        if game.hero.rect.midbottom[1] // 10 * 10 == platform.rect.top and game.hero.rect.colliderect(rectangle):
            game.resistance = -10
            game.hero.nb_jump = 0

    for platform in game.platform_group:
        platform.afficher_platform(screen)

    for i in range(0, 4):
        position = game.platform_position[i]
        screen.blit(platformdraw, position)

    # Affichage du héros
    screen.blit(game.hero.image, game.hero.rect)

    # Affichage de l'attaque
    game.hero.all_attack.draw(screen)
    game.hero.all_trajectoire.draw(screen)

    # Affichage du boss
    screen.blit(game.boss.image, game.boss.rect)



    # Affichage des attaques du boss
    game.boss.all_attack_boss.draw(screen)

    if game.hero.pv <= 0 and played:
        sound.death.play()
        print("deathsound")
        played = False

    # Changements de phases
    if game.boss.change_phase != 0:
        game.boss.phase = game.boss.change_phase
        game.boss.change_phase = 0

    if game.boss.pv < game.boss.pvmax / 2 and 1 == game.boss.phase:
        game.boss.phase = 15
        boss_phase = game.boss.phase

    if game.boss.pv <= 0 and game.boss.phase == 2:
        game.boss.phase = 245

    if game.boss.pv <= 0 and game.boss.phase == 3:
        game.boss.phase = 5
        game.boss.active = False

    if time_now - game.boss.fake_death_beggining > fake_death_cooldown and game.boss.phase == 246:
        game.boss.phase = 25
        start_cooldown = 1000
        last_attack_boss = pg.time.get_ticks() + 1000

    if 3 < game.boss.phase < 35 or game.boss.phase > 35:
        game.boss.active = False
    else:
        game.boss.active = True

    if game.boss.phase == 25 and game.boss.pv < 1000:
        game.boss.pv += 25

    if game.boss.phase == 1 and start_cooldown == 0:
        game.boss.active = True
    #Conditions pour l'apparition d'une nouvelle attaque
    #Première condition : attendre le délai au début du jeu pour pas que le joueur se fasse attaquer tout de suite
    #Deuxième condition : attendre qu'il n'y ai plus d'attaque pour en lancer une autre
    if time_now - last_attack_boss > start_cooldown + game.boss.cooldown and (game.boss.phase == 1 or game.boss.phase == 2):
        start_cooldown = 0
        last_attack_boss = pg.time.get_ticks()
        game.boss.Attack_boss(game.hero.rect.x, game.hero.rect.y)

    if time_now - last_attack_boss > game.boss.cooldown - 500 + start_cooldown and game.boss.phase == 3:
        game.boss.phase = 35

    if time_now - last_attack_boss > game.boss.cooldown + start_cooldown and game.boss.phase == 35:
        game.boss.Attack_boss(game.hero.rect.x, game.hero.rect.y)
        last_attack_boss = pg.time.get_ticks()
        start_cooldown = 0

    # Boucle d'affichage des projectiles
    for i in game.hero.all_attack:
        i.mouv_attack(screen)
        if game.boss.rect.colliderect(i.rect) and i.rect.x > game.boss.rect.x + 80:
            game.hero.all_attack.remove(i)
            game.boss.damage(game.hero.attack/3)

    for projectile in game.hero.all_trajectoire:
        projectile.move_trajectoire(screen)
        if game.boss.rect.colliderect(projectile.rect) and projectile.rect.x > game.boss.rect.x + 100:
            game.hero.all_trajectoire.remove(projectile)
            game.boss.damage(game.hero.attack)

    # Création et affichage des attaques du boss
    for i in game.boss.all_attack_boss:
        i.mouv_attack(screen)
        if game.hero.rect.colliderect(i.rect) and time_now - last_hit_hero > invicibility_cooldown:
            game.hero.get_degats = 25

            game.hero.pv -= game.hero.get_degats
            game.hero.get_degats = 0
            last_hit_hero = pg.time.get_ticks()



    # Ensuite, dans votre boucle principale, affichez les cœurs en fonction des PV du héros
    for i in range(game.hero.nombre_coeurs()):
        # Supposons que vous avez une image de cœur chargée et prête à être utilisée
        coeur_image = pg.image.load(keur)
        coeur_image = pg.transform.scale(coeur_image,(70,70))
        coeur_rect = coeur_image.get_rect(topleft=(0 + i * 30, -10))  # Changer la position pour chaque cœur
        screen.blit(coeur_image, coeur_rect)


    if game.hero.rect.colliderect(game.boss.rect) and game.hero.rect.x > game.boss.rect.x:
        game.hero.rect.x -= 200
        if time_now - last_hit_hero > invicibility_cooldown:
            game.hero.get_degats = 25
            last_hit_hero = pg.time.get_ticks()
        game.hero.pv -= game.hero.get_degats
        game.hero.get_degats = 0

    if game.hero.pv <= 0:
        game.hero.death()
        game.hero.start_animation()

    # Mise à jour de la barre de vie
    game.hero.health_bar(screen)
    # Animation lorsque le hero marche
    game.hero.update_animation(game.hero.direction)

    if end:
        time.sleep(5)
        running = False
    if game.boss.animation_end:
        screen.blit(win, (0, 0))
        end = True
    if game.hero.game_over:
        screen.blit(lose, (0, 0))
        end = True
    if time_now - last_attack_boss > beginning_cooldown and beginning:
        beginning = False
    if beginning:
        screen.blit(bg, (0, 0))
        screen.blit(game_keys, (reso_h-192*2, reso_l-124*2))


    # gestion des FPS (Framerate Per Second)
    game.clock.tick(game.fps)
    # Mise à jour de l'affichage
    pg.display.flip()

    clock.tick(30)

# Fermeture de Pygame
pg.quit()
