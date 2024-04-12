import pygame
import os
import subprocess


# Initialise Pygame
pygame.init()

# Charge l'image de fond
background_image = pygame.image.load('img/CARTE.png')

# Taille de l'écran basée sur l'image de fond
screen = pygame.display.set_mode(background_image.get_size())
pygame.display.set_caption('Menu avec bouton')

# Position et taille du bouton, à ajuster selon les coordonnées exactes
button_color = (255, 0, 0)  # Couleur rouge pour le bouton
button_position = (355, 332)  # Utiliser les coordonnées exactes du cercle rouge
button_radius = 20

# Fonction pour dessiner le bouton
def draw_button(screen, position, radius, color):
    pygame.draw.circle(screen, color, position, radius)

# Fonction pour vérifier si le bouton est cliqué
def is_button_clicked(position, radius, mouse_pos):
    return pygame.math.Vector2(position).distance_to(mouse_pos) < radius

# Fonction pour exécuter un autre script Python
def run_script():
    subprocess.run(['python', 'chapters.py'])

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if is_button_clicked(button_position, button_radius, mouse_pos):
                run_script()

    # Affiche l'image de fond
    screen.blit(background_image, (0, 0))
    
    # Dessine le bouton sur l'écran
    draw_button(screen, button_position, button_radius, button_color)
    
    # Met à jour l'affichage
    pygame.display.flip()

# Quitte Pygame
pygame.quit()
