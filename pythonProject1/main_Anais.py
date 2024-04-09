import os
import pygame

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")

# set frame
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75

# define player action variables
moving_left = False
moving_right = False

# define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Class for the object
class Object:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


objet = Object(400, 250, 50)


# Class for the NPC object
class NPC:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)


class FlowerSeed:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = pygame.image.load("img/player/Walk/0.png").convert_alpha()  # (a modifier avec la graine)
        self.planted = False  # (la graine n'est pas arrosée)
        self.growing = False  # (pour lancer l'animation)
        self.animation_frames = []
        self.animation_index = 0
        self.animation_speed = 0.1  # Speed of animation
        self.pickable = False

        # Load animation frames for flower growth
        for i in range(8):
            frame = pygame.image.load(f"img/player/Walk/{i}.png").convert_alpha()
            self.animation_frames.append(pygame.transform.scale(frame, (50, 50)))

    def draw(self):
        if not self.planted:
            screen.blit(self.image, self.rect)
        elif self.growing:
            if self.animation_index < len(self.animation_frames):
                screen.blit(self.animation_frames[int(self.animation_index)], self.rect)
            # else:
                # self.pickable = True  Once animation is finished, flower becomes pickable

    def update_animation(self):
        if self.growing:
            self.animation_index += 1 * self.animation_speed
            if self.animation_index >= len(self.animation_frames):
                self.animation_index = len(self.animation_frames) - 1


# Function to display text on the screen
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# Font initialization
font = pygame.font.SysFont(None, 40)


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


class Player(pygame.sprite.Sprite):
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

        # load all images for the payers
        animation_types = ["Idle", "Run", "Jump"]
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0

        # assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 100
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out the reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Function to display text on the screen dynamic
def draw_text_dynamic(text, font, color, x, y, delay=50):
    rendered_text = ""
    for i in range(len(text) + 1):
        rendered_text = text[:i]
        img = font.render(rendered_text, True, color)
        screen.blit(img, (x, y))
        pygame.display.flip()
        pygame.time.wait(delay)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return


player = Player("player", 200, 200, 0.1, 5)
npc = NPC(600, 200, 50, 100)
flower_seed = FlowerSeed(200, 250)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()
    objet.draw()
    npc.draw()
    flower_seed.draw()

    # Check for interactions with the object
    if player.rect.colliderect(objet.rect):
        if pygame.key.get_pressed()[pygame.K_f]:
            draw_text("Oui grgrgegeg", font, RED, 400, 100)

    # Check for interactions with the NPC
    if player.rect.colliderect(npc.rect):
        if pygame.key.get_pressed()[pygame.K_f]:
            draw_text_dynamic("Hihihii oui oui il elle ah", font, RED, 100, 150)

    # Check for interactions with the flower seed
    if not flower_seed.planted and player.rect.colliderect(flower_seed.rect):
        if pygame.key.get_pressed()[pygame.K_f]:
            # if player.has_watering_can:
                flower_seed.planted = True
                flower_seed.growing = True

    flower_seed.update_animation()

    # update player actions
    if player.alive:
        if player.in_air:
            player.update_action(2)  # 2: jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1: run
        else:
            player.update_action(0)  # 0: idle
        player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
