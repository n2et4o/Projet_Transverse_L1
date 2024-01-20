import pygame as pg
pg.init()

# fenetre du jeu
pg.display.set_caption("storm Grief")
screen = pg.display.set_mode((1080,720))
background = pg.image.load("Image_du_jeu/Background.jpg")


#boucle du jeu
running = True
while running == True :
    for events in pg.event.get(): # event est une liste, events est un élèment de cette liste

        #Affichage de l'arrière plan
        screen.blit(background, (250, 200))
        pg.display.flip()

        #fermeture de la fenetre
        if events.type == pg.QUIT :
            running = False
            pg.quit()
