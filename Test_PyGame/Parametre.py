import pygame, sys

class Slider:
    def __init__(self, min_val, max_val, x, y, width, image):
        self.min = min_val
        self.max = max_val
        self.value = min_val
        self.pos = (x, y)
        self.width = width
        self.slider_pos = x
        self.dragging = False
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (40, 40))

    def start_drag(self, x, y):
        if self.pos[0] <= x <= self.pos[0] + self.width and self.pos[1] - 20 <= y <= self.pos[1] + 20:
            self.dragging = True

    def stop_drag(self):
        self.dragging = False

    def draw(self, screen):
        screen.blit(self.image, (self.pos[0] - 50, self.pos[1] - 20))
        pygame.draw.line(screen, WHITE, self.pos, (self.pos[0] + self.width, self.pos[1]), 5)
        pygame.draw.circle(screen, WHITE, (self.slider_pos, self.pos[1]), 10)

    def move(self, x):
        if self.dragging:
            self.slider_pos = max(self.pos[0], min(x, self.pos[0] + self.width))
            self.value = self.min + (self.max - self.min) * ((self.slider_pos - self.pos[0]) / self.width)

class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.pos = (x, y)

    def draw(self, screen):
        draw_text(self.text, *self.pos)

    def is_clicked(self, pos):
        x, y = pos
        text_width, text_height = FONT.size(self.text)
        return self.pos[0] <= x <= self.pos[0] + text_width and self.pos[1] - text_height / 2 <= y <= self.pos[1] + text_height / 2

class Dropdown: 
    def __init__(self, options, x, y):
        self.options = options
        self.current_option = options[0]
        self.pos = (x, y)

    def draw(self, screen):
        draw_text(self.current_option, *self.pos)

    def is_clicked(self, pos):
        x, y = pos
        text_width, text_height = FONT.size(self.current_option)
        return self.pos[0] <= x <= self.pos[0] + text_width and self.pos[1] <= y <= self.pos[1] + text_height

    def next_option(self):
        current_index = self.options.index(self.current_option)
        self.current_option = self.options[(current_index + 1) % len(self.options)]

pygame.init()

screen = pygame.display.set_mode((800, 600))

settings = {
    'volume': 50,
    'resolution': (800, 600),
    'screen_mode': 'Windowed',
    'language': 'English'
}

volume_slider = Slider(0, 100, 330, 50, 200, 'Sound.png')
music_slider = Slider(0, 100, 330, 100, 200, 'Music.png')
language_dropdown = Dropdown(['English', 'Français'], 300, 300)
cancel_button = Button('Cancel', 350, 250)
apply_button = Button('Apply', 450, 300)
FONT = pygame.font.Font(None, 24)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

def draw_text(text, x, y):
    img = FONT.render(text, True, WHITE)
    screen.blit(img, (x, y))

def draw_settings():
    screen.fill(GRAY)
    draw_text("Volume:", 50, 50)
    draw_text(str(int(volume_slider.value)), 550, 50)
    volume_slider.draw(screen)

    draw_text("Music:", 50, 100)
    draw_text(str(int(music_slider.value)), 550, 100)
    music_slider.draw(screen)

    draw_text("Resolution:", 50, 150)
    draw_text("Screen Mode:", 50, 200)
    draw_text("Cancel", 50, 250)
    draw_text("Apply", 50, 300)

    draw_text("<", 300, 150)
    draw_text(f"{settings['resolution'][0]}x{settings['resolution'][1]}", 330, 150)
    draw_text(">", 460, 150)
    draw_text("<", 300, 200)
    draw_text(settings['screen_mode'], 330, 200)
    draw_text(">", 460, 200)

def handle_click(pos):
    x, y = pos
    global settings_open
    if 50 <= x <= 250:
        if 250 <= y <= 285:
            settings_open = False
        elif 300 <= y <= 335:
            apply_settings()
    elif 300 <= x <= 325:
        if 150 <= y <= 185:
            settings['resolution'] = (800, 600) if settings['resolution'] == (1024, 768) else (1024, 768)
        elif 200 <= y <= 235:
            settings['screen_mode'] = "Fullscreen" if settings['screen_mode'] == "Windowed" else "Windowed"
    elif 460 <= x <= 485: 
        if 150 <= y <= 185:
            settings['resolution'] = (1024, 768) if settings['resolution'] == (800, 600) else (800, 600)
        elif 200 <= y <= 235:
            settings['screen_mode'] = "Windowed" if settings['screen_mode'] == "Fullscreen" else "Fullscreen"
    if 300 <= x <= 500 and 45 <= y <= 55:
        volume_slider.move(x)
    if 300 <= x <= 500 and 95 <= y <= 105:
        music_slider.move(x)

def apply_settings():
    global screen
    if settings['screen_mode'] == "Fullscreen":
        screen = pygame.display.set_mode(settings['resolution'], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(settings['resolution'])

running = True

settings_button = Button('Settings', 350, 400)
settings_open = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            volume_slider.start_drag(*pos)
            music_slider.start_drag(*pos)
            if settings_button.is_clicked(pos):
                settings_open = not settings_open
            elif settings_open:
                if cancel_button.is_clicked(pos):
                    pygame.quit()
                    sys.exit()
                elif apply_button.is_clicked(pos):
                    apply_settings()
                elif language_dropdown.is_clicked(pos):
                    language_dropdown.next_option()
                else:
                    handle_click(pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            volume_slider.stop_drag()
            music_slider.stop_drag()
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if volume_slider.dragging:
                volume_slider.move(pos[0])
            if music_slider.dragging:
                music_slider.move(pos[0])

    screen.fill(GRAY)
    settings_button.draw(screen)

    if settings_open:
        settings['volume'] = volume_slider.value
        draw_settings()
    pygame.display.flip()

pygame.quit()