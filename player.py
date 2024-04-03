import pygame

class Player:
    def __init__(self, game):
        self.game = game
        self.perso_scale = 15
        self.perso = pygame.image.load("img/perso JV.png")
        self.perso = pygame.transform.scale(self.perso, (self.game.screen_width // self.perso_scale, self.game.screen_height // (self.perso_scale // 2)))
        self.rect = self.perso.get_rect()
        self.rect.x = 500
        self.rect.y = self.game.screen.get_height() - self.perso.get_height()
        self.speed = 8
        self.velocity = [0, 0]
        self.perso_width = self.rect.width
        self.perso_height = self.rect.height


        self.is_jumping = False
        self.jump_scale = self.perso_scale + ((1 * self.game.screen_width) / 1920)
        self.jump_count = self.perso_scale
        self.vertical_speed = 0

    def move_character(self, pressed):
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

        self.rect.move_ip(self.velocity[0] * self.speed, self.velocity[1] * self.speed)

    def jump(self, pressed):
        if not self.is_jumping:
            if pressed[pygame.K_SPACE] or pressed[pygame.K_UP]:
                self.is_jumping = True
                self.vertical_speed = self.jump_scale

        if self.is_jumping:
            if self.jump_count >= -self.jump_scale:
                self.rect.y -= self.jump_count * abs(self.jump_count) * 0.4
                self.jump_count -= 1
                self.vertical_speed = -self.jump_count
            else:
                self.jump_count = self.jump_scale
                self.is_jumping = False
                self.rect.y = self.game.screen.get_height() - self.perso.get_height()
                self.vertical_speed = 0

        if not self.game.is_grounded:
            self.vertical_speed += self.game.gravity
            self.rect.y += self.vertical_speed

            # Détecter la collision avec le sol
            if self.rect.bottom >= self.game.ground_level:
                self.rect.bottom = self.game.ground_level
                self.vertical_speed = 0  # Arrêter la chute du joueur

    def draw_character(self):
        if self.game.orientation == "Right":
            self.game.screen.blit(self.perso, (self.rect))
        elif self.game.orientation == "Left":
            self.game.screen.blit(pygame.transform.flip(self.perso, True, False), (self.rect))
