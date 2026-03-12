import pygame, ui, mods, random
pygame.init()

class Shop:
    def __init__(self, cx, cy, w, h):
        self.outrect = pygame.rect.Rect(0, 0, w, h)
        self.inrect = pygame.rect.Rect(0, 0, w - 10, h - 10)
        self.outrect.center = [cx, cy]
        self.inrect.center = [cx, cy]
        self.text = ui.Text("Shop", 593, 308, 20, 45, [173, 117, 0])
        self.exitbutton = ui.Button(417, 290, 25, 25, "exitbutton.png")
        self.itempos = []
        self.buybuttons = []
        for i in range(3):
            for n in range(3):
                self.itempos.append([474 + n * 121, 388 + i * 121])
                self.buybuttons.append(ui.Button(474 + n * 121, 448 + i * 121, 75, 30, "buybutton.png", "Buy $10", [163, 139, 0], 65, 20))
        self.items = []
        self.restockshop()


    def renderself(self, screen):
        pygame.draw.rect(screen, [173, 117, 0], self.outrect)
        pygame.draw.rect(screen, [255, 173, 3], self.inrect)

    def rendertext(self, screen):
        self.text.render(screen)

    def renderbutton(self, screen):
        self.exitbutton.render(screen)
        for buybutton in self.buybuttons:
            buybutton.render(screen)

    def renderitems(self, screen):
        for item in self.items:
            item.render(screen)

    def restockshop(self):
        self.items = []
        self.projectilemods = mods.projectilemods.copy()
        self.playermods = mods.playermods.copy()
        self.manamods = mods.manamods.copy()
        for i in range(3):
            self.currentitem = self.projectilemods.pop(random.randint(0, len(self.projectilemods) - 1))
            self.items.append(Item(597, 521, 75, 75, self.currentitem, 1))
        for i in range(3):
            self.currentitem = self.playermods.pop(random.randint(0, len(self.playermods) - 1))
            self.items.append(Item(597, 521, 75, 75, self.currentitem, 1))
        for i in range(3):
            self.currentitem = self.manamods.pop(random.randint(0, len(self.manamods) - 1))
            self.items.append(Item(597, 521, 75, 75, self.currentitem, 1))
        for i in range(len(self.items)):
            self.items[i].cx = self.itempos[i][0]
            self.items[i].cy = self.itempos[i][1]
            self.items[i].rect.center = [self.itempos[i][0], self.itempos[i][1]]

    def update(self, screen):
        self.renderself(screen)
        self.rendertext(screen)
        self.renderitems(screen)
        self.renderbutton(screen)

class Inventory:
    def __init__(self, cx, cy, w, h):
        self.outrect = pygame.rect.Rect(0, 0, w, h)
        self.inrect = pygame.rect.Rect(0, 0, w - 10, h - 10)
        self.outrect.center = [cx, cy]
        self.inrect.center = [cx, cy]
        self.loadouttext = ui.Text("Loadout", 202, 163, 20, 45, [0, 167, 176])
        self.inventorytext = ui.Text("Inventory", 202, 308, 20, 45, [0, 167, 176])
        self.exitbutton = ui.Button(362, 155, 25, 25, "exitbutton.png")
        self.loadoutitempos = []
        for i in range(2):
            for n in range(7):
                self.loadoutitempos.append([52 + n * 50, 212 + i * 50])
        self.itempos = []
        for i in range(5):
            for n in range(6):
                self.itempos.append([77 + n * 50, 362 + i * 50])
        self.items = []
        self.loadout = []


    def renderself(self, screen):
        pygame.draw.rect(screen, [0, 167, 176], self.outrect)
        pygame.draw.rect(screen, [3, 240, 252], self.inrect)

    def rendertext(self, screen):
        self.loadouttext.render(screen)
        self.inventorytext.render(screen)

    def renderbutton(self, screen):
        self.exitbutton.render(screen)


    def renderitems(self, screen):
        for pos in self.loadoutitempos + self.itempos:
            self.slotsurf = pygame.surface.Surface([40, 40], pygame.SRCALPHA)
            self.slotsurf.fill([0, 0, 0, 100])
            self.slotrect = self.slotsurf.get_rect(center=pos)
            screen.blit(self.slotsurf, self.slotrect)
        for item in self.items:
            item.render(screen)


    def update(self, screen):
        self.renderself(screen)
        self.rendertext(screen)
        self.renderitems(screen)
        self.renderbutton(screen)


class Item:
    def __init__(self, cx, cy, w, h, item, level):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.item = item
        self.level = level
        self.image = pygame.image.load(self.item.shopimage)
        self.bgimage = {1 : pygame.image.load("basic.png")}[self.level]
        self.image = pygame.transform.smoothscale(self.image, [self.w - 20, self.h - 20])
        self.bgimage = pygame.transform.smoothscale(self.bgimage, [self.w, self.h])
        self.image.set_colorkey([0, 0, 0])
        self.bgimage.set_colorkey([0, 0, 0])
        self.rect = self.bgimage.get_rect(center=[self.cx, self.cy])
        self.innerrect = self.image.get_rect(center=[self.cx, self.cy])

    def render(self, screen):
        self.rect.centerx = pygame.math.lerp(self.rect.centerx, self.cx, 0.1)
        self.rect.centery = pygame.math.lerp(self.rect.centery, self.cy, 0.1)
        self.innerrect.center = self.rect.center

        screen.blit(self.bgimage, self.rect)
        screen.blit(self.image, self.innerrect)




