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


def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))


def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    paused = False

        screen.fill((0, 0, 0))
        pause_font = pygame.font.Font(None, int(SCREEN_WIDTH / 20))
        button_width = SCREEN_WIDTH / 4
        button_height = SCREEN_HEIGHT / 15

        resume_text = pause_font.render("Resume", True, (255, 255, 255))
        restart_text = pause_font.render("Restart", True, (255, 255, 255))
        main_menu_text = pause_font.render("Main Menu", True, (255, 255, 255))
        quit_text = pause_font.render("Quit Game", True, (255, 255, 255))

        button_gap = SCREEN_HEIGHT / 20
        button_y = SCREEN_HEIGHT / 4

        resume_button = pygame.Rect((SCREEN_WIDTH - button_width) / 2, button_y, button_width, button_height)
        restart_button = pygame.Rect((SCREEN_WIDTH - button_width) / 2, button_y + button_height + button_gap, button_width, button_height)
        main_menu_button = pygame.Rect((SCREEN_WIDTH - button_width) / 2, button_y + (button_height + button_gap) * 2, button_width, button_height)
        quit_button = pygame.Rect((SCREEN_WIDTH - button_width) / 2, button_y + (button_height + button_gap) * 3, button_width, button_height)

        pygame.draw.rect(screen, (255, 0, 0), resume_button)
        pygame.draw.rect(screen, (255, 0, 0), restart_button)
        pygame.draw.rect(screen, (255, 0, 0), main_menu_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)

        screen.blit(resume_text, ((SCREEN_WIDTH - resume_text.get_width()) / 2, button_y))
        screen.blit(restart_text, ((SCREEN_WIDTH - restart_text.get_width()) / 2, button_y + button_height + button_gap))
        screen.blit(main_menu_text, ((SCREEN_WIDTH - main_menu_text.get_width()) / 2, button_y + (button_height + button_gap) * 2))
        screen.blit(quit_text, ((SCREEN_WIDTH - quit_text.get_width()) / 2, button_y + (button_height + button_gap) * 3))

        pygame.display.update()
        clock.tick(60)


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


player = Player("player", 200, 200, 3, 5)
enemy = Player("enemy", 400, 200, 3, 5)

run = True
while run:

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()
    enemy.draw()

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
            if event.key == pygame.K_o:
                pause_menu()

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()

pygame.quit()
