import pygame
from pygame.locals import *
from balle import Balle
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
ballinv = balle.copy()

##-----------------------##
class Personnage:
    def __init__(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    def affiche(self, fenetre):
        fenetre.blit(self.image, self.rect)


# Positionnement initial des personnages et de la balle
persoRect = perso.get_rect()
persoRect.topleft = (750, 754)
balleRect = balle.get_rect()
balleRect.topleft = (650, 754)
ballinvrect = ballinv.get_rect()
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

inv_open = True
startinv = 0
balrectemp = balleRect.topleft

# Police de caractères pour l'affichage de l'inventaire
font = pygame.font.Font(None, 36)

def afficher_inventaire(inv_open,):
    if inv_open == False:
        fond_inv.set_alpha(255)
        inv_open = True
        return inv_open
    elif inv_open == True:
        fond_inv.set_alpha(0)
        inv_open = False
        return inv_open

def detecter_hover(mouse_pos):
    global inventaire
    for i, (item_rect, item_image) in enumerate(inventaire):
        if item_rect.collidepoint(mouse_pos):
            return i, item_rect, item_image
    return None, None, None

continuer = True
item_index = None
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            if inv_open:
                item_index = None
                for index, bal in enumerate(inventaire):
                    balrect = bal.rect
                    if balrect.collidepoint(mouse_x, mouse_y):
                        item_index = index
                        if isinstance(bal, Balle):
                            texte_obj ="Balle"
                        elif isinstance(bal, Personnage):
                            texte_obj ="Personnage"
                        break
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
                    inventaire.append(Balle("Images/golfBall.png"))
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
                if startinv==0:
                    inv_open = False
                    startinv += 1 
                inv_open = afficher_inventaire(inv_open)

            elif event.key == K_j:
                    compteur_objets += 2
                    inventaire.append(Balle("Images/golfBall.png"))
                    inventaire.append(Personnage("Images/Perso.png"))
    fenetre.fill(BLANC)
    fenetre.blit(fond, (0, 0))
    fenetre.blit(perso, persoRect)
    fenetre.blit(fond_inv,fond_invRect)
    fenetre.blit(balle, balleRect)
    if inv_open == True and startinv!=0:
        start_x = 575
        for bal in inventaire:
            bal.affiche(fenetre)  
            balrect = bal.rect 
            balrect.topleft = (start_x, 300)
            start_x += balrect.width + 10
    if item_index is not None:
        # Si la souris survole un objet, afficher le texte d'information à côté de cet objet
        texte_objet = font.render(f"{texte_obj} {item_index + 1} survolé", True, NOIR)
        fenetre.blit(texte_objet, (balrect.right + 10, balrect.top))
    
    

    # Affichage du compteur d'objets
    texte_compteur = font.render(f"Objets : {compteur_objets}", True, (255, 255, 255))
    fenetre.blit(texte_compteur, (balle_compteur_rect.right + 10, balle_compteur_rect.top))
    fenetre.blit(balle_compteur_image, balle_compteur_rect)


    pygame.display.update()
pygame.quit()