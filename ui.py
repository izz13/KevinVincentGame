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
        if self.text != None:
            self.fontsurface = self.font.render(self.text, False, [0, 0, 0])
            self.fontsurface = pygame.transform.scale(self.fontsurface, (self.w * self.txtwratio, self.h * self.txthratio))

    def render(self, screen):
        screen.blit(self.image, self.rect)
        if self.text != None:
            screen.blit(self.fontsurface, self.txtrect)
    def update(self, screen):
        self.render(screen)
    def checkcollisions(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

class TypeField:
    def __init__(self, centerx, centery, w, h, txtwratio, txthratio, image, label, maxchrs, txtcolor):
        self.centerx = centerx
        self.centery = centery
        self.w = w
        self.h = h
        self.txtwratio = txtwratio
        self.txthratio = txthratio
        self.image = pygame.image.load(image)
        self.rect = pygame.rect.Rect(6, 7, self.w, self.h)
        self.txtrect = pygame.rect.Rect(6, 7, self.w * self.txtwratio, self.h * self.txthratio)
        self.rect.center = [self.centerx, self.centery]
        self.txtrect.center = [self.centerx, self.centery]
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        self.label = label
        self.maxchrs = maxchrs
        self.text = []
        self.font = pygame.font.Font("pixelfont.ttf")
        self.state = "inactive"
        self.txtcolor = txtcolor

    def render(self, screen):
        self.textstr = ""
        for chr in self.text:
            self.textstr += str(chr)
        if self.text != None:
            self.fontsurface = self.font.render(self.label + self.textstr, False, self.txtcolor)
            self.fontsurface = pygame.transform.scale(self.fontsurface, (self.w * self.txtwratio, self.h * self.txthratio))

        screen.blit(self.image, self.rect)
        if self.text != None:
            screen.blit(self.fontsurface, self.txtrect)
    def update(self, screen):
        if self.checkcollisions():
            self.state = "active"
        if pygame.mouse.get_pressed()[0] and not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.state = "inactive"
        if self.state == "active":
            if pygame.key.get_just_pressed()[pygame.K_0] and len(self.text) != self.maxchrs:
                self.text.append(0)
            if pygame.key.get_just_pressed()[pygame.K_1] and len(self.text) != self.maxchrs:
                self.text.append(1)
            if pygame.key.get_just_pressed()[pygame.K_2] and len(self.text) != self.maxchrs:
                self.text.append(2)
            if pygame.key.get_just_pressed()[pygame.K_3] and len(self.text) != self.maxchrs:
                self.text.append(3)
            if pygame.key.get_just_pressed()[pygame.K_4] and len(self.text) != self.maxchrs:
                self.text.append(4)
            if pygame.key.get_just_pressed()[pygame.K_5] and len(self.text) != self.maxchrs:
                self.text.append(5)
            if pygame.key.get_just_pressed()[pygame.K_6] and len(self.text) != self.maxchrs:
                self.text.append(6)
            if pygame.key.get_just_pressed()[pygame.K_7] and len(self.text) != self.maxchrs:
                self.text.append(7)
            if pygame.key.get_just_pressed()[pygame.K_8] and len(self.text) != self.maxchrs:
                self.text.append(8)
            if pygame.key.get_just_pressed()[pygame.K_9] and len(self.text) != self.maxchrs:
                self.text.append(9)
            if pygame.key.get_just_pressed()[pygame.K_BACKSPACE] and len(self.text) != 0:
                self.text.remove(self.text[-1])
        self.render(screen)
    def checkcollisions(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]

def text(centerx, centery, w, h, txt, color, screen):
    font = pygame.font.Font("pixelfont.ttf")
    fontrect = pygame.rect.Rect(6, 7, w, h)
    fontrect.center = [centerx, centery]
    fontsurface = font.render(txt, False, color)
    fontsurface = pygame.transform.scale(fontsurface, (w, h))
    screen.blit(fontsurface, fontrect)