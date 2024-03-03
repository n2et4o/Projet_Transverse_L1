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
            if game.pressed.get(pg.K_a):
                first = game.hero.image
                game.hero.image = pg.image.load(at)
                game.hero.image = pg.transform.scale(game.hero.image, (150, 150))
                game.hero.Attack()
                #game.hero.image = first
            # Pression sur la touche (up) pour effectuer un saut
            if event.key == pg.K_UP :
                game.hero.jumped = True
                game.hero.nb_jump += 1
                if game.hero.rect.y == 0:
                    game.hero.jumped = False

        elif event.type == pg.KEYUP:
            game.pressed[event.key] = False


    # Vérification que la touche est pressée et que le hero ne sorte pas du cadre de l'écran
    if game.pressed.get(pg.K_RIGHT) and game.hero.rect.x + game.hero.rect.width < screen.get_width():
        game.hero.move_right()
        game.hero.direction = 1
    elif game.pressed.get(pg.K_LEFT) and game.hero.rect.x > 0:
        game.hero.move_left()
        game.hero.direction = -1


    #game.hero.rect.clamp_ip(game.hero.rect)

    # Application de gravite
    game.application_gravite()

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
        i.mouv_attack(screen)
        #i.health_bar(screen)

    # Création et affichage du des platformes
    for rectangle in game.list_platform:
        platform = Ground_up(rectangle)
        game.platform_group.add(platform)
        # Conditions pour marcher la platforme
        if game.hero.rect.midbottom[1] // 10 * 10 == platform.rect.top and game.hero.rect.colliderect(rectangle):
            game.resistance = -10
            game.hero.nb_jump = 0

    for platform in game.platform_group:
        platform.afficher_platform(screen)

    # Mise à jour de la barre de vie
    game.hero.health_bar(screen)



    # Génerer les contours de l'écran pour definir les bordures
    #pg.draw.rect(screen,(0,0,0),game.rect_limite,1)

    #game.clock.tick(game.fps)
    # Mise à jour de l'affichage
    pg.display.flip()

# Fermeture de Pygame
pg.quit()
