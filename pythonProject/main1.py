import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')

#set framerate
clock = pygame.time.Clock()
FPS = 60


#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 30
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

#define player action variables
moving_left = False
moving_right = False
is_running = False

#load music and sounds
#pygame.mixer.music.load('audio/music2.mp3')
#pygame.mixer.music.set_volume(0.3)
#pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.05)

def resize_image(image, target_width, target_height):
    return pygame.transform.scale(image, (target_width, target_height))

def run_external_script(script_name):
    os.system(f'python {script_name}')

#load images
#button images
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
#background
bg1 = pygame.image.load('img/Background/bg1.png').convert_alpha()
bg1 = resize_image(bg1,SCREEN_WIDTH, SCREEN_HEIGHT)
bg2 = pygame.image.load('img/Background/bg2.png').convert_alpha()
bg2 = resize_image(bg2,SCREEN_WIDTH, SCREEN_HEIGHT)
bg3 = pygame.image.load('img/Background/bg3.png').convert_alpha()
bg3 = resize_image(bg3,SCREEN_WIDTH, SCREEN_HEIGHT)
bg4 = pygame.image.load('img/Background/bg4.png').convert_alpha()
bg4 = resize_image(bg4,SCREEN_WIDTH, SCREEN_HEIGHT)
bg5 = pygame.image.load('img/Background/bg5.png').convert_alpha()
bg5 = resize_image(bg5,SCREEN_WIDTH, SCREEN_HEIGHT)

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/Tile1/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (235, 65, 54)



#define font
font = pygame.font.SysFont('Futura', 30)




def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_bg():
    screen.fill(BG)
    width = bg5.get_width()
    for x in range(5):
        screen.blit(bg5, ((x * width) - bg_scroll * 0.35, 0))
        screen.blit(bg4, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - bg5.get_height()))
        screen.blit(bg3, ((x * width) - bg_scroll * 0.85, SCREEN_HEIGHT - bg4.get_height()))
        screen.blit(bg2, ((x * width) - bg_scroll * 1.1, SCREEN_HEIGHT - bg3.get_height()))
        screen.blit(bg1, ((x * width) - bg_scroll * 1.35, SCREEN_HEIGHT - bg2.get_height()))


#function to reset level
def reset_level():
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        #ai specific variables
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        #load all images for the players
        animation_types = ['Idle_left','Idle_right', 'Walk_left','Walk_right', 'Run_left','Run_right', 'Jump_left', 'Jump_right']
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = resize_image(img,50,50)
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.update_animation()

    def move(self, moving_left, moving_right):
        #reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_left:
            if is_running:
                dx = -(self.speed * 2)
            else:
                dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            if is_running:
                dx = self.speed * 2
            else:
                dx = self.speed
            self.flip = False
            self.direction = 1


        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #if the ai has hit a wall then make it turn around
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player position
        if self.char_type == 'player':
            if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (
                    world.level_length * TILE_SIZE) - SCREEN_WIDTH) \
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def ai(self):
        if self.idling == False and random.randint(1, 200) == 1:
            self.update_action(0)  #0: idle
            self.idling = True
            self.idling_counter = 50
        #check if the ai in near the player
        if self.vision.colliderect(player.rect):
            #stop running and face the player
            self.update_action(0)  #0: idle

        else:
            if self.idling == False:
                if self.direction == 1:
                    ai_moving_right = True
                else:
                    ai_moving_right = False
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1)  #1: run
                self.move_counter += 1
                #update ai vision as the enemy moves
                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        #scroll
        self.rect.x += screen_scroll

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  #create player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5)

        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

    def draw_object(self):
        for item in collectible_items:
            if not item.collected:  # Vérifie si l'objet n'a pas été ramassé
                screen.blit(item.image, item.rect)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1:  #whole screen fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour,
                             (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour,
                             (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:  #vertical screen fade down
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True

        return fade_complete


#create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

#create buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

#create sprite groups
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


class CollectibleItem(pygame.sprite.Sprite):
    def __init__(self, name, description, position, image):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.description = description
        self.image = image  # Définit l'image de l'objet
        self.rect = self.image.get_rect(
            topleft=position)  # Utilise la position comme coin supérieur gauche du rectangle
        self.collected = False

    def collect(self):
        self.collected = True
        # Actions supplémentaires lors de la collecte, comme jouer un son ou afficher un message


class Inventory:
    def __init__(self):
        self.items = {}
        self.inv_open = False
        self.item_collected = 0

    def add_item(self, item):
        if item.name in self.items:
            self.items[item.name]['quantity'] += 1
        else:
            self.items[item.name] = {'item': item, 'quantity': 1}
    def remove_item(self, item_name):
        if item_name in self.items and self.items[item_name]['quantity'] > 0:
            self.items[item_name]['quantity'] -= 1
            if self.items[item_name]['quantity'] == 0:
                del self.items[item_name]

    def draw_inventory(self):
        # Dessine le fond de l'inventaire
        inventory_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, SCREEN_WIDTH - 100,
                                     60)  # Ajuste les dimensions selon tes besoins
        pygame.draw.rect(screen, (50, 50, 50), inventory_rect)

        # Affiche les objets dans l'inventaire
        start_x = 60  # Position de départ pour le premier objet dans l'inventaire
        for item_name, item_info in inventory.items.items():
            item_icon = item_info['item'].image  # Suppose que chaque objet dans l'inventaire a une image associée
            item_rect = item_icon.get_rect(topleft=(start_x, SCREEN_HEIGHT - 65))

            screen.blit(item_icon, item_rect)  # Dessine l'icône de l'objet


            # Vérifie si la souris est sur cet objet
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                # Affiche la description de l'objet à un emplacement fixe
                draw_description(item_info['item'].description)

            start_x += 50  # Espace entre les objets



inventory = Inventory()


def draw_description(text):
    font = pygame.font.SysFont('arial', 20)  # Choisis la police et la taille
    text_surf = font.render(text, True, (255, 255, 255))  # Crée un surface de texte
    # Définit la position fixe pour la description, ajuste selon tes besoins
    text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))

    # Dessine un fond pour la description (facultatif)
    background_rect = text_rect.inflate(15, 15)  # Un peu plus grand que le texte
    pygame.draw.rect(screen, (0, 0, 0), background_rect)  # Fond noir

    screen.blit(text_surf, text_rect)  # Dessine le texte sur l'écran

