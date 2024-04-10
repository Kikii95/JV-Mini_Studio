import pygame
from random import randint

class Balle:
    def __init__(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    def affiche(self, fenetre):
        fenetre.blit(self.image, self.rect)