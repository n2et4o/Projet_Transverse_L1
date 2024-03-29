import pygame as pg
from pygame import Surface, SurfaceType

from fonctions import *

# Initialisation de Pygame
pg.init()

# Fenêtre du jeu
pg.display.set_caption("Winter Grief")
reso_h = 1280
reso_l = 720
screen = pg.display.set_mode((reso_h, reso_l))
background_path = trouver_image("new_background.png")
background = pg.image.load(background_path)
background = pg.transform.scale(background,(reso_h,reso_l))

# Chargement du jeu
game = Game()

at = trouver_image("hero's_attack.png")

# Temps entre chaque attaque du hero
temps_de_pause = 0.1

# Boucle du jeu
running = True
while running:
    # Initilisation de t1
    game.hero.t1 = time.time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Pression sur une touche
        elif event.type == pg.KEYDOWN:
            game.pressed[event.key] = True

            # Pression sur la touche d'attaque
            if game.pressed.get(pg.K_a) and game.hero.can_attack(temps_de_pause):
                first = game.hero.image
                game.hero.image = pg.image.load(at)
                game.hero.image = pg.transform.scale(game.hero.image, (150, 150))
                game.hero.Attack()

                # Initialisation de t2
                game.hero.t2 = time.time()  # Mise à jour de t2 après l'attaque

            if event.key == pg.K_t and game.hero.can_attack(temps_de_pause):
                print("Touche T pressée")
                try:
                    nouveau_projectile = Trajectoire_hero(game.hero)
                    game.hero.all_trajectoire.add(nouveau_projectile)
                    game.hero.t2 = time.time()  # Mise à jour de t2 après l'attaque
                    print("Projectile ajouté avec succès")
                except Exception as e:
                    print(f"Erreur lors de l'ajout du projectile: {e}")

            # Pression sur la touche (up) pour effectuer un saut
            if event.key == pg.K_UP :
                game.hero.jumped = True
                game.hero.nb_jump += 1
                if game.hero.rect.y == 0:
                    game.hero.jumped = False
            # Pression sur la touche (down) pour descendre des plateformes et descente du sol
            if event.key == pg.K_DOWN and game.hero.rect.y <= 560:
                game.resistance = 0

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False

    # Vérification que la touche est pressée et que le hero ne sorte pas du cadre de l'écran
    if game.pressed.get(pg.K_RIGHT) and game.hero.rect.x + game.hero.rect.width < screen.get_width():
        game.hero.move_right()
        game.hero.direction = 1
    elif game.pressed.get(pg.K_LEFT) and game.hero.rect.x > 0:
        game.hero.move_left()
        game.hero.direction = -1

    # Test du delta_temps
    #game.hero.deltas(game.hero.t1,game.hero.t2,game.hero.delta_temps)

    # Application de gravite
    game.application_gravite()

    # Affichage de l'arrière-plan
    screen.blit(background, (0, 0))

    # Affichage du sol
    game.ground.afficher_sol(screen)

    # Affichage du boss
    screen.blit(game.boss.image,game.boss.rect)

    # Mise à jour de la barre de vie du Boss
    game.boss.update_health_bar(screen)

    # Affichage du héros
    screen.blit(game.hero.image, game.hero.rect)

    # Affichage de l'attaque
    game.hero.all_attack.draw(screen)
    game.hero.all_trajectoire.draw(screen)

    # Boucle d'affichage du projectile
    for i in game.hero.all_attack:
        i.mouv_attack(screen)

    for projectile in game.hero.all_trajectoire:
        projectile.move_trajectoire(screen)

    # Création et affichage des plateformes
    for rectangle in game.list_platform:
        platform = Ground_up(rectangle)
        game.platform_group.add(platform)
        # Conditions pour marcher sur la plateforme
        if game.hero.rect.midbottom[1] // 10 * 10 == platform.rect.top and game.hero.rect.colliderect(rectangle):
            game.resistance = -10
            game.hero.nb_jump = 0

    for platform in game.platform_group:
        platform.afficher_platform(screen)

    # Mise à jour de la barre de vie
    game.hero.health_bar(screen)

    pg.draw.rect(screen,(0,0,0),game.rect_limite,1)

    # Génerer les contours de l'écran pour definir les bordures
    #pg.draw.rect(screen,(0,0,0),game.rect_limite,1)

    game.clock.tick(game.fps)
    # Mise à jour de l'affichage
    pg.display.flip()


#hope this shit works
# Fermeture de Pygame
pg.quit()