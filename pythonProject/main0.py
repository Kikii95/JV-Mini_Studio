# main0_fixed.py — version corrigée et portable (paths/chargements/sons/polices/CSV)
import pygame
from pygame import mixer
import os
import sys
import csv
import random
import subprocess
from pathlib import Path
import button

# === Répertoires ===
BASE_DIR = Path(__file__).resolve().parent
ASSETS   = BASE_DIR / "img"
AUDIO    = BASE_DIR / "audio"
FONTS    = BASE_DIR / "fonts"
LEVELS   = BASE_DIR  # CSV au même niveau que ce fichier

# === Init ===
mixer.init()
pygame.init()

SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('pythonProject/Game')

clock = pygame.time.Clock()
FPS = 60

# === Variables du jeu ===
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 30
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 0
start_game = False
start_intro = False

# === Actions joueur ===
moving_left = False
moving_right = False
is_running = False
gliding = False

# === Utils ===
def resize_image(image, target_width, target_height):
    return pygame.transform.scale(image, (int(target_width), int(target_height)))

def run_external_script(script_name):
    """Exécute un script Python situé à côté de ce fichier (BASE_DIR/script_name)."""
    p = (BASE_DIR / script_name).resolve()
    if p.exists():
        subprocess.Popen([sys.executable, str(p)])
    else:
        print(f"[WARN] Script introuvable: {p}")

def load_sound_safe(pathlike, volume=0.05):
    try:
        s = pygame.mixer.Sound(str(pathlike))
        s.set_volume(volume)
        return s
    except Exception as e:
        print(f"[INFO] Son optionnel non chargé ({pathlike}): {e}")
        return None

def get_font(size=30, ttf_name=None, fallback_name=None):
    """Charge une police TTF depuis FONTS si fournie, sinon SysFont avec fallback."""
    if ttf_name:
        p = FONTS / ttf_name
        if p.exists():
            return pygame.font.Font(str(p), size)
    if fallback_name:
        return pygame.font.SysFont(fallback_name, size)
    return pygame.font.SysFont(None, size)

# === Musique / Sons (optionnels) ===
# pygame.mixer.music.load(str(AUDIO / 'music2.mp3'))
# pygame.mixer.music.set_volume(0.3)
# pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = load_sound_safe(AUDIO / 'jump.wav', volume=0.05)

# === Images UI ===
start_img   = pygame.image.load(str(ASSETS / 'start_btn.png')).convert_alpha()
exit_img    = pygame.image.load(str(ASSETS / 'exit_btn.png')).convert_alpha()
restart_img = pygame.image.load(str(ASSETS / 'restart_btn.png')).convert_alpha()

# === Backgrounds ===
BG_DIR = ASSETS / 'Background' / 'Bg_1'
bg1 = pygame.image.load(str(BG_DIR / 'bg1.png')).convert_alpha()
bg1 = resize_image(bg1, 2/3 * SCREEN_WIDTH, 4/5 * SCREEN_HEIGHT)

bg2 = pygame.image.load(str(BG_DIR / 'bg2.png')).convert_alpha()
bg2 = resize_image(bg2, 2/3 * SCREEN_WIDTH, 4/5 * SCREEN_HEIGHT)

bg3 = pygame.image.load(str(BG_DIR / 'bg3.png')).convert_alpha()
bg3 = resize_image(bg3, 2/3 * SCREEN_WIDTH, 4/5 * SCREEN_HEIGHT)

bg4 = pygame.image.load(str(BG_DIR / 'bg4.png')).convert_alpha()
bg4 = resize_image(bg4, 2/3 * SCREEN_WIDTH, 4/5 * SCREEN_HEIGHT)

bg5 = pygame.image.load(str(BG_DIR / 'bg5.png')).convert_alpha()
bg5 = resize_image(bg5, 2/3 * SCREEN_WIDTH, SCREEN_HEIGHT)

