import pygame

class Camera:

    def __init__(self, game):
        self.game = game
        self.player = player
        self.CameraX = 0
        self.CameraY = 0

    def move_background(self, pressed):
        if pressed[pygame.K_a]:
            self.CameraX += 5
            self.area1 = pygame.Rect(((self.screen_width - self.area1_width) / 2) - self.CameraX,
                                     self.screen_height - self.area1_height, self.area1_width, self.area1_height)
            self.area2 = pygame.Rect((self.screen_width - self.area2_width) - self.CameraX,
                                     (self.screen_height - self.area2_height) / 2, self.area2_width, self.area2_height)
        elif pressed[pygame.K_e]:
            self.CameraX -= 5
            self.area1 = pygame.Rect(((self.screen_width - self.area1_width) / 2) - self.CameraX,
                                     self.screen_height - self.area1_height, self.area1_width, self.area1_height)
            self.area2 = pygame.Rect((self.screen_width - self.area2_width) - self.CameraX,
                                     (self.screen_height - self.area2_height) / 2, self.area2_width, self.area2_height)
