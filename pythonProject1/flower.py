import pygame

class FlowerSeed:
    def __init__(self, game):
        self.game = game
        h = 30
        x = 500
        y = self.game.screen_height - (self.game.screen_height - self.game.camera.down_screen_cap)
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = pygame.image.load("img/player/Walk/0.png").convert_alpha()
        self.planted = False
        self.growing = False
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
            self.game.screen.blit(self.image, self.rect)
        elif self.growing:
            if self.animation_index < len(self.animation_frames):
                self.game.screen.blit(self.animation_frames[int(self.animation_index)], self.rect)
            # else:
            # self.pickable = True  Once animation is finished, flower becomes pickable