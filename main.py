import pygame as pg
from fonctions import *
# Initialisation de Pygame
pg.init()

# Fenêtre du jeu
pg.display.set_caption("storm Grief")
screen = pg.display.set_mode((1080, 720))
background = pg.image.load("Image_du_jeu/Background.png")

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
        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False

    # Vérification que la touche est pressée et que le hero ne sorte pas du cadre de l'écran
    if game.pressed.get(pg.K_RIGHT) and game.hero.rect.x + game.hero.rect.width < screen.get_width() +130:
        game.hero.move_right()
    elif game.pressed.get(pg.K_LEFT) and game.hero.rect.x > -50:
        game.hero.move_left()

    # Affichage de l'arrière-plan
    screen.blit(background, (0, 0))

    # Affichage du héros
    screen.blit(game.hero.image, game.hero.rect)

    # Mise à jour de l'affichage
    pg.display.flip()

# Fermeture de Pygame
pg.quit()