def draw_collectibles_counter(item_collected, total_collectibles):
    font = pygame.font.SysFont('arial', 20)  # Choix de la police et de la taille
    text_surf = font.render(f"{item_collected} / {total_collectibles}", True, (255, 255, 255))  # Création d'une surface de texte
    text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))  # Définition de la position

    screen.blit(text_surf, text_rect)  # Dessin du texte sur l'écra

def is_near(player_pos, item_pos, distance=50):
    dx = player_pos[0] - item_pos[0]
    dy = player_pos[1] - item_pos[1]
    distance_between = (dx ** 2 + dy ** 2) ** 0.5
    print(f"Distance entre le joueur et l'objet : {distance_between}")
    return distance_between < distance


#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

collectible_items = []

tile_collectible_mapping = {
    13: {'name': 'Cailloux', 'description': 'Ceci est un beau cailloux qui signe la fonctionnalité de inventaire', 'image': img_list[13]},
    11: {'name': 'moins jolie Caillous', 'description': 'Ceci est un plus petit cailloux et pas tres beau', 'image': img_list[11]},
    # Ajoute d'autres entrées de mapping au besoin
}

total_collectibles = 0
types_ramassables_trouves = set()

# Lecture du Fichier CSV et Création des Objets Ramassables
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile_type in enumerate(row):
            tile_type = int(tile_type)
            if tile_type in tile_collectible_mapping:  # Vérifie si la tuile correspond à un objet ramassable
                types_ramassables_trouves.add(tile_type)
                collectible_info = tile_collectible_mapping[tile_type]
                collectible_item = CollectibleItem(collectible_info['name'], collectible_info['description'], (y * TILE_SIZE, x * TILE_SIZE), collectible_info['image'])
                collectible_items.append(collectible_item)
            else:
                world_data[x][y] = tile_type

total_collectibles = len(types_ramassables_trouves)
world = World()
player = world.process_data(world_data)

run = True
while run:

    clock.tick(FPS)

    if start_game == False:
        #draw menu
        screen.fill(BG)
        #add buttons
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        #update background
        draw_bg()
        #draw world map
        world.draw()
        world.draw_object()

        player.update()
        player.draw()
        if inventory.inv_open:
            inventory.draw_inventory()

        #update and draw groups
        decoration_group.update()
        decoration_group.draw(screen)

        #show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        #update player actions
        if player.alive:
            if player.in_air and player.direction > 0:
                player.update_action(7)  #: jump_R
            elif player.in_air and player.direction < 0:
                player.update_action(6)  #: jump_L
            elif moving_right and is_running:
                player.update_action(5)  #: run_R
            elif moving_left and is_running:
                player.update_action(4)  #: run_L
            elif moving_right:
                player.update_action(3)  #: walk_R
            elif moving_left:
                player.update_action(2)  #: walk_L
            else:
                if player.direction > 0:
                    player.update_action(1)  #: idle_R
                else:
                    player.update_action(0)  #: idle_L
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)
        else:
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    world_data = reset_level()
                    #load in level data and create world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                inventory.inv_open = not inventory.inv_open
                print(inventory.inv_open)
            if not inventory.inv_open:
                if event.key == pygame.K_q:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_SPACE and player.alive:
                    player.jump = True
                    jump_fx.play()
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_a:
                    run_external_script('Album1.py')
                if event.key == pygame.K_p:
                    run_external_script('text1.py')


        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT]:
            if moving_left or moving_right:
                is_running = True
            else:
                is_running = False
        else:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Vérifie la collision pour chaque objet ramassable
                for item in collectible_items:
                    if pygame.sprite.collide_rect(player, item) and not item.collected:
                        inventory.item_collected += 1
                        item.collect()  # Marque l'objet comme ramassé
                        inventory.add_item(item)  # Ajoute l'objet à l'inventaire du joueur
                        print(f"Objet {item.name} ramassé et ajouté à l'inventaire")

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    draw_collectibles_counter(inventory.item_collected, total_collectibles)

    pygame.display.update()

pygame.quit()
