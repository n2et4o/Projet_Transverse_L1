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

"""
# Vérification de collision pour la collecte du bonus
    # Dans la boucle principale de votre jeu
    for bonus in game.bonus.all_bonuses:  # Supposant que vous avez un groupe all_bonuses
        if game.hero.rect.colliderect(bonus.rect) and not bonus.hidden:
            bonus.collect(game.hero)
"""

"""
class Bonus(pygame.sprite.Sprite):
    def __init__(self, image_path, platforms, boss, screen_rect):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.platforms = platforms  # Liste ou Groupe de sprites des plateformes
        self.boss = boss  # Référence à l'objet Sprite du boss
        self.screen_rect = screen_rect  # Rectangle de la zone de jeu pour contraindre le bonus
        self.hide()

    def hide(self):
        self.hidden = True
        self.rect.x = -100  # Déplace le bonus hors de l'écran
        self.rect.y = -100
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        # Réapparaît après un certain délai
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > self.reappear_delay:
            self.reappear()

    def reappear(self):
        valid_position = False
        while not valid_position:
            # Générer une position aléatoire dans la zone de jeu
            self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
            self.rect.y = random.randint(0, self.screen_rect.height - self.rect.height)

            # Vérifie si le bonus n'est pas sur le boss ou une plateforme
            if not pygame.sprite.collide_rect(self, self.boss):
                for platform in self.platforms:
                    if self.rect.colliderect(platform.rect):
                        self.rect.bottom = platform.rect.top  # Assurez que le bonus atterrisse sur la plateforme
                        valid_position = True
                        break
                else:  # Si le bonus n'est pas sur une plateforme, vérifiez s'il est au sol
                    if self.rect.bottom >= self.screen_rect.height:
                        self.rect.bottom = self.screen_rect.height
                        valid_position = True

        self.hidden = False

    def collect(self, hero):
        # Ajoute une vie au héros, puis cache le bonus
        hero.add_life()
        self.hide()
"""

"""# Charger l'image du bonus
bonus = Bonus(reso_h, reso_l, bonous)

# Groupe de sprites pour gérer l'affichage et les mises à jour
all_sprites = pygame.sprite.Group()
all_sprites.add(bonus)"""

"""# Mettre à jour les éléments du jeu
    all_sprites.update()
    if not bonus.hidden:
        screen.blit(bonus.image, bonus.rect)"""

#""" "death": load_animate_image("death") ""

"""if self.hero.pv == 0:
            self.images = dict_animation.get("death")
        self.animation = False """

"""if sprite_name == "death":
        path = f"Image_du_jeu/{sprite_name}/" """