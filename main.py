from turtle import width
import pygame
import sys,os,random
import enemy
from playerIcon import PlayerIcon
from enemy import Enemy

# Initialize pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "SpaceDodge"
FPS = 60


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_img_path = os.path.join("assets","background.png")
background = pygame.image.load(bg_img_path).convert()
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption(GAME_TITLE) #Game title

player = PlayerIcon(SCREEN_WIDTH//2, SCREEN_HEIGHT-30, SCREEN_WIDTH)

enemies = []
num_enemies = 6
for _ in range(num_enemies):
    enemies.append(Enemy(x=random.randint(0,SCREEN_WIDTH-50),
        y=random.randint(-300,-50),
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        )
        )


clock=pygame.time.Clock() 





run = True

while run:
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    pygame.draw.rect(screen,(0,0,0), player)
    delta_time = clock.tick(FPS)/1000.0
    key = pygame.key.get_pressed()

    player.update(key,delta_time)
    enemy.update(delta_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player.draw(screen)
    enemy.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()