# === Tiles ===
img_list = []
tile_dir = ASSETS / 'Tile0'
for x in range(TILE_TYPES):
    p = tile_dir / f"{x}.png"
    if not p.exists():
        raise FileNotFoundError(f"Tuile manquante: {p}")
    img = pygame.image.load(str(p)).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# === Couleurs ===
BG    = (144, 201, 120)
RED   = (255,   0,   0)
WHITE = (255, 255, 255)
GREEN = (  0, 255,   0)
BLACK = (  0,   0,   0)
PINK  = (235,  65,  54)

button_activated = False

# === Fonts ===
# Tente Futura.ttf locale, sinon Futura système, sinon fallback neutre
font = get_font(30, ttf_name='Futura.ttf', fallback_name='Futura')
ui_font_small = get_font(20, fallback_name='Arial')

def draw_text(text, font_obj, text_col, x, y):
    img = font_obj.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    offset = 70
    width = bg5.get_width()
    for i in range(5):
        screen.blit(bg5, ((i * width) - bg_scroll * 0.35, 0))
        screen.blit(bg4, ((i * width) - bg_scroll * 0.6,  (2/3 * SCREEN_HEIGHT - (bg5.get_height() - 2*offset)) + offset))
        screen.blit(bg3, ((i * width) - bg_scroll * 0.85, (2/3 * SCREEN_HEIGHT - bg4.get_height()) + offset))
        screen.blit(bg2, ((i * width) - bg_scroll * 1.1,  (2/3 * SCREEN_HEIGHT - bg3.get_height()) + offset))
        screen.blit(bg1, ((i * width) - bg_scroll * 1.35, (2/3 * SCREEN_HEIGHT - bg2.get_height()) + offset))

# === Reset level ===
def reset_level():
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    data = []
    for _ in range(ROWS):
        data.append([-1] * COLS)
    return data

# === Classes ===
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        super().__init__()
        self.alive = True
        self.char_type = char_type  # ex: 'player'
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
        # AI
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling = False
        self.idling_counter = 0

        animation_types = ['Idle_left','Idle_right','Walk_left','Walk_right',
                           'Run_left','Run_right','Jump_left','Jump_right','Glide_left','Glide_right']
        for animation in animation_types:
            temp_list = []
            anim_dir = ASSETS / self.char_type / animation
            if not anim_dir.exists():
                raise FileNotFoundError(f"Répertoire d'animation manquant: {anim_dir}")
            # trie numérique: 0.png, 1.png, ...
            frames = sorted([p for p in anim_dir.iterdir() if p.suffix.lower()=='.png'],
                            key=lambda p: int(p.stem))
            for frame in frames:
                img = pygame.image.load(str(frame)).convert_alpha()
                img = resize_image(img, 50, 50)
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
        global screen_scroll
        screen_scroll = 0
        dx, dy = 0, 0

        if moving_left:
            dx = -(self.speed * 2) if is_running else -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = (self.speed * 2) if is_running else self.speed
            self.flip = False
            self.direction = 1

        # Saut
        if self.jump and not self.in_air:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        # Glide
        if gliding:
            self.vel_y += GRAVITY * dy
            self.rect.y += self.vel_y
            self.vel_y *= 0.3
            self.rect.x += self.direction * 300 * dy

        # Gravité
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Collisions
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                else:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        # Sortie
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        # Bords écran (player)
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # Mise à jour
        self.rect.x += dx
        self.rect.y += dy

        # Scroll
        if self.char_type == 'player':
            if ((self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx))):
                self.rect.x -= dx
                screen_scroll = -dx

        return screen_scroll, level_complete

    def ai(self):
        if not self.idling and random.randint(1, 200) == 1:
            self.update_action(0)  # idle
            self.idling = True
            self.idling_counter = 50

        if self.vision.colliderect(player.rect):
            self.update_action(0)  # idle face au joueur
        else:
            if not self.idling:
                ai_moving_right = self.direction == 1
                ai_moving_left = not ai_moving_right
                self.move(ai_moving_left, ai_moving_right)
                self.update_action(1)  # run
                self.move_counter += 1
                self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                if self.move_counter > TILE_SIZE:
                    self.direction *= -1
                    self.move_counter *= -1
            else:
                self.idling_counter -= 1
                if self.idling_counter <= 0:
                    self.idling = False

        self.rect.x += screen_scroll

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect)

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if 0 <= tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif 11 <= tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:  # create player
                        player = Soldier('player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5)
        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

    def draw_object(self):
        for item in collectible_items:
            if not item.collected and item.name != 'Secret_Path':
                screen.blit(item.image, item.rect)

    def draw_secretpath(self):
        for item in collectible_items:
            if not button_activated:
                screen.blit(item.image, item.rect)

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class SecretPath(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
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
        if self.direction == 1:
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.colour, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.direction == 2:
            pygame.draw.rect(screen, self.colour, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))
        if self.fade_counter >= SCREEN_WIDTH:
            fade_complete = True
        return fade_complete

# === Fades & Boutons ===
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

start_button   = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button    = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50,  exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50,  restart_img, 2)

