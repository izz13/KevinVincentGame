import pygame
pygame.init()

def text(centerx, centery, w, h, txt, color, screen):
    font = pygame.font.Font("pixelfont.ttf")
    fontrect = pygame.rect.Rect(6, 7, w, h)
    fontrect.center = [centerx, centery]
    fontsurface = font.render(str(txt), False, color)
    fontsurface = pygame.transform.scale(fontsurface, (w, h))
    screen.blit(fontsurface, fontrect)

class Button:
    def __init__(self, centerx, centery, w, h, text):
        self.centerx = centerx
        self.centery = centery
        self.w = w
        self.h = h
        self.txtwratio = 0.7
        self.txthratio = 0.8
        self.rect = pygame.rect.Rect(6, 7, self.w, self.h)
        self.txtrect = pygame.rect.Rect(6, 7, self.w * self.txtwratio, self.h * self.txthratio)
        self.rect.center = [self.centerx, self.centery]
        self.txtrect.center = [self.centerx, self.centery]
        self.text = text
        self.font = pygame.font.Font("pixelfont.ttf")
        if self.text != None:
            self.fontsurface = self.font.render(self.text, False, [0, 0, 0])
            self.fontsurface = pygame.transform.scale(self.fontsurface, (self.w * self.txtwratio, self.h * self.txthratio))

    def render(self, screen):
        pygame.draw.rect(screen, [100,100,100], self.rect)
        pygame.draw.rect(screen, [50,50,50], self.rect, 7)
        if self.text != None:
            screen.blit(self.fontsurface, self.txtrect)
    def update(self, screen):
        self.render(screen)
    def checkcollisions(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_just_pressed()[0]


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

class Slider:
    def __init__(self, barcenterx, barcentery, barcolor, barlength, barwidth, initialpercentage, sliderimage, sliderimagew, sliderimageh):
        self.barcenterx = barcenterx
        self.barcentery = barcentery
        self.barcolor = barcolor
        self.barlength = barlength
        self.barwidth = barwidth
        self.initalpercentage = initialpercentage
        self.sliderimage = sliderimage
        self.sliderimagew = sliderimagew
        self.sliderimageh = sliderimageh
        self.image = pygame.image.load(sliderimage)
        self.image = pygame.transform.scale(self.image, (self.sliderimagew, self.sliderimageh))
        self.image.set_colorkey([0, 0, 0])
        self.rect = pygame.rect.Rect(0, 0, self.sliderimagew, self.sliderimageh)
        self.rect.centerx = pygame.math.lerp(self.barcenterx - self.barlength / 2, self.barcenterx + self.barlength / 2, self.initalpercentage)
        self.rect.centery = self.barcentery
        self.hasclicked = True

    def render(self, screen):
        pygame.draw.line(screen, self.barcolor, (self.barcenterx + self.barlength / 2, self.barcentery), (self.barcenterx - self.barlength / 2, self.barcentery), self.barwidth)
        screen.blit(self.image, self.rect)

    def updatepos(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0]:
            self.hasclicked = True
        if not pygame.mouse.get_pressed()[0]:
            self.hasclicked = False
        if self.hasclicked:
            self.rect.centerx = pygame.math.clamp(pygame.mouse.get_pos()[0], self.barcenterx - self.barlength / 2, self.barcenterx + self.barlength / 2)
            self.rect.centery = self.barcentery

    def update(self, screen):
        self.updatepos()
        self.render(screen)

    def findvalue(self, startval, endval):
        self.weight = (self.rect.centerx - (self.barcenterx - self.barlength / 2)) / self.barlength
        return pygame.math.lerp(startval, endval, self.weight)
