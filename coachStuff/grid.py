import pygame
from pygame.math import Vector2

class Grid:
    def __init__(self,size,gridPercentage = .1):
        self.size = Vector2(size)
        self.squareSize = Vector2(int(self.size[0] * gridPercentage) ,int(self.size[1] * gridPercentage))
        self.rows = int(self.size.y/self.squareSize.y)
        self.cols = int(self.size.x/self.squareSize.x)
        self.squares = self.generateGrid()


    def generateGrid(self):
        squares = []
        for i in range(self.cols):
            for j in range(self.rows):
                pos = Vector2(int(i * self.squareSize.x), int(j * self.squareSize.y))
                s = Square(pos,self.squareSize)
                squares.append(s)
        return squares
    
    def update(self):
        for square in self.squares:
            square.update()

    def draw(self,screen):
        for square in self.squares:
            square.draw(screen)



class Square:
    def __init__(self,pos,size):
        self.pos = Vector2(pos)
        self.size = Vector2(size)
        self.surface = pygame.Surface(self.size)
        self.surface.fill("green")
        self.surface.set_colorkey("green")
        self.object = None
        self.worldRect = self.surface.get_rect(topleft = self.pos)
        self.localRect = self.surface.get_rect()

    def update(self):
        self.worldRect.topleft = self.pos

    def draw(self,screen):
        rectBorder = 3
        pygame.draw.rect(self.surface,"black",self.localRect,rectBorder)
        if self.object != None:
            self.object.draw(self.surface)
        screen.blit(self.surface,self.worldRect)