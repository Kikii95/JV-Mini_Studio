import pygame, sys

pygame.init()

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
    draw_text("Resolution:", 50, 100)
    draw_text("Screen Mode:", 50, 150)
    draw_text("Cancel", 50, 200)
    draw_text("Apply", 50, 250)
    draw_text("<", 300, 50)
    draw_text(str(settings['volume']), 350, 50)
    draw_text(">", 410, 50)
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
        if 50 <= y <= 85:
            settings['volume'] = max(0, settings['volume'] - 10)
        elif 100 <= y <= 135:
            settings['resolution'] = (800, 600) if settings['resolution'] == (1024, 768) else (1024, 768)
        elif 150 <= y <= 185:
            settings['screen_mode'] = "Fullscreen" if settings['screen_mode'] == "Windowed" else "Windowed"
    elif 460 <= x <= 485: 
        if 100 <= y <= 135:
            settings['resolution'] = (1024, 768) if settings['resolution'] == (800, 600) else (800, 600)
        elif 150 <= y <= 185:
            settings['screen_mode'] = "Windowed" if settings['screen_mode'] == "Fullscreen" else "Fullscreen"


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

    draw_settings()
    pygame.display.flip()

pygame.quit()