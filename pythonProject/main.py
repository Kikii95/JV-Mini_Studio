import pygame
import sys
from player import Player
from camera import Camera

class Game:
    def __init__(self, level_file=None):
        self.screen_width = 1920
        self.screen_height = 1080

        self.background_scale = 1.2
        self.background = pygame.image.load("img/backgroundEndless_JV.png")
        self.background = pygame.transform.scale(self.background, ( self.screen_width * self.background_scale, self.screen_height * self.background_scale))  # Double la largeur pour créer l'effet endless
        self.rect1 = self.background.get_rect()
        self.rect2 = self.background.get_rect()
        self.rect1.x = 0 - ((self.screen_width * 1 / 9) * self.background_scale)
        self.rect2.x = self.screen_width * self.background_scale
        self.rect1.y = self.screen_height - (self.screen_height * self.background_scale)
        self.rect2.y = self.screen_height - (self.screen_height * self.background_scale)

        self.Camera1X = self.rect1.x
        self.Camera1Y = self.rect1.y
        self.Camera2X = self.rect2.x
        self.Camera2Y = self.rect2.y

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.player = Player(self)
        self.camera = Camera(self)


        self.x = 0
        self.y = self.screen.get_height() - self.player.perso.get_height()

        self.orientation = "Right"
        self.running = True
        self.is_on_ground = False
        self.is_on_platform = False

        self.ground_width = self.screen_width
        self.ground_height = 200

        self.ground = pygame.Rect(0 - self.camera.left_screen_cap , (self.screen_height - 22), self.ground_width + self.camera.right_screen_cap, self.ground_height)
        self.ground_color = (255, 0, 255)

        self.p1_width = 200
        self.p1_height = 300

        self.platforms = []
        self.create_platform(1100, self.screen_height, 200, 100, 'blue')
        self.create_platform(1600, self.screen_height, 200, 200, 'white')
        self.create_platform(2100, self.screen_height, 200, 300, 'red')

        self.create_platform(2400, self.screen_height * 6/10, 200, 50, 'yellow')
        self.create_platform(2600, self.screen_height * 2/10, 200, 50, 'green')
        self.create_platform(3000, self.screen_height * 1/10, 200, 50, 'purple')
        self.create_platform(3500, self.screen_height * 2/10, 200, 50, 'black')
        self.create_platform(3900, self.screen_height * 0/10, 200, 50, 'pink')

        if level_file:
            self.load_level(level_file)
        else:
            # Charger un niveau par défaut ou lancer l'éditeur de niveaux
            pygame.display.set_caption("Affichage de texte")



    def create_platform(self, x, y, width, height, color=None):
        if color is None:
            color = (255, 255, 255)
        platform = pygame.Rect(x - self.camera.left_screen_cap, y - height, width, height)
        self.platforms.append((platform, color))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.running = False

    def update_background(self):
        if self.rect1.right <= 0:
            self.rect1.x = self.rect2.right
        elif self.rect2.right <= 0:
            self.rect2.x = self.rect1.right

        if self.rect1.left >= self.screen_width * self.background_scale :
            self.rect1.x = (self.rect2.left - (self.screen_width * self.background_scale))
        elif self.rect2.left >= self.screen_width * self.background_scale:
            self.rect2.x = (self.rect1.left - (self.screen_width * self.background_scale))

    def is_visible(self, rect):
        camera_rect = pygame.Rect(self.camera.CameraX, self.camera.CameraY, self.screen_width, self.screen_height)
        return camera_rect.colliderect(rect)

    def text(self, text, text_size, font_color, position):
        font_size = int(float((text_size * self.screen_width) / 1920))
        font = pygame.font.Font(None, font_size)
        margin = font_size

        positions = {
            "top_left": (margin, margin),
            "top_center": (self.screen_width // 2, margin),
            "top_right": (self.screen_width - margin, margin),
            "mid_left": (margin, self.screen_height // 2),
            "mid_center": (self.screen_width // 2, self.screen_height // 2),
            "mid_right": (self.screen_width - margin, self.screen_height // 2),
            "down_left": (margin, self.screen_height - margin),
            "down_center": (self.screen_width // 2, self.screen_height - margin),
            "down_right": (self.screen_width - margin, self.screen_height - margin)
        }

        text_position = positions.get(position, (0, 0))

        text_surface = font.render(text, True, font_color)
        text_rect = text_surface.get_rect(center = text_position)

        if text_rect.left < margin:
            text_rect.left = margin
        elif text_rect.right > self.screen_width - margin:
            text_rect.right = self.screen_width - margin

        if text_rect.top < margin:
            text_rect.top = margin
        elif text_rect.bottom > self.screen_height - margin:
            text_rect.bottom = self.screen_height - margin

        self.screen.blit(text_surface, text_rect)

    def display(self):
        self.screen.fill((152, 140, 122))
        self.screen.blit(self.background, self.rect1)
        self.screen.blit(self.background, self.rect2)

        for platform in self.platforms:
            if self.is_visible(platform[0]):
                pygame.draw.rect(self.screen, platform[1], platform[0])
        #if self.is_visible(self.ground):
            #pygame.draw.rect(self.screen, self.ground_color, self.ground)


        self.player.draw_character()
        self.text("Bienvenue sur cette Alpha du jeu ! :p", 65, "black", "top_center")

        pygame.display.flip()

    def update(self, pressed):
        self.player.move_character(pressed, self.player.is_jumping, self.dt)
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_q] or keys[pygame.K_SPACE]:
            #self.camera.update()
        self.camera.update()

        for platform in self.platforms:
            if platform[0].colliderect(self.player.rect):
                if self.player.rect.bottom > platform[0].top > self.player.rect.top and (platform[0].left <= self.player.rect.left + (self.player.perso_width * 3 / 4) and platform[0].right >= self.player.rect.right - (self.player.perso_width * 3 / 4)) and self.player.velocity[1] > 0:
                    self.is_on_platform = True
                    self.player.velocity[1] = 0
                    self.player.rect.bottom = platform[0].top
                elif self.player.rect.right > platform[0].left > self.player.rect.left and self.player.rect.bottom > platform[0].top:
                    self.player.rect.right = platform[0].left
                elif self.player.rect.left < platform[0].right < self.player.rect.right and self.player.rect.bottom > platform[0].top:
                    self.player.rect.left = platform[0].right
                elif self.player.rect.top < platform[0].bottom and self.player.rect.bottom > platform[0].top:
                    self.player.rect.top = platform[0].bottom


            else:
                self.p1_color = (255, 0, 0)


        if self.ground.colliderect(self.player.rect):
            self.ground_color = (0, 0, 255)
            self.is_on_ground = True
            self.player.velocity[1] = 0
            self.player.rect.bottom = self.ground.top
            #self.ground.top += 1
        else:
            self.ground_color = (200, 0, 200)

        if self.player.velocity[1] != 0:
            self.is_on_ground = False
            self.is_on_platform = False
        if (not self.is_on_platform or not self.is_on_ground) and not self.player.is_jumping:
            self.player.apply_gravity()


    def run(self):
        self.dt = 0
        FPSTarget = 60
        dtTarget = 1 / FPSTarget
        while self.running:
            start = pygame.time.get_ticks()

            self.camera.update()
            self.update_background()
            self.handle_events()
            pressed = pygame.key.get_pressed()
            self.update(pressed)
            self.display()
            self.dt = (pygame.time.get_ticks() - start) / 1000
            if self.dt < dtTarget:
                pygame.time.wait(int(1000 * (dtTarget - self.dt)))
                self.dt = dtTarget

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()