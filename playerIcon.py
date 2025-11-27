import pygame
import os



class PlayerIcon:

    def __init__(self,x,y, width,speed =1):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
      

        # Load the spaceship image
        image_path = os.path.join("assets", "Icon.png")
        self.image = pygame.image.load(image_path).convert_alpha()

        # Resize
        self.image = pygame.transform.scale(self.image, (80, 80))

        # Create rect
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shield_active = False
        
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
       

        # Keep inside screen width
        self.rect.x = max(0, min(self.rect.x, self.width - self.rect.width))

    def draw(self, screen):
        if self.shield_active:
            pygame.draw.circle(screen, (0,255,0), self.rect.center, 40, 2)

        screen.blit(self.image, self.rect.topleft)

    def get_rect(self):
        return self.rect