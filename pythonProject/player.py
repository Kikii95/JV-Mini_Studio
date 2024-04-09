import pygame

class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Charger l'image du joueur et la redimensionner si nécessaire
        self.perso = pygame.image.load('img/perso JV.png').convert_alpha()
        self.perso = pygame.transform.scale(self.perso, (50, 50))  # Modifier la taille selon besoin

        # Créer un rectangle pour le joueur
        self.rect = self.perso.get_rect(topleft=(self.x, self.y))

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= 1  # Vitesse de déplacement à gauche
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 1  # Vitesse de déplacement à droite
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.rect.y -= 1  # Vitesse de déplacement en haut (saut si vous ajoutez de la physique)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += 1  # Vitesse de déplacement en bas

    def draw(self, screen):
        # Dessiner le joueur sur l'écran
        screen.blit(self.perso, self.rect)
