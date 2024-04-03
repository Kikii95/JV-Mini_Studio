class Camera:
    def __init__(self, game):
        self.game = game
        self.right_screen_cap = self.game.screen_width * 4 / 5
        self.left_screen_cap = self.game.screen_width * 1 / 5
        self.top_screen_cap = self.game.screen_height * 1 / 3
        self.down_screen_cap = self.game.screen_height * 4 / 5

    def update(self):
        # Suivre le joueur horizontalement
        if self.game.player.rect.right > self.right_screen_cap:
            self.game.player.rect.x = self.right_screen_cap - self.game.player.perso_width
            delta_x = self.game.player.rect.right - self.right_screen_cap
            self.game.rect.x -= delta_x
            self.game.area1.x -= delta_x
            self.game.area2.x -= delta_x
            self.game.ground_area.x -= delta_x
        elif self.game.player.rect.left < self.left_screen_cap:
            self.game.player.rect.x = self.left_screen_cap
            delta_x = self.left_screen_cap - self.game.player.rect.left
            self.game.rect.x += delta_x
            self.game.area1.x += delta_x
            self.game.area2.x += delta_x
            self.game.ground_area.x += delta_x

        # Suivre le joueur verticalement
        if not self.game.is_grounded and self.game.player.rect.top < self.top_screen_cap:
            delta_y = self.game.player.rect.top - self.top_screen_cap
            self.game.rect.y += delta_y
            self.game.area1.y += delta_y
            self.game.area2.y += delta_y
            self.game.ground_area.y += delta_y
        elif self.game.is_grounded:
            self.game.player.rect.y = self.down_screen_cap - self.game.player.perso_height