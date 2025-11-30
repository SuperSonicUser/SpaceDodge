import pygame
import os
import random





class Enemy:
    def __init__(self,x,y,screen_width, screen_height,speed=180):
        self.x = x
        self.y = y 
        self.width = screen_width
        self.height = screen_height
        self.speed = speed

        image_path = os.path.join("assets", "enemy.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x,self.y)


    def update(self,dt):
        #enemy moves down to the screen 
        self.rect.y += self.speed * dt

        if self.rect.top > self.height:
            self.rect.x = random.randint(0,self.width - self.rect.width)
            self.rect.y = random.randint(-200,-50)


    def draw(self,screen):
        screen.blit(self.image,self.rect.topleft)