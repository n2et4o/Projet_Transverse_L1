#game.hero.jumpe()
    # elif game.pressed.get(pg.K_UP) and game.hero.rect.y > 0:
    #    game.hero.move_up()
    # elif game.pressed.get(pg.K_DOWN) and game.hero.rect.y < screen.get_height() - 150:
    #   game.hero.move_down()

# Exemple pour un bouton (le bouton X de la PS5 pour sauter)
 #   if joystick.get_button(1):  # Supposons que le bouton 1 soit le bouton X
  #      game.hero.jumped = True
   #     game.hero.nb_jump += 1
    #    if game.hero.rect.y == 0:
     #       game.hero.jumped = False

"""    for heart in game.heart_list:
        hearts = Heart(heart)
        game.heart_groupe.add(hearts)
        if game.hero.rect.colliderect(game.boss.rect) and game.hero.rect.x > game.boss.rect.x :
            game.hero.rect.x -= 150
            game.hero.get_degats = 5
            game.hero.pv -= game.hero.get_degats
            game.hero.get_degats = 0
            if game.hero.pv == 75:
                game.heart_groupe.remove(hearts)

    for hearts in game.heart_groupe:
        hearts.display_heart(screen)"""


"""class Heart(pg.sprite.Sprite):
    def __init__(self,rect):
        super().__init__()
        self.rect = rect

    def display_heart(self,surface):
        pg.draw.rect(surface,(0,255,0), self.rect)"""

""" self.heart_groupe = Group()
        self.heart_list = [
            pg.Rect(25,10,10,50),pg.Rect(50,10,10,50),pg.Rect(75,10,10,50),pg.Rect(100,10,10,50)
        ]"""