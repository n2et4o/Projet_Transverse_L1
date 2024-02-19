import pygame as pg
from fonctions import *

# Initialisation de Pygame
pg.init()

# Fenêtre du jeu
pg.display.set_caption("storm Grief")
screen = pg.display.set_mode((1080, 720))
background = pg.image.load("Image_du_jeu/new_background.png")

# Chargement du jeu
game = Game()

# Boucle du jeu
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # Pression sur une touche
        elif event.type == pg.KEYDOWN:
            game.pressed[event.key] = True

            # Pression sur la touche d'attaque
            if event.key == pg.K_a:
                game.hero.Attack()
            # Pression sur la touche (up) pour effectuer un saut
            if event.key == pg.K_j and game.hero.rect.y != 0:
                game.hero.jumped = True
                game.hero.nb_jump += 1
                if game.hero.rect.y == 0:
                    game.hero.jumped = False

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False

    # Vérification que la touche est pressée et que le hero ne sorte pas du cadre de l'écran
    if game.pressed.get(pg.K_RIGHT) and game.hero.rect.x + game.hero.rect.width < screen.get_width():
        game.hero.move_right()
    elif game.pressed.get(pg.K_LEFT) and game.hero.rect.x > 0:
        game.hero.move_left()

    game.hero.rect.clamp_ip(game.hero.rect)
    # Application de gravite

    game.application_gravite()

    #game.hero.jumpe()
    # elif game.pressed.get(pg.K_UP) and game.hero.rect.y > 0:
    #    game.hero.move_up()
    # elif game.pressed.get(pg.K_DOWN) and game.hero.rect.y < screen.get_height() - 150:
    #   game.hero.move_down()

    # Affichage de l'arrière-plan
    screen.blit(background, (0, 0))

    game.ground.afficher_sol(screen)
    #game.plac.afficher_sol_up(screen)

    # Affichage du héros
    screen.blit(game.hero.image, game.hero.rect)

    # Affichage de l'attaque
    game.hero.all_attack.draw(screen)

    # Boucle d'affichage du projectile
    for i in game.hero.all_attack:
        i.mouv_attack()
        # i.health_bar(screen)

    # Mise à jour de la barre de vie
    game.hero.health_bar(screen)

    pg.draw.rect(screen,(0,0,0),game.rect_limite,1)

    game.clock.tick(game.fps)
    # Mise à jour de l'affichage
    pg.display.flip()

# Fermeture de Pygame
pg.quit()
