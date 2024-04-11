import pygame, sys
class PhotoAlbum:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.current_page = 0
        self.screen_width, self.screen_height = self.screen.get_size()
        self.album_background = pygame.transform.scale(pygame.image.load('album_background.png'), (self.screen_width, self.screen_height))  # Chargement arrière-plan de l'album
        self.next_button = pygame.transform.scale(pygame.image.load('next_button.png'), (200, 200))  # Loading next button
        self.prev_button = pygame.transform.scale(pygame.image.load('prev_button.png'), (200, 200))  # Loading previous button
        self.close_button = pygame.transform.scale(pygame.image.load('close_button.png'), (100, 100))  # Chargement bouton de fermeture        
        self.pages = [[(pygame.transform.scale(pygame.image.load('photo1.png'), (self.screen_width//3, self.screen_height//3)), (self.screen_width//6 - 50, self.screen_height//4)),  # Chargement des photos
        (pygame.transform.scale(pygame.image.load('photo2.png'), (self.screen_width//3, self.screen_height//3)), (self.screen_width//2 + 50, self.screen_height//2))],
        [(pygame.transform.scale(pygame.image.load('photo3.png'), (self.screen_width//3, self.screen_height//3)), (self.screen_width//6 - 50, self.screen_height//4)),  
        (pygame.transform.scale(pygame.image.load('photo4.png'), (self.screen_width//3, self.screen_height//3)), (self.screen_width//2 + 50, self.screen_height//2))]]
        self.hovered_photo = None
        self.clicked_photo = None
        self.back_button = pygame.transform.scale(pygame.image.load('prev_button.png'), (50, 50))  
        self.transparent_background = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.transparent_background.fill((128, 128, 128, 128))


    def handle_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            if self.visible:
                self.hovered_photo = None
                for photo, position in self.pages[self.current_page]:
                    if photo.get_rect(topleft=position).collidepoint(x, y):
                        self.hovered_photo = photo, position
                        break

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.visible:
                if self.clicked_photo and self.back_button.get_rect(topleft=(10, 10)).collidepoint(x, y):
                    self.clicked_photo = None
                elif not self.clicked_photo:
                    if self.close_button.get_rect(topleft=(10, 10)).collidepoint(x, y):
                        self.visible = False
                    elif self.current_page < len(self.pages) - 1 and self.next_button.get_rect(topleft=(self.screen_width - self.next_button.get_width() - 30, self.screen_height - self.next_button.get_height() - 10)).collidepoint(x, y):
                        self.current_page += 1
                    elif self.current_page > 0 and self.prev_button.get_rect(topleft=(50, self.screen_height - self.prev_button.get_height() - 10)).collidepoint(x, y):
                        self.current_page -= 1
                    else:
                        for photo, position in self.pages[self.current_page]:
                            if photo.get_rect(topleft=position).collidepoint(x, y):
                                self.clicked_photo = pygame.transform.scale(photo, (self.screen_width, self.screen_height))
                                break

    def draw(self):
        if self.visible:
            if self.clicked_photo:
                self.screen.blit(self.transparent_background, (0, 0))
                self.screen.blit(self.clicked_photo, (0, 0))
                self.screen.blit(self.back_button, (10, 10))
            else:
                #arrière-plan de l'album
                self.screen.blit(self.album_background, (0, 0))
                #chaque photo de la page actuelle
                for photo, position in self.pages[self.current_page]:
                    if (photo, position) == self.hovered_photo:
                        self.screen.blit(pygame.transform.scale(photo, (photo.get_width() + 10, photo.get_height() + 10)), position)
                    else:
                        self.screen.blit(photo, position)
                # Next button
                if self.current_page < len(self.pages) - 1:
                    self.screen.blit(self.next_button, (self.screen_width - self.next_button.get_width() - 30, self.screen_height - self.next_button.get_height() - 10))
                # Previous button
                if self.current_page > 0:
                    self.screen.blit(self.prev_button, (50, self.screen_height - self.prev_button.get_height() - 10))            
                #bouton de fermeture
                self.screen.blit(self.close_button, (10, 10))

    def toggle(self):
        self.visible = not self.visible



def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    album = PhotoAlbum(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    album.toggle()

            album.handle_event(event)
            album.handle_mouse_motion(event)

        screen.fill((0, 0, 0))

        # Dessiner

        album.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
