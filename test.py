import pygame
from pygame.locals import *

pygame.init()
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Effet de survol")

# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)

# Création des rectangles représentant les objets survolables
objet1_rect = pygame.Rect(100, 100, 100, 50)
objet2_rect = pygame.Rect(300, 200, 150, 100)

# Variable pour indiquer si l'objet est survolé
survol_objet1 = False
survol_objet2 = False

# Police de caractères
font = pygame.font.Font(None, 24)

# Boucle principale du jeu
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == MOUSEMOTION:
            # Récupérer les coordonnées de la souris
            mouse_x, mouse_y = event.pos
            # Vérifier si la souris survole l'objet 1
            survol_objet1 = objet1_rect.collidepoint(mouse_x, mouse_y)
            # Vérifier si la souris survole l'objet 2
            survol_objet2 = objet2_rect.collidepoint(mouse_x, mouse_y)

    # Effacer l'écran
    fenetre.fill(BLANC)

    # Dessiner les objets
    # Si survolé, changer la couleur de fond et afficher le texte
    if survol_objet1:
        pygame.draw.rect(fenetre, BLEU, objet1_rect)
        texte_objet1 = font.render("Objet 1 survolé", True, NOIR)
        fenetre.blit(texte_objet1, (objet1_rect.right + 10, objet1_rect.top))
    else:
        pygame.draw.rect(fenetre, NOIR, objet1_rect)

    if survol_objet2:
        pygame.draw.rect(fenetre, BLEU, objet2_rect)
        texte_objet2 = font.render("Objet 2 survolé", True, NOIR)
        fenetre.blit(texte_objet2, (objet2_rect.right + 10, objet2_rect.top))
    else:
        pygame.draw.rect(fenetre, NOIR, objet2_rect)

    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()