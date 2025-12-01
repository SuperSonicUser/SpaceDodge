import pygame
import sys,os,random,json
import enemy
from playerIcon import PlayerIcon
from enemy import Enemy
from user_adaptive_enemies import AdaptiveEnemyManager, update_enemy_pattern

# Initialize pygame
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "SpaceDodge"
FPS = 60
score = 0
font = pygame.font.Font(None, 24)
HIGH_SCORE_PATH = "high_score.json"

def load_high_score():
    try:
        with open(HIGH_SCORE_PATH, "r") as f:
            data = json.load(f)
            return int(data.get("high_score", 0))
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return 0

def save_high_score(value):
    try:
        with open(HIGH_SCORE_PATH, "w") as f:
            json.dump({"high_score": value}, f)
    except OSError:
        pass  # ignore save errors so the game keeps running

high_score = load_high_score()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

bg_img_path = os.path.join("assets","background.png")
background = pygame.image.load(bg_img_path).convert()
background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption(GAME_TITLE) #Game title

player = PlayerIcon(SCREEN_WIDTH//2, SCREEN_HEIGHT-80, SCREEN_WIDTH)

manager = AdaptiveEnemyManager(SCREEN_WIDTH, SCREEN_HEIGHT)
enemies = []
# initial fill
for _ in range(4):
    enemies.append(manager.spawn_enemy(speed=140))
clock=pygame.time.Clock() 


run = True

#Exit screen 

state = "playing"
enemy_speed = 140  # default start speed

def reset_game():
    global score, enemies, player, state, enemy_speed
    score = 0
    enemy_speed = 140
    enemies = [manager.spawn_enemy(speed=enemy_speed) for _ in range(4)]
    player.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-30)
    state = "playing"

def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    msg = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
    hint = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
    screen.blit(msg, msg.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)))
    screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)))




while run:
    
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    pygame.draw.rect(screen,(0,0,0), player)
    delta_time = clock.tick(FPS)/1000.0
    key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif state == "game_over" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                run = False

    if state == "playing":
        player.update(key,delta_time)
        manager.observe_player(key, delta_time)
        manager.maybe_update_pattern()

        # bullet-enemy collisions + scoring
        for bullet in list(player.bullets):
            hit = None
            for enemy in list(enemies):
                if bullet.colliderect(enemy.rect):
                    hit = enemy
                    break
            if hit:
                score += 1
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                player.bullets.remove(bullet)
                enemies.remove(hit)

        # maintain enemy count/speed based on score-driven difficulty
        target_count = max(4, min(12, 4 + int(1 + score / 50)))
        enemy_speed = max(120, min(350, int(120 * (1 + score / 50))))
        while len(enemies) < target_count:
            enemies.append(manager.spawn_enemy(speed=enemy_speed))

        for enemy in enemies:
            enemy.speed = enemy_speed
            update_enemy_pattern(enemy, delta_time)

        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                state = "game_over"
                break

    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_surf.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(score_surf, score_rect)

    high_surf = font.render(f"High Score: {high_score}", True, (200, 200, 200))
    high_rect = high_surf.get_rect(topright=(SCREEN_WIDTH - 10, score_rect.bottom + 5))
    screen.blit(high_surf, high_rect)

    if state == "game_over":
        draw_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()
 
