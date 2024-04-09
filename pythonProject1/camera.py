class Camera:
    def __init__(self, game):
        self.game = game
        self.CameraX = 0
        self.CameraY = 0

        self.right_screen_cap = self.game.screen_width * (4.7 / 7)
        self.left_screen_cap = self.game.screen_width * (1.5 / 6)
        self.top_screen_cap = self.game.screen_height * (2 / 9)
        self.down_screen_cap = self.game.screen_height * (6.5 / 9)

    def update(self):
        if self.game.player.rect.x > self.right_screen_cap:
            delta_x = self.game.player.rect.x - self.right_screen_cap
            self.game.player.rect.x = self.right_screen_cap
            self.game.rect1.x -= delta_x
            self.game.rect2.x -= delta_x
            for platform in self.game.platforms:
                platform[0].x -= delta_x

        if self.game.player.rect.x < self.left_screen_cap:
            delta_x = self.left_screen_cap - self.game.player.rect.x
            self.game.player.rect.x = self.left_screen_cap
            self.game.rect1.x += delta_x
            self.game.rect2.x += delta_x
            for platform in self.game.platforms:
                platform[0].x += delta_x

        if self.game.player.rect.y < self.top_screen_cap:
            delta_y = self.top_screen_cap - self.game.player.rect.y
            self.game.player.rect.y = self.top_screen_cap
            self.game.rect1.y += delta_y
            self.game.rect2.y += delta_y
            for platform in self.game.platforms:
                platform[0].y += delta_y
            self.game.ground.y += delta_y

        if self.game.player.rect.y > self.down_screen_cap:
            delta_y = self.game.player.rect.y - self.down_screen_cap
            self.game.player.rect.y = self.down_screen_cap
            self.game.rect1.y -= delta_y
            self.game.rect2.y -= delta_y
            for platform in self.game.platforms:
                platform[0].y -= delta_y
            self.game.ground.y -= delta_y

    def is_talking(self):
        delta_x = self.game.player.rect.x - self.right_screen_cap
        self.game.player.rect.x = self.right_screen_cap
        self.game.rect1.x -= delta_x
        self.game.rect2.x -= delta_x
        for platform in self.game.platforms:
            platform[0].x -= delta_x

        if self.game.player.rect.y < self.top_screen_cap:
            delta_y = self.top_screen_cap - self.game.player.rect.y
            self.game.player.rect.y = self.top_screen_cap
            self.game.rect1.y += delta_y
            self.game.rect2.y += delta_y
            for platform in self.game.platforms:
                platform[0].y += delta_y
            self.game.ground.y += delta_y

        for i in range(self.down_screen_cap - self.game.player.rect.y):
            delta_y = self.game.player.rect.y - self.down_screen_cap
            self.game.player.rect.y = self.down_screen_cap
            self.game.rect1.y -= delta_y
            self.game.rect2.y -= delta_y
            for platform in self.game.platforms:
                platform[0].y -= delta_y
            self.game.ground.y -= delta_y

        if self.game.player.rect.right < self.right_screen_cap:
            self.game.player.move_character()