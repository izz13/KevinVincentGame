import pygame
from pygame.math import Vector2

#Homework make the player spawn at a random square

class Player:
    def __init__(self,square):
        self.localPos = Vector2(square.localRect.center)
        self.worldPos = Vector2(square.worldRect.topleft)
        self.image = pygame.Surface([32,32])
        self.rect = self.image.get_rect(center = self.localPos)
        