# === Groupes ===
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

class CollectibleItem(pygame.sprite.Sprite):
    def __init__(self, name, description, position, image):
        super().__init__()
        self.name = name
        self.description = description
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.collected = False
        self.start_pos = position

    def update(self, scroll):
        if not self.collected:
            self.rect.x = self.start_pos[0] + scroll

    def collect(self):
        self.collected = True

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
        inventory_rect = pygame.Rect(50, SCREEN_HEIGHT - 70, SCREEN_WIDTH - 100, 60)
        pygame.draw.rect(screen, (50, 50, 50), inventory_rect)
        start_x = 60
        for _, item_info in inventory.items.items():
            item_icon = item_info['item'].image
            item_rect = item_icon.get_rect(topleft=(start_x, SCREEN_HEIGHT - 65))
            screen.blit(item_icon, item_rect)
            if item_rect.collidepoint(pygame.mouse.get_pos()):
                draw_description(item_info['item'].description)
            start_x += 50

inventory = Inventory()

def draw_description(text):
    text_surf = ui_font_small.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    background_rect = text_rect.inflate(15, 15)
    pygame.draw.rect(screen, (0, 0, 0), background_rect)
    screen.blit(text_surf, text_rect)

def draw_collectibles_counter(item_collected, total_collectibles):
    text_surf = ui_font_small.render(f"{item_collected} / {total_collectibles}", True, (255, 255, 255))
    text_rect = text_surf.get_rect(topright=(SCREEN_WIDTH - 20, 20))
    screen.blit(text_surf, text_rect)

def is_near(player_pos, item_pos, distance=50):
    dx = player_pos[0] - item_pos[0]
    dy = player_pos[1] - item_pos[1]
    distance_between = (dx ** 2 + dy ** 2) ** 0.5
    print(f"Distance entre le joueur et l'objet : {distance_between}")
    return distance_between < distance

# === World data vide ===
world_data = [[-1] * COLS for _ in range(ROWS)]
collectible_items = []

# Mapping tuiles → objets
tile_collectible_mapping = {
    13: {'name': 'Cailloux', 'description': 'Beau caillou pour tester l’inventaire', 'image': img_list[13]},
    18: {'name': 'Button',  'description': 'Petit caillou pas très beau',          'image': img_list[18]},
    14: {'name': 'moins jolie Caillous', 'description': 'Encore un plus petit caillou', 'image': img_list[14]},
    12: {'name': 'Secret_Path', 'description': '', 'image': img_list[12]},
}

total_collectibles = 0
types_ramassables_trouves = set()

