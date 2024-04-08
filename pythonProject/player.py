import pygame

class Player:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Chargez ici votre sprite de joueur et ajustez sa taille si nécessaire
        self.perso = pygame.image.load('img/perso JV.png').convert_alpha()
        self.perso = pygame.transform.scale(self.perso, (50, 50))  # Ajustez les dimensions selon les besoins

        # Initialisation du rectangle pour le joueur
        self.rect = self.perso.get_rect(topleft=(self.x, self.y))

        # Variables pour la gestion des mouvements
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 5  # Ajustez selon les besoins
        self.gravity = 0.5  # Ajustez selon les besoins
        self.jump_height = -10  # Ajustez selon les besoins

    def move(self, keys):
        self.velocity.x = 0

        # Mouvement gauche/droite
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = self.speed

        # Ajouter la gravité
        self.apply_gravity()

        # Mise à jour de la position du rectangle
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Empêcher le joueur de sortir de l'écran
        self.rect.x = max(0, min(self.screen_width - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(self.screen_height - self.rect.height, self.rect.y))

    def apply_gravity(self):
        self.velocity.y += self.gravity
        self.velocity.y = min(self.velocity.y, 10)  # Limite la vitesse de chute

    def jump(self):
        self.velocity.y = self.jump_height

    def draw(self, screen):
        screen.blit(self.perso, self.rect)

# Exemple d'utilisation dans la boucle principale du jeu
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# player = Player(100, 100, 800, 600)
# clock = pygame.time.Clock()

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 player.jump()

#     keys = pygame.key.get_pressed()
#     player.move(keys)

#     screen.fill((0, 0, 0))  # Efface l'écran
#     player.draw(screen)
#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
