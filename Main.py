import pygame
from pygame.locals import *
from random import randint

pygame.init()
largeur_fenetre = 1536
hauteur_fenetre = 864

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu avec inventaire")

# Chargement des images
fond = pygame.image.load("Images/background.png").convert()
perso = pygame.image.load("Images/Perso.png").convert_alpha()
balle = pygame.image.load("Images/golfBall.png").convert_alpha()

# Positionnement initial des personnages et de la balle
persoRect = perso.get_rect()
persoRect.topleft = (750, 754)
balleRect = balle.get_rect()
balleRect.topleft = (650, 754)

pygame.key.set_repeat(400, 30)
compteur_objets = 0
balle_dans_inventaire = False

# Position de la balle fixe à côté du compteur d'objets
balle_compteur_image = balle.copy()
balle_compteur_rect = balle_compteur_image.get_rect(topleft=(20, 20))

# Boucle principale du jeu
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if persoRect.left >= 10:
                    persoRect = persoRect.move(-25, 0)
            elif event.key == K_RIGHT:
                if persoRect.right <= largeur_fenetre - 10:
                    persoRect = persoRect.move(25, 0)
            elif event.key == K_f:
                if balleRect.colliderect(persoRect):
                    balle_dans_inventaire = True
                    compteur_objets += 1
                    balleRect.topleft = (randint(100, largeur_fenetre - 100), -100)
                    balle.set_alpha(0)

            elif event.key == K_a and compteur_objets>=1:
                if balle_dans_inventaire:
                    balleRect.topleft = (persoRect.right + 10, persoRect.top)
                    balle.set_alpha(255)
                    compteur_objets -= 1


    fenetre.blit(fond, (0, 0))
    fenetre.blit(perso, persoRect)
    fenetre.blit(balle, balleRect)

    # Affichage du compteur d'objets
    font = pygame.font.Font(None, 36)
    texte_compteur = font.render(f"Balles : {compteur_objets}", True, (255, 255, 255))
    fenetre.blit(texte_compteur, (balle_compteur_rect.right + 10, balle_compteur_rect.top))
    fenetre.blit(balle_compteur_image, balle_compteur_rect)

    pygame.display.update()
pygame.quit()
