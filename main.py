import pygame
from player import Player


class Game:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = 1080
        self.perso_scale = 15

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

        self.player = Player(self)

        self.x = 0
        self.y = self.screen.get_height() - self.player.perso.get_height()
        self.is_jumping = False
        self.base_jump = self.player.perso_scale
        self.scale_factor = 20
        self.jump_scale = self.base_jump * (self.scale_factor / (self.player.perso_scale * 1.5))
        self.jump_count = self.jump_scale
        self.orientation = "Right"
        self.running = True

        self.area1 = pygame.Rect((self.screen_width - 250) / 2, self.screen_height - 350, 250, 350)
        self.area1_color = (255, 0, 0)
        self.area2 = pygame.Rect(self.screen_width - 500, (self.screen_height - 100) / 2, 500, 100)
        self.area2_color = (255, 0, 255)

        pygame.display.set_caption("Affichage de texte")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.running = False

    def update(self, pressed):
        self.player.move_character(pressed, self.is_jumping)
        if self.area1.colliderect(self.player.rect):
            self.area1_color = (0, 255, 0)
        else:
            self.area1_color = (255, 0, 0)

        if self.area2.colliderect(self.player.rect):
            self.area2_color = (0, 0, 255)
        else:
            self.area2_color = (200, 0, 200)

    def display(self):
        self.screen.fill((152, 140, 122))
        pygame.draw.rect(self.screen, self.area1_color, self.area1)
        pygame.draw.rect(self.screen, self.area2_color, self.area2)
        if self.area1_color == (0, 255, 0):
            self.text("Collider activé", 40, "black", "down_center")
        if self.area2_color == (0, 0, 255):
            self.text("Collider activé", 40, "white", "mid_right")
        self.player.draw_character()
        self.text("Bienvenue sur cette Alpha du jeu ! :p", 65, "white", "top_center")

        pygame.display.flip()


    def text(self, text, font_size, font_color, position):
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
            self.display()
            self.clock.tick(75)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
