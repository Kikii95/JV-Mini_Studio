import pygame
import os
import sys

# Initialisation de Pygame
pygame.init()

# Charger l'image de fond
background_image = pygame.image.load('img/CHOIX_NIVEAU.png')

# Configurations pour le bouton transparent
button_color = (255, 255, 255, 128)  # Couleur blanche avec une transparence
transparent_button_position = [190, 350, 295, 600]  # Remplacer avec les coordonnées et la taille réelle

# Créer une surface pour le bouton transparent avec la transparence
button_surface = pygame.Surface((transparent_button_position[2], transparent_button_position[3]), pygame.SRCALPHA)
button_surface.fill(button_color)

# Configuration pour le bouton 'roue'
wheel_image = pygame.image.load('img/roue.png')
wheel_image = pygame.transform.scale(wheel_image, (100, 100))  # Redimensionner l'image si nécessaire
wheel_button_position = [10, 10, 100, 100]  # Coordonnées x, y et taille du bouton 'roue'

# Fonction pour lancer le script externe
def run_external_script(script_name):
    os.system(f'python {script_name}')

# Créer la fenêtre de Pygame
screen = pygame.display.set_mode(background_image.get_size())
pygame.display.set_caption('Menu')

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si le clic est sur le bouton transparent
            if button_surface.get_rect(topleft=transparent_button_position[:2]).collidepoint(event.pos):
                run_external_script('main2.py')
            # Vérifier si le clic est sur le bouton 'roue'
            if pygame.Rect(wheel_button_position).collidepoint(event.pos):
                run_external_script('carte.py')

    # Afficher l'image de fond
    screen.blit(background_image, (0, 0))
    
    # Afficher le bouton transparent par-dessus l'image de fond
    screen.blit(button_surface, transparent_button_position[:2])
    
    # Afficher le bouton 'roue'
    screen.blit(wheel_image, (wheel_button_position[0], wheel_button_position[1]))
    
    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame proprement
pygame.quit()
sys.exit()
