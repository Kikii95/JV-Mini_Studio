import pygame
import csv
from player import Player

# Initialiser Pygame
pygame.init()

# Initialiser le module d'affichage
screen_width, screen_height = 1000, 1000  # Ajustez à votre configuration
screen = pygame.display.set_mode((screen_width, screen_height))

def lire_csv(fichier_csv):
    niveau = []
    with open(fichier_csv, newline='') as csvfile:
        lecteur = csv.reader(csvfile, delimiter=',')
        for ligne in lecteur:
            niveau.append([int(tuile) for tuile in ligne])
    return niveau

def creer_niveau(fichier_csv):
    niveau = lire_csv(fichier_csv)
    for y, ligne in enumerate(niveau):
        for x, tuile in enumerate(ligne):
            if tuile != 0:  # Créer un collider pour chaque tuile non nulle
                creer_collider(x, y, screen)
            if tuile == 15:  # Positionner le joueur à la tuile numéro 15
                joueur = Player(x * 50, y * 50, screen_width, screen_height)  # Ajustez 50 si la taille de votre tuile est différente

def creer_collider(x, y, screen):
    print(f"Création d'un collider en position ({x}, {y})")
    # Exemple pour dessiner un rectangle pour le collider (à ajuster selon vos besoins)
    pygame.draw.rect(screen, (255, 0, 0), (x * 50, y * 50, 50, 50), 2)

creer_niveau('level1_data.csv')

# Boucle de jeu (exemple simplifié)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour le jeu ici

    pygame.display.flip()  # Mettre à jour l'écran

pygame.quit()
