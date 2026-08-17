import pygame, ui
pygame.init()

class Bar:
    def __init__(self, cx, cy, w, h, image, padx=10, pady=10):
        self.cx = cx
        self.cy = cy
        self.center = [self.cx, self.cy]
        self.w = w
        self.h = h
        self.exteriorrect = pygame.rect.Rect(0, 0, self.w, self.h)
        self.exteriorrect.center = self.center
        self.image = pygame.image.load(image)
        self.padx = padx
        self.pady = pady
        self.image = pygame.transform.scale(self.image, [self.w - self.padx, self.h - self.pady])
        self.image.set_colorkey([0, 0, 0])
        self.barrect = self.image.get_rect(center=self.center)

    def render(self, screen, amount):
        self.exteriorrect = pygame.rect.Rect(0, 0, self.w, self.h)
        self.exteriorrect.center = self.center
        self.barrect = self.image.get_rect(center=self.center)
        self.coversurface = pygame.surface.Surface([self.w - self.padx, self.h - self.pady])
        self.coversurface.fill([0, 0, 0])
        self.coverrect = pygame.rect.Rect(0, 0, pygame.math.lerp(0, self.w - self.padx, amount), self.h - self.pady)
        pygame.draw.rect(self.coversurface, [255, 255, 255], self.coverrect)
        self.coversurface.set_colorkey([255, 255, 255])
        self.newimage = self.image.copy()
        self.newimage.blit(self.coversurface, (0,0))
        self.newimage.set_colorkey([0, 0, 0])
        pygame.draw.rect(screen, [100, 100, 100], self.exteriorrect)
        screen.blit(self.newimage, self.barrect)

class Text:
    def __init__(self, text, cx, cy, charw, charh, color, wrap=0):
        self.text = text
        self.cx = cx
        self.cy = cy
        self.charw = round(charw)
        self.charh = round(charh)
        self.color = color
        self.wrap = wrap


    def render(self, screen, camerapos=None):
        self.textfont = pygame.font.Font("sansserif.ttf")
        if self.wrap != 0:
            self.textsurface = self.textfont.render(self.text, True, self.color, None, self.wrap * self.charw)
            self.textsurface = pygame.transform.smoothscale(self.textsurface, [self.charw * self.wrap, self.charh * (len(self.text) // self.wrap)])
        else:
            self.textsurface = self.textfont.render(self.text, True, self.color, None)
            self.textsurface = pygame.transform.smoothscale(self.textsurface, [len(self.text) * self.charw, self.charh])
        self.rect = self.textsurface.get_rect(center=[self.cx, self.cy])
        if camerapos == None:
            screen.blit(self.textsurface, self.rect)
        else:
            screen.blit(self.textsurface, self.rect.topleft - camerapos)

class Button:
    def __init__(self, cx, cy, w, h, image, text=" ", color=[0,0,0], tw=0, th=0, isui=True):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, [self.w, self.h])
        self.rect = self.image.get_rect(center=[self.cx, self.cy])
        self.text = text
        self.color = color
        self.tw = tw
        self.th = th
        self.text = ui.Text(self.text, self.cx, self.cy, self.tw / len(text), self.th, self.color)
        self.isui = isui

    def render(self, screen, camerapos=None):
        if camerapos == None:
            screen.blit(self.image, self.rect)
            self.text.render(screen)
        else:
            screen.blit(self.image, self.rect.topleft - camerapos)
            self.text.render(screen, camerapos)

    def checkcollisions(self, player=None):
        if self.isui:
            return self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_just_pressed()[0]
        else:
            return self.rect.colliderect(player.rect)