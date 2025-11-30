import pygame
import os



class PlayerIcon:

    def __init__(self,x,y, width,speed =500):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
      

        # Load the spaceship image
        image_path = os.path.join("assets", "player.png")
        bullet_path = os.path.join("assets", "bullet.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        self.bullet = pygame.image.load(bullet_path).convert_alpha()
        
        # Resize
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.bullet = pygame.transform.scale(self.bullet,(10,20))


        # Create rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shield_active = False
        
        self.bullets = []
        self.bullet_speed = 500  # pixels per second
        self.shot_cooldown = 0.18  # seconds between shots
        self._cooldown_timer = 0.0
        
    def update(self, keys,dt):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt

        # Shooting (with a small cooldown so you don't spawn hundreds per second)
        self._cooldown_timer -= dt
        if keys[pygame.K_SPACE] and self._cooldown_timer <= 0:
            bullet_rect = self.bullet.get_rect()
            bullet_rect.midbottom = self.rect.midtop
            self.bullets.append(bullet_rect)
            self._cooldown_timer = self.shot_cooldown

        # Move bullets up and remove off-screen ones
        for bullet in list(self.bullets):
            bullet.y -= self.bullet_speed * dt
            if bullet.bottom < 0:
                self.bullets.remove(bullet)
       

        # Keep inside screen width
        self.rect.x = max(0, min(self.rect.x, self.width - self.rect.width))

    def draw(self, screen):
        if self.shield_active:
            pygame.draw.circle(screen, (0,255,0), self.rect.center, 40, 2)

        screen.blit(self.image, self.rect.topleft)
        for bullet in self.bullets:
            screen.blit(self.bullet, bullet.topleft)

    def get_rect(self):
        return self.rect
