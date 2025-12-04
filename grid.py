import pygame
pygame.init()

WIDTH = 750
HEIGTH = 750

class Grid:
    def __init__(self, tilesx, tilesy, borderwidth):
        self.squares = []
        self.tilesx = tilesx
        self.tilesy = tilesy
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