# === Lecture CSV niveau initial ===
csv_path = LEVELS / f'level{level}_data.csv'
with open(str(csv_path), newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x_idx, row in enumerate(reader):
        for y_idx, tile_type in enumerate(row):
            tile_type = int(tile_type)
            if tile_type in tile_collectible_mapping:
                types_ramassables_trouves.add(tile_type)
                info = tile_collectible_mapping[tile_type]
                collectible_item = CollectibleItem(info['name'], info['description'],
                                                   (y_idx * TILE_SIZE, x_idx * TILE_SIZE),
                                                   info['image'])
                collectible_items.append(collectible_item)
            else:
                world_data[x_idx][y_idx] = tile_type

total_collectibles = len(types_ramassables_trouves)
world = World()
player = world.process_data(world_data)

# === Fades ===
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, PINK, 4)

run = True
while run:
    clock.tick(FPS)
    current_fps = clock.get_fps()
    fps_text = f"FPS: {int(current_fps)}"

    if start_game:
        for item in collectible_items:
            item.update(-bg_scroll)

    if not start_game:
        screen.fill(BG)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False
    else:
        draw_bg()
        world.draw()
        world.draw_object()

        player.update()
        player.draw()
        world.draw_secretpath()

        if inventory.inv_open:
            inventory.draw_inventory()

        decoration_group.update()
        decoration_group.draw(screen)

        if start_intro:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0

        if player.alive:
            if gliding and player.direction > 0:
                player.update_action(9)   # Glide_right
            if gliding and player.direction < 0:
                player.update_action(8)   # Glide_left
            if player.in_air and not gliding and player.direction > 0:
                player.update_action(7)   # Jump_right
            elif player.in_air and not gliding and player.direction < 0:
                player.update_action(6)   # Jump_left
            elif moving_right and is_running:
                player.update_action(5)   # Run_right
            elif moving_left and is_running:
                player.update_action(4)   # Run_left
            elif moving_right:
                player.update_action(3)   # Walk_right
            elif moving_left:
                player.update_action(2)   # Walk_left
            else:
                if player.direction > 0:
                    player.update_action(1)  # Idle_right
                else:
                    player.update_action(0)  # Idle_left

            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll

            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    csv_next = LEVELS / f'level{level}_data.csv'
                    with open(str(csv_next), newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x_idx, row in enumerate(reader):
                            for y_idx, tile in enumerate(row):
                                world_data[x_idx][y_idx] = int(tile)
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
                    csv_cur = LEVELS / f'level{level}_data.csv'
                    with open(str(csv_cur), newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x_idx, row in enumerate(reader):
                            for y_idx, tile in enumerate(row):
                                world_data[x_idx][y_idx] = int(tile)
                    world = World()
                    player = world.process_data(world_data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                run_external_script('Album0.py')
            if event.key == pygame.K_p:
                run_external_script('text0.py')
            if event.key == pygame.K_e:
                inventory.inv_open = not inventory.inv_open
                print("Inventory open:", inventory.inv_open)

            if not inventory.inv_open:
                if event.key == pygame.K_q:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_SPACE and player.alive:
                    player.jump = True
                    if jump_fx:
                        jump_fx.play()
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_SPACE and player.in_air:
                    if (moving_left or moving_right):
                        gliding = True
                    else:
                        gliding = False
                else:
                    gliding = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT]:
            is_running = moving_left or moving_right
        else:
            is_running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                for item in collectible_items:
                    if pygame.sprite.collide_rect(player, item) and not item.collected and item.name != 'Button':
                        inventory.item_collected += 1
                        item.collect()
                        inventory.add_item(item)
                        print(f"Objet {item.name} ramassé et ajouté à l'inventaire")
                    if pygame.sprite.collide_rect(player, item) and item.name == 'Button':
                        button_activated = True
                        print("Bouton activé:", button_activated)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    draw_collectibles_counter(inventory.item_collected, total_collectibles)
    draw_text(fps_text, font, BLACK, 150, 120)
    pygame.display.update()

pygame.quit()
