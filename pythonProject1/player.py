import pygame
import os

class Player:
    def __init__(self, char_type, game):
        self.game = game
        self.perso_scale = 15
        self.game = game
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ["Idle", "Walk", "Run", "Jump"]
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f'img/{char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (self.game.screen_width // self.perso_scale + self.perso_scale, self.game.screen_height // (self.perso_scale // 2)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()

        self.perso_width = self.image.get_width()
        self.perso_height = self.image.get_height()
        self.rect = pygame.Rect(0, self.game.screen.get_height() - self.perso_height, self.perso_width, self.perso_height)
        self.speed = 325
        self.direction = [0, 0]

        self.velocity_y = 0
        self.jump_force = 4.5 * 10
        self.gravity = 2.9 * self.jump_force
        self.scale_factor = self.game.screen_width / 1920
        self.jump_scale = self.perso_scale + ((1 * self.scale_factor) / 2)
        self.jump_count = self.perso_scale

        self.gliding = False
        self.is_moving = False
        self.is_running = False
        self.on_air = False

        for elt in self.animation_list:
            print(elt)

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


    def move_character(self, pressed, dt):
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.game.orientation = "Left"
            self.is_moving = True
            if self.rect.left <= 0:
                self.direction[0] = 0
            elif self.rect.left > 0:
                self.direction[0] = -1
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.game.orientation = "Right"
            self.is_moving = True
            if self.rect.right >= self.game.screen_width:
                self.direction[0] = 0
            elif self.rect.right < self.game.screen_width:
                self.direction[0] = 1
        else:
            self.direction[0] = 0
            self.is_moving = False

        self.rect.move_ip(self.direction[0] * self.speed * dt, self.direction[1] * self.speed * dt)

        if pressed[pygame.K_LSHIFT]:
            self.speed = 650
            if self.is_moving:
                self.is_running = True
            else:
                self.is_running = False
        else:
            self.speed = 325
            self.is_running = False

        if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]:
            if self.game.is_on_ground or self.game.is_on_platform:
                self.velocity_y = -self.jump_force
                self.game.is_on_ground = False
                self.game.is_on_platform = False
            else:
                if self.velocity_y > -3:
                    self.is_glidding(dt)

        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y

        print(self.gliding)

    def is_glidding(self, dt):
        if not self.game.is_on_ground and not self.game.is_on_platform:
            self.gliding = True
            if self.gliding == True:
                self.velocity_y += self.gravity * dt
                self.rect.y += self.velocity_y

                self.velocity_y = -(self.gravity / self.jump_force) * 0.9
                #self.velocity_y = -5  Pour s'envoler !!

                self.rect.x += self.direction[0] * 150 * dt

        else:
            self.velocity_y = 0
            self.gliding = False

    def draw_character(self):
        if self.game.orientation == "Right":
            self.game.screen.blit(self.image, self.rect)
        elif self.game.orientation == "Left":
            self.game.screen.blit(pygame.transform.flip(self.image, True, False), self.rect)
