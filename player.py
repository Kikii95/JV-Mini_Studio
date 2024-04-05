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
        #feet_offset = self.perso_width * 3 / 4  # Décalage pour aligner le milieu de la largeur avec les pieds
        #self.rect.x += feet_offset
        self.speed = 1000
        self.velocity = [0, 0]

        self.is_jumping = False
        self.scale_factor = self.game.screen_width / 1920
        self.jump_scale = self.perso_scale + ((1 * self.scale_factor) / 2)
        self.jump_count = self.perso_scale

    def move_character(self, pressed, is_jumping, dt):
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            self.game.orientation = "Left"
            if self.rect.left <= 0:
                self.velocity[0] = 0
            elif self.rect.left > 0:
                self.velocity[0] = -1
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.game.orientation = "Right"
            if self.rect.right >= self.game.screen_width:
                self.velocity[0] = 0
            elif self.rect.right < self.game.screen_width:
                self.velocity[0] = 1
        else:
            self.velocity[0] = 0

        self.rect.move_ip(self.velocity[0] * self.speed * dt, self.velocity[1] * self.speed * dt)

        if not is_jumping and (self.game.is_on_ground == True or self.game.is_on_platform == True):
            if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]:
                self.is_jumping = True

        if is_jumping:
            self.game.falling = True
            if self.jump_count >= -self.jump_scale:
                self.velocity[1] = -self.jump_count * abs(self.jump_count) * self.game.dt
                self.jump_count -= 1
            else:
                self.jump_count = self.jump_scale
                self.is_jumping = False

    def apply_gravity(self):
        if not self.game.is_on_ground or not self.game.is_on_platform:
            self.velocity[1] += 1
            self.rect.y += self.velocity[1]

    def draw_character(self):
        if self.game.orientation == "Right":
            self.game.screen.blit(self.perso, self.rect)
        elif self.game.orientation == "Left":
            self.game.screen.blit(pygame.transform.flip(self.perso, True, False), self.rect)
