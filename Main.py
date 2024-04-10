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
fond_inv = pygame.image.load("Images/fondGris.jpg").convert_alpha()

# Positionnement initial des personnages et de la balle
persoRect = perso.get_rect()
persoRect.topleft = (750, 754)
balleRect = balle.get_rect()
balleRect.topleft = (650, 754)
fond_invRect = fond_inv.get_rect()
fond_invRect.topleft = (550, 275)
fond_inv.set_alpha(0)

pygame.key.set_repeat(400, 30)
compteur_objets = 0
balle_dans_inventaire = False
inventaire = []

# Position de la balle fixe à côté du compteur d'objets
balle_compteur_image = balle.copy()
balle_compteur_rect = balle_compteur_image.get_rect(topleft=(1320, 20))

# Couleur du texte de l'inventaire
text_color = (255, 255, 255)
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)

inv_open = False
balrectemp = balleRect.topleft

# Police de caractères pour l'affichage de l'inventaire
font = pygame.font.Font(None, 36)

def afficher_inventaire(inv_open,balrectemp):
    alphatemp = balle.get_alpha
    
    if inv_open == False:
        balrectemp = balleRect.topleft
        balleRect.topleft = (575, 300)
        balle.set_alpha(255)
        fond_inv.set_alpha(255)
        inv_open = True
        return inv_open, balrectemp
    elif inv_open == True:
        balleRect.topleft = (balrectemp)
        balle.set_alpha(0)
        fond_inv.set_alpha(0)
        inv_open = False
        return inv_open, balrectemp

def detecter_hover(mouse_pos):
    global inventaire
    for i, (item_rect, item_image) in enumerate(inventaire):
        if item_rect.collidepoint(mouse_pos):
            # Si la souris survole l'objet, retourner l'index de l'objet et son emplacement
            return i, item_rect, item_image
    # Si aucun objet n'est survolé, retourner None
    return None, None, None

# Boucle principale du jeu
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            item_index = balleRect.collidepoint(mouse_x, mouse_y)
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
                    inventaire.append((balleRect, balle))  # Ajout de la balle à l'inventaire
                    balleRect.topleft = (randint(100, largeur_fenetre - 100), -100)
                    balle.set_alpha(0)

            elif event.key == K_a and compteur_objets >= 1:
                if balle_dans_inventaire:
                    balleRect.topleft = (persoRect.right + 10, persoRect.top)
                    balle.set_alpha(255)
                    compteur_objets -= 1

            elif event.key == K_e:
                # Ouvrir l'inventaire en appuyant sur la touche E
                print("Inventaire ouvert")
                print("Contenu de l'inventaire:", inventaire)
                inv_open, balrectemp = afficher_inventaire(inv_open,balrectemp)  # Afficher l'inventaire
    fenetre.fill(BLANC)
    fenetre.blit(fond, (0, 0))
    fenetre.blit(perso, persoRect)
    fenetre.blit(fond_inv,fond_invRect)
    fenetre.blit(balle, balleRect)
    if item_index:
        # Si la souris survole un objet, afficher l'image de l'objet
        texte_objet1 = font.render("Objet 1 survolé", True, NOIR)
        fenetre.blit(texte_objet1, (balleRect.right + 10, balleRect.top))
    
    

    # Affichage du compteur d'objets
    texte_compteur = font.render(f"Balles : {compteur_objets}", True, (255, 255, 255))
    fenetre.blit(texte_compteur, (balle_compteur_rect.right + 10, balle_compteur_rect.top))
    fenetre.blit(balle_compteur_image, balle_compteur_rect)


    pygame.display.update()
pygame.quit()