import pygame
import sys
from playerIcon import PlayerIcon

# Initialize pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "SpaceDodge"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

player = PlayerIcon(SCREEN_WIDTH//2, SCREEN_HEIGHT-30, SCREEN_WIDTH, SCREEN_HEIGHT)

run = True

while run:
    
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,0,0), player)

    key = pygame.key.get_pressed()

    player.update(key)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()