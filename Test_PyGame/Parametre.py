import pygame, sys
class Slider:
    def __init__(self, min_val, max_val, x, y, width):
        self.min = min_val
        self.max = max_val
        self.value = min_val
        self.pos = (x, y)
        self.width = width
        self.slider_pos = x  # Initial position of the slider

    def draw(self, screen):
        pygame.draw.line(screen, WHITE, self.pos, (self.pos[0] + self.width, self.pos[1]), 5)
        pygame.draw.circle(screen, WHITE, (self.slider_pos, self.pos[1]), 10)

    def move(self, x):
        self.slider_pos = max(self.pos[0], min(x, self.pos[0] + self.width))
        self.value = self.min + (self.max - self.min) * ((self.slider_pos - self.pos[0]) / self.width)

pygame.init()

volume_slider = Slider(0, 100, 300, 50, 200)  # Create a slider from 0 to 100 at position (300, 50) with width 200
WIDTH, HEIGHT = 800, 600
FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

settings = {
    "volume": 50,
    "resolution": (800, 600),
    "screen_mode": "Windowed"
}

def draw_text(text, x, y):
    img = FONT.render(text, True, WHITE)
    screen.blit(img, (x, y))

def draw_settings():
    screen.fill(GRAY)
    draw_text("Volume:", 50, 50)
    draw_text(str(int(volume_slider.value)), 550, 50)  # Display the volume value
    volume_slider.draw(screen)  # Draw the slider
    draw_text("Resolution:", 50, 100)
    draw_text("Screen Mode:", 50, 150)
    draw_text("Cancel", 50, 200)
    draw_text("Apply", 50, 250)
    draw_text("<", 300, 100)
    draw_text(f"{settings['resolution'][0]}x{settings['resolution'][1]}", 330, 100)
    draw_text(">", 460, 100)
    draw_text("<", 300, 150)
    draw_text(settings['screen_mode'], 330, 150)
    draw_text(">", 460, 150)

def handle_click(pos):
    x, y = pos
    if 50 <= x <= 250:
        if 200 <= y <= 235:
            pygame.quit()
            sys.exit()
        elif 250 <= y <= 285:
            apply_settings()
    elif 300 <= x <= 325:
        if 100 <= y <= 135:
            settings['resolution'] = (800, 600) if settings['resolution'] == (1024, 768) else (1024, 768)
        elif 150 <= y <= 185:
            settings['screen_mode'] = "Fullscreen" if settings['screen_mode'] == "Windowed" else "Windowed"
    elif 460 <= x <= 485: 
        if 100 <= y <= 135:
            settings['resolution'] = (1024, 768) if settings['resolution'] == (800, 600) else (800, 600)
        elif 150 <= y <= 185:
            settings['screen_mode'] = "Windowed" if settings['screen_mode'] == "Fullscreen" else "Fullscreen"
    if 300 <= x <= 500 and 45 <= y <= 55:  # Check if click is within the slider
        volume_slider.move(x)  # Move the slider to the click position
def apply_settings():
    global screen
    if settings['screen_mode'] == "Fullscreen":
        screen = pygame.display.set_mode(settings['resolution'], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(settings['resolution'])

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEMOTION:  # Handle slider movement when mouse is dragged
            if pygame.mouse.get_pressed()[0]:  # If left mouse button is pressed
                handle_click(pygame.mouse.get_pos())

    settings['volume'] = volume_slider.value  # Update the volume setting from the slider value
    draw_settings()
    pygame.display.flip()

pygame.quit()