import pygame
import sys

pygame.init()

screen_width = 1280
screen_height = 720

pause = False
sound_enabled = True

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")
fond = pygame.image.load(r"C:\Users\bench\Desktop\Winter Grief\bg_2-2.jpg")
fond = pygame.transform.scale(fond, (1280, 720))

play = pygame.image.load(r"C:\Users\bench\Desktop\Winter Grief\button_play_-2_surbrillance.jpg")

# Chargez votre image pour le menu pause
pause_menu_image = pygame.image.load(r"C:\Users\bench\Desktop\Winter Grief\R.jpg").convert_alpha()
pause_menu_image = pygame.transform.scale(pause_menu_image, (screen_width, screen_height))

# Couleur semi-transparente pour l'assombrissement
overlay_color = (0, 0, 0, 200)  # Noir avec une opacité de 75%

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause  # Inverser l'état de pause
        if event.type == pygame.QUIT:
            run = False
            sys.exit()

    if not pause:
        # Afficher l'écran du jeu normal
        screen.blit(fond, (0, 0))
        screen.blit(play, (435, 170))
    else:
        # Afficher le menu pause
        screen.blit(pause_menu_image, (0, 0))
        # Superposer un rectangle semi-transparent sur l'image pour l'assombrir
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill(overlay_color)
        screen.blit(overlay, (0, 0))

    pygame.display.update()

pygame.quit()