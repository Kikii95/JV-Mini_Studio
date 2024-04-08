import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load('Images/explosion.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)
BLACK = (0, 0, 0)

animation_list = []
animation_steps = 4
last_update = pygame.time.get_ticks()
animation_cooldown = 250
frame = 0

for x in range (animation_steps):
	animation_list.append(sprite_sheet.get_image(x, 32, 32, 6, BLACK))


run = True
while run:

	#update background
	screen.fill(BG)

	current_time = pygame.time.get_ticks()
	if current_time - last_update >= animation_cooldown:
		frame += 1
		last_update = current_time
		if frame >= len(animation_list):
			frame = 0

	#show frame image
	screen.blit(animation_list[frame], (650, 350))

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()