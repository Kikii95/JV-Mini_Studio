import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images
background_image = pygame.image.load('img/backgroundEndless_JV.png')
character_image = pygame.image.load('img/Perso.png')
shield_image = pygame.image.load('img/ecu.png')
bubble_image = pygame.image.load('img/Bulle.png')

# Scale images
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
character_image = pygame.transform.scale(character_image, (320, 320))
shield_image = pygame.transform.scale(shield_image, (200, 200))
bubble_image = pygame.transform.scale(bubble_image, (1366, 768))

# The bubble image should not be scaled if its dimensions are already 1366x768.
# If it needs to be scaled, uncomment the next line and set the desired dimensions.
# bubble_image = pygame.transform.scale(bubble_image, (desired_width, desired_height))

# Position images
character_rect = character_image.get_rect(midleft=(600, SCREEN_HEIGHT // 2))
shield_rect = shield_image.get_rect(midright=(1400, SCREEN_HEIGHT // 2))
bubble_rect = bubble_image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT))

# Dialogues
dialogues = [
    "You found them? Thank you so much! Thanks to you we can finally travel again!",
    "I remember the time when we first realized the link across Canada !",
    "My name is William and I ushered the National Transcontinental Railway in 1917.",
    "Find your way to Niagara Falls, a mystica\nl group is painting the landscape nearby.",



]

current_dialogue = 0

# Font settings
font_size = 36
font = pygame.font.Font(None, font_size)
text_color = (0, 0, 0)  # Black text

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bubble_rect.collidepoint(event.pos):
                current_dialogue += 1
                if current_dialogue >= len(dialogues):
                    subprocess.run(['python', 'main2.py'])
                    running = False

    # Drawing
    screen.blit(background_image, (0, 0))
    screen.blit(character_image, character_rect)
    screen.blit(shield_image, shield_rect)
    screen.blit(bubble_image, bubble_rect)

    # Draw dialogue text if there is a dialogue to display
    if current_dialogue < len(dialogues):
        text_surface = font.render(dialogues[current_dialogue], True, text_color)
        # Calculate the position of the text. Adjust these values as needed.
        text_x = 900  # Horizontal center
        text_y = 875  # Vertically center in the upper half of the bubble
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
sys.exit()
