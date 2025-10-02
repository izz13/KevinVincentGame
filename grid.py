import pygame
import random

WIDTH = 800
HEIGTH = 640

class Grid:
    def __init__(self, tilesx, tilesy, borderwidth):
        self.squares = []
        for i in range(tilesx):
            x = (WIDTH * i / tilesx) + borderwidth
            w = (WIDTH / tilesx) - (2 * borderwidth)
            for n in range(tilesy):
                y = (HEIGTH * n / tilesy) + borderwidth
                h = (HEIGTH / tilesy) - 2 * borderwidth
                self.squares.append(Squares(x, y, w, h, [200, 200, 200], "Tile.png", [i,n]))
    def render(self, screen):
        for square in self.squares:
            square.render(screen)
class Squares:
    def __init__(self, x, y, w, h, color, image, coords):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.coords = coords
        self.color = color
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.surface = pygame.Surface([self.w, self.h])
        self.surface.fill("green")
        self.surface.set_colorkey("green")
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, [w,h])
        self.image.set_colorkey([0,0,0])

    def render(self, screen):
        screen.blit(self.image, self.rect)
        '''
        if self.coords[0] % 2 == 1 and self.coords[1] % 2 == 1:
            for i in range(15):
                x = random.randint(0, self.w)
                y = random.randint(0, self.h)
                color = random.choice(["green", "salmon", "red"])
                size = random.randint(1,3)
                pygame.draw.circle(self.surface,color,[x,y],size)
        screen.blit(self.surface, self.rect)
        '''




