import pygame
from pygame.math import Vector2


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.direction = Vector2(0)
        self.img = pygame.Surface([64, 64])
        self.img.fill("red")
        self.rect = self.img.get_rect(center=self.pos)
        self.speed = 500

    def update(self, dt):
        self.direction = self.getInput()
        print(self.direction)
        self.pos += self.direction * dt * self.speed
        self.rect.center = self.pos
    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def getInput(self):
        direction = Vector2(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1
        if direction != Vector2(0):
            direction.normalize_ip()
        return direction




