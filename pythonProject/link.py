import pygame
import csv
from player import Player

# Initialiser Pygame
pygame.init()

# Définir la largeur et la hauteur de l'écran
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Charger les images des tuiles et associer chaque numéro de tuile à son image
tuiles_images = {
       1: pygame.image.load('img/tile/0.png'),
    2: pygame.image.load('img/tile/1.png'),
    3: pygame.image.load('img/tile/2.png'),
    4: pygame.image.load('img/tile/3.png'),
    5: pygame.image.load('img/tile/4.png'),
    6: pygame.image.load('img/tile/5.png'),
    7: pygame.image.load('img/tile/6.png'),
    8: pygame.image.load('img/tile/7.png'),
    9: pygame.image.load('img/tile/8.png'),
    10: pygame.image.load('img/tile/9.png'),
    11: pygame.image.load('img/tile/10.png'),
    12: pygame.image.load('img/tile/11.png'),
    13: pygame.image.load('img/tile/12.png'),
    14: pygame.image.load('img/tile/13.png'),
    15: pygame.image.load('img/tile/14.png'),
    16: pygame.image.load('img/tile/15.png'),
    17: pygame.image.load('img/tile/16.png'),
    18: pygame.image.load('img/tile/17.png'),
    19: pygame.image.load('img/tile/18.png'),
    20: pygame.image.load('img/tile/19.png'),
    21: pygame.image.load('img/tile/20.png'),



}

# Charger l'image d'arrière-plan
arriere_plan = pygame.image.load('img/fond.webp').convert()

# Variable pour stocker l'instance du joueur
joueur = None

# Lire le fichier CSV et retourner une matrice représentant le niveau
def lire_csv(fichier_csv):
    niveau = []
    with open(fichier_csv, newline='') as csvfile:
        lecteur = csv.reader(csvfile, delimiter=',')
        for ligne in lecteur:
            niveau.append([int(tuile) if tuile.isdigit() else 0 for tuile in ligne])
    return niveau

# Fonction pour créer le niveau à partir du fichier CSV
def creer_niveau(fichier_csv):
    global joueur
    niveau = lire_csv(fichier_csv)
    for y, ligne in enumerate(niveau):
        for x, tuile in enumerate(ligne):
            if tuile in tuiles_images:
                # Dessiner l'image de la tuile
                screen.blit(tuiles_images[tuile], (x * 50, y * 50))
            if tuile == 15 and joueur is None:  # Supposer que 15 est le numéro pour le joueur
                # Créer le joueur à cet emplacement
                joueur = Player(x * 50, y * 50, screen_width, screen_height)

# Boucle de jeu principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gérer les entrées du joueur
    if joueur:
        joueur.handle_keys()

    # Mettre à jour l'écran à chaque passage dans la boucle
    screen.fill((0, 0, 0))  # Remplir l'écran de noir
    screen.blit(arriere_plan, (0, 0))  # Dessiner l'arrière-plan
    creer_niveau('level1_data.csv')  # Redessiner le niveau
    if joueur:
        joueur.draw(screen)  # Dessiner le joueur

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()
