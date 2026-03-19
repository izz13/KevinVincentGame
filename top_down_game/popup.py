import pygame, ui, mods, random, math
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

    def renderbutton(self, screen, player, inventory):
        self.exitbutton.render(screen)
        for buybutton in self.buybuttons:
            buybutton.render(screen)
            if buybutton.checkcollisions() and player.money >= 10 and len(inventory.items) < 30:
                player.money -= 10
                self.index = self.buybuttons.index(buybutton)
                inventory.items.insert(0, Item(77, 362, 50, 50, self.items[self.index].item, 1))


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

    def update(self, player, inventory, screen):
        self.renderself(screen)
        self.rendertext(screen)
        self.renderitems(screen)
        self.renderbutton(screen, player, inventory)

class Inventory:
    def __init__(self, cx, cy, w, h):
        self.outrect = pygame.rect.Rect(0, 0, w, h)
        self.inrect = pygame.rect.Rect(0, 0, w - 10, h - 10)
        self.outrect.center = [cx, cy]
        self.inrect.center = [cx, cy]
        self.loadouttext = ui.Text("Loadout", 202, 163, 20, 45, [0, 167, 176])
        self.inventorytext = ui.Text("Inventory", 202, 308, 20, 45, [0, 167, 176])
        self.exitbutton = ui.Button(382, 155, 25, 25, "exitbutton.png")
        self.loadoutitempos = []
        for i in range(2):
            for n in range(7):
                self.loadoutitempos.append([40 + n * 55, 212 + i * 55])
        self.itempos = []
        for i in range(5):
            for n in range(6):
                self.itempos.append([65 + n * 55, 362 + i * 55])
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


    def renderitems(self, player, screen):
        for pos in self.loadoutitempos + self.itempos:
            self.slotsurf = pygame.surface.Surface([50, 50], pygame.SRCALPHA)
            self.slotsurf.fill([0, 0, 0, 100])
            self.slotrect = self.slotsurf.get_rect(center=pos)
            screen.blit(self.slotsurf, self.slotrect)
        for num in range(len(self.items)):
            self.items[num].render(screen)
            self.items[num].move(self.itempos[num][0], self.itempos[num][1], self.items + self.loadout)
        for num in range(len(self.loadout)):
            self.loadout[num].render(screen)
            self.loadout[num].move(self.loadoutitempos[num][0], self.loadoutitempos[num][1], self.items + self.loadout)

        for item in self.items:
            for pos in self.loadoutitempos:
                if math.dist(pos, item.rect.center) <= 30 and item.state == "not clicked" and len(self.loadout) < 14:
                    try:
                        self.loadout.insert(0, item)
                        player.addmods([item.item, item.level])
                        self.items.remove(item)
                    except:
                        pass


        for item in self.loadout:
            for pos in self.itempos:
                if math.dist(pos, item.rect.center) <= 30 and item.state == "not clicked" and len(self.items) < 30:
                    try:
                        self.items.insert(0, item)
                        player.removemod(item.item, item.level)
                        self.loadout.remove(item)
                    except:
                        pass




    def update(self, player, screen):
        self.renderself(screen)
        self.rendertext(screen)
        self.renderitems(player, screen)
        self.renderbutton(screen)

class Forge:
    def __init__(self, cx, cy, w, h):
        self.outrect = pygame.rect.Rect(0, 0, w, h)
        self.inrect = pygame.rect.Rect(0, 0, w - 10, h - 10)
        self.outrect.center = [cx, cy]
        self.inrect.center = [cx, cy]
        self.text = ui.Text("Shop", 593, 308, 20, 45, [173, 117, 0])
        self.exitbutton = ui.Button(96, 155, 25, 25, "exitbutton.png")
        self.itempos = []
        self.buybuttons = []
        for i in range(3):
            for n in range(3):
                self.itempos.append([474 + n * 121, 388 + i * 121])
                self.buybuttons.append(ui.Button(474 + n * 121, 448 + i * 121, 75, 30, "buybutton.png", "Buy $10", [163, 139, 0], 65, 20))
        self.items = []


    def renderself(self, screen):
        pygame.draw.rect(screen, [112, 112, 112], self.outrect)
        pygame.draw.rect(screen, [148, 148, 148], self.inrect)

    def rendertext(self, screen):
        self.text.render(screen)

    def renderbutton(self, screen, player, inventory):
        self.exitbutton.render(screen)



    def renderitems(self, screen):
        for item in self.items:
            item.render(screen)

    def update(self, player, inventory, screen):
        self.renderself(screen)
        #self.rendertext(screen)
        #self.renderitems(screen)
        self.renderbutton(screen, player, inventory)


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
        self.image = pygame.transform.scale(self.image, [self.w - 20, self.h - 20])
        self.bgimage = pygame.transform.smoothscale(self.bgimage, [self.w, self.h])
        self.image.set_colorkey([0, 0, 0])
        self.bgimage.set_colorkey([0, 0, 0])
        self.rect = self.bgimage.get_rect(center=[self.cx, self.cy])
        self.innerrect = self.image.get_rect(center=[self.cx, self.cy])
        self.state = "not clicked"

    def render(self, screen):
        self.innerrect.center = self.rect.center

        screen.blit(self.bgimage, self.rect)
        screen.blit(self.image, self.innerrect)

    def move(self, cx, cy, items):
        if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0] and self.state == "not clicked":
            self.state = "clicked"
            for item in items:
                if item.state == "clicked" and item != self:
                    self.state = "not clicked"

        if self.state == "clicked":
            self.cx = pygame.mouse.get_pos()[0]
            self.cy = pygame.mouse.get_pos()[1]
            if not pygame.mouse.get_pressed()[0]:
                self.state = "not clicked"
        else:
            self.cx = cx
            self.cy = cy
        self.rect.centerx = round(pygame.math.lerp(self.rect.centerx, self.cx, 0.3))
        self.rect.centery = round(pygame.math.lerp(self.rect.centery, self.cy, 0.3))



