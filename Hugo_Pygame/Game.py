import pygame, sys, os
class Animation(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.attack_animation = False
        self.sprites = []
        for i in range (1, 13):
            img = pygame.image.load(f'Explosion/{i}.png')
            img = pygame.transform.scale(img, (50, 50))
            self.sprites.append(img)
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def attack(self):
        self.attack_animation = True

    def update(self,speed):
        if self.attack_animation == True:
            self.current_sprite += speed
            if int(self.current_sprite) >= len(self.sprites):
                self.current_sprite = 0
                self.attack_animation = False
                self.kill()
        self.image = self.sprites[int(self.current_sprite)]

class Player(object):
    def __init__(self):
        """ The constructor of the class """
        self.image = img_path2
        self.x = 0
        self.y = 350
        self.attack = False

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 10
        if key[pygame.K_DOWN]:
            self.y += dist 
        elif key[pygame.K_UP]: 
            self.y -= dist 
        if key[pygame.K_RIGHT]:
            self.x += dist 
        elif key[pygame.K_LEFT]: 
            self.x -= dist 
        if key[pygame.K_SPACE]: 
            self.attack = True

    def draw(self, surface):
        """ Draw on surface """
        surface.blit(self.image, (self.x, self.y))


    def draw(self, surface):
        """ Draw on surface """
        surface.blit(self.image, (self.x, self.y))
    
def pause (paused):
        resume_button_img = pygame.image.load('img\Play_Long.png')
        quit_button_img = pygame.image.load('img\Play_Long.png')
        main_menu_button_img = pygame.image.load('img\home.png')
        bg = pygame.image.load("img\Background.png")
        Window = pygame.image.load("img\Big.png")
        
        button_width_large, button_height_large = resume_button_img.get_size()
        button_width, button_height = main_menu_button_img.get_size()
        
        button_x = (screen_width - button_width_large) / 2
        button_mini = (screen_width - button_width) / 2
        
        resume_button_y = (screen_height - button_height_large * 3) / 2
        quit_button_y = resume_button_y + button_height_large
        main_menu_button_y = quit_button_y + button_height 

        resume_button = resume_button_img.get_rect(topleft=(button_x, resume_button_y))
        quit_button = quit_button_img.get_rect(topleft=(button_x, quit_button_y))
        main_menu_button = main_menu_button_img.get_rect(topleft=(button_mini, main_menu_button_y))

        screen.blit(bg, (0, 0))
        screen.blit(Window, (screen_width / 2 - Window.get_width() / 2, screen_height / 2.2 - Window.get_height() / 2))
        screen.blit(resume_button_img, resume_button)
        screen.blit(quit_button_img, quit_button)
        screen.blit(main_menu_button_img, main_menu_button)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if resume_button.collidepoint(event.pos):
                paused = False
                return paused
            elif quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            elif main_menu_button.collidepoint(event.pos):
                # À Mettre ici le code pour retourner au menu principal
                pass

img_path = pygame.image.load("img\Player.png")
img_path2 = pygame.transform.scale_by(img_path,0.3)
img_path3 = pygame.transform.rotate(img_path,180)
Background = pygame.image.load("img\Background.jpeg")

pygame.init()
paused = False
player = Player() 
clock = pygame.time.Clock()
moving_sprites = pygame.sprite.Group()

screen_width = 1228
screen_height = 694
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

# Main game loop
while True:
    screen.blit(Background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # p pour pause/ unpause
                paused = not paused
    if paused==True:
        pause(paused)
        if pause(paused)==False:
            paused = False
    else: # Le jeu n'est pas en pause 
        player.handle_keys() 
        if player.attack:
            animation = Animation(player.x,player.y)
            animation.attack()
            moving_sprites.add(animation)
            player.attack = False
        moving_sprites.draw(screen)
        player.draw(screen) 
        moving_sprites.update(0.25)
    pygame.display.update() 
    pygame.display.flip()
    clock.tick(60)