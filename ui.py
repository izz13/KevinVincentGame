import pygame
from pygame import mixer

class Button:
    def __init__(self, centerx, centery, w, h, txtwratio, txthratio, image, sound, text):
        self.centerx = centerx
        self.centery = centery
        self.w = w
        self.h = h
        self.txtwratio = txtwratio
        self.txthratio = txthratio
        self.image = pygame.image.load(image)
        self.sound = sound
        #self.sound = pygame.mixer.Sound(sound)
        self.rect = pygame.rect.Rect(6, 7, self.w, self.h)
        self.txtrect = pygame.rect.Rect(6, 7, self.w * self.txtwratio, self.h * self.txthratio)
        self.rect.center = [self.centerx, self.centery]
        self.txtrect.center = [self.centerx, self.centery]
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.text = text
        self.font = pygame.font.Font("pixelfont.ttf")
        self.fontsurface = self.font.render(self.text, False, [0, 0, 0])
        self.fontsurface = pygame.transform.scale(self.fontsurface, (self.w * self.txtwratio, self.h * self.txthratio))

    def render(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.fontsurface, self.txtrect)
    def update(self, screen):
        self.render(screen)
    def checkcollisions(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

