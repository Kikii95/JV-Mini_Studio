import pygame
from player import Player
from camera import Camera

class Game:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080

        self.background = pygame.image.load("img/backgroundEndless-JV.png")
        self.background = pygame.transform.scale(self.background, (self.screen_width * 50, self.screen_height))
        self.rect = self.background.get_rect()
        self.background_height = self.background.get_height()
        self.rect.x = 0
        self.rect.y = self.screen_height - (self.screen_height)

        self.CameraX = self.rect.x
        self.CameraY = self.rect.y


        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.player = Player(self)
        self.camera = Camera(self)
        self.player.rect.bottom = self.screen_height


        self.x = 0
        self.y = self.screen.get_height() - self.player.perso.get_height()

        self.orientation = "Right"
        self.running = True
        self.is_grounded = True
        self.ground_level = self.screen_height - self.player.perso.get_height()
        self.distance_to_ground = 0
        self.gravity = 0.5

        self.area1_width = self.screen_width/7
        self.area1_height = self.screen_height/3
        self.area2_width = self.screen_width / 3
        self.area2_height = self.screen_height / 10

        self.area1 = pygame.Rect(((self.screen_width - self.area1_width) /2) , self.screen_height - self.area1_height, self.area1_width, self.area1_height)
        self.area1_color = (255, 0, 0)
        self.area2 = pygame.Rect((self.screen_width - self.area2_width) , (self.screen_height - self.area2_height) / 2, self.area2_width, self.area2_height)
        self.area2_color = (255, 0, 255)
        self.ground_area = pygame.Rect(0, self.screen_height - 50, self.screen_width, 50)
        self.ground_color = (255, 255, 0)

        pygame.display.set_caption("Affichage de texte")

    def check_grounded(self):
        # On vérifie si le bas du joueur est au niveau du sol
        return self.player.rect.bottom == self.screen_height

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.running = False

    def update(self, pressed):
        self.player.move_character(pressed)
        self.player.jump(pressed)
        self.camera.update()

        self.ground_level = self.screen_height - self.player.perso.get_height()

        if self.player.vertical_speed > 0:
            self.is_grounded = False
        else:
            self.is_grounded = self.check_grounded()

        if self.player.rect.bottom >= self.background_height:
            self.is_grounded = True

        self.distance_to_ground = self.background_height - self.player.rect.bottom

        if self.distance_to_ground < 0:
            self.distance_to_ground = 0

        if self.area1.colliderect(self.player.rect):
            self.area1_color = (0, 255, 0)
        else:
            self.area1_color = (255, 0, 0)

        if self.area2.colliderect(self.player.rect):
            self.area2_color = (0, 0, 255)
        else:
            self.area2_color = (200, 0, 200)

        if self.ground_area.colliderect(self.player.rect):
            self.ground_color = (0, 0, 255)
        else:
            self.ground_color = (200, 0, 200)

    def display(self):
        self.screen.fill((152, 140, 122))
        self.screen.blit(self.background, (self.rect))
        pygame.draw.rect(self.screen, self.area1_color, self.area1)
        pygame.draw.rect(self.screen, self.area2_color, self.area2)
        pygame.draw.rect(self.screen, self.ground_color, self.ground_area)
        if self.area1_color == (0, 255, 0):
            self.text("Collider activé", 40, "black", "down_center")
        if self.area2_color == (0, 0, 255):
            self.text("Collider activé", 40, "white", "mid_right")
        if self.ground_color == (0, 0, 255):
            self.is_grounded = True
        self.player.draw_character()
        self.text("Bienvenue sur cette Alpha du jeu ! :p", 65, "black", "top_center")

        pygame.display.flip()


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

    def run(self):
        while self.running:
            self.handle_events()
            pressed = pygame.key.get_pressed()
            self.update(pressed)
            self.camera.update()  # S'assure que la caméra est mise à jour après la mise à jour du joueur
            self.display()
            self.clock.tick(75)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
