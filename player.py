import pygame

class Player:
    def __init__(self, game):
        self.game = game
        self.perso_scale = 15
        self.perso = pygame.image.load("img/perso JV.png")
        self.perso = pygame.transform.scale(self.perso, (self.game.screen_width // self.perso_scale, self.game.screen_height // (self.perso_scale // 2)))
        self.perso_width = self.perso.get_width()
        self.perso_height = self.perso.get_height()
        self.rect = pygame.Rect(0, self.game.screen.get_height() - self.perso_height, self.perso_width, self.perso_height)
        self.rect.x = 0
        self.rect.y = self.game.screen.get_height() - self.perso_height
        self.speed = 325
        self.direction = [0, 0]

        self.velocity_y = 0
        self.jump_force = 4.5 * 10
        self.gravity = 2.9 * self.jump_force


        self.scale_factor = self.game.screen_width / 1920
        self.jump_scale = self.perso_scale + ((1 * self.scale_factor) / 2)
        self.jump_count = self.perso_scale

        self.gliding = False

    def move_character(self, pressed, dt):
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.game.orientation = "Left"
            if self.rect.left <= 0:
                self.direction[0] = 0
            elif self.rect.left > 0:
                self.direction[0] = -1
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.game.orientation = "Right"
            if self.rect.right >= self.game.screen_width:
                self.direction[0] = 0
            elif self.rect.right < self.game.screen_width:
                self.direction[0] = 1
        else:
            self.direction[0] = 0

        self.rect.move_ip(self.direction[0] * self.speed * dt, self.direction[1] * self.speed * dt)

        if pressed[pygame.K_LSHIFT]:
            self.speed = 650
        else:
            self.speed = 325

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
            self.game.screen.blit(self.perso, self.rect)
        elif self.game.orientation == "Left":
            self.game.screen.blit(pygame.transform.flip(self.perso, True, False), self.rect)
