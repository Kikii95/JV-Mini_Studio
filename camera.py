class Camera:
    def __init__(self, game):
        self.game = game
        self.CameraX = 0
        self.CameraY = 0

        self.right_screen_cap = self.game.screen_width * 5 / 6
        self.left_screen_cap = self.game.screen_width * 1 / 9
        self.top_screen_cap = self.game.screen_height * 4 / 9
        self.down_screen_cap = self.game.screen_height

    def update(self):
        if self.game.player.rect.x > self.right_screen_cap:
            delta_x = self.game.player.rect.x - self.right_screen_cap
            self.game.player.rect.x = self.right_screen_cap
            self.game.rect1.x -= delta_x
            self.game.rect2.x -= delta_x
            self.game.area1.x -= delta_x


        if self.game.player.rect.x < self.left_screen_cap:
            delta_x = self.left_screen_cap - self.game.player.rect.x
            self.game.player.rect.x = self.left_screen_cap
            self.game.rect1.x += delta_x
            self.game.rect2.x += delta_x
            self.game.area1.x += delta_x

        if self.game.player.rect.y < self.top_screen_cap:
            delta_y = self.top_screen_cap - self.game.player.rect.y
            self.game.player.rect.y = self.top_screen_cap
            self.game.rect1.y += delta_y
            self.game.rect2.y += delta_y
            self.game.area1.y += delta_y
            self.game.area2.y += delta_y


        if self.game.player.rect.y > self.down_screen_cap:
            delta_y = self.game.player.rect.y - self.down_screen_cap
            self.game.player.rect.y = self.down_screen_cap
            self.game.rect1.y -= delta_y
            self.game.rect2.y -= delta_y
            self.game.area1.y -= delta_y
            self.game.area2.y -= delta_y


