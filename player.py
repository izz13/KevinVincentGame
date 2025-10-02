import pygame
import random
from spritesheet import SpriteSheet
import math
from pygame import PixelArray

WIDTH = 800
HEIGTH = 640

class Player:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, [w, h])
        self.image.set_colorkey([0,0,0])
        self.state = "idle"
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.aniframes = 0
        self.pastaniframes = 0


    def render(self, screen):
        #pygame.draw.rect(screen, "red", self.rect)
        screen.blit(self.image, self.rect)

    def checkcollisions(self, walls, xvel, yvel, pushables, tilesx, tilesy, doors, robots):
        if self.coordsx + xvel < 0 or self.coordsx + xvel > tilesx - 1 or self.coordsy + yvel < 0 or self.coordsy + yvel > tilesy - 1:
            return False
        if walls == []:
            return True
        else:
            for obstacle in walls:
                if [self.coordsx + xvel, self.coordsy + yvel] == [obstacle.coordsx, obstacle.coordsy]:
                    return False
            for door in doors:
                if [self.coordsx + xvel, self.coordsy + yvel] == [door.coordsx, door.coordsy] and door.frame == 1:
                    return False
            if pushables != []:
                for pushable in pushables + robots:
                    if math.dist([self.coordsx + xvel, self.coordsy + yvel], [pushable.coordsx, pushable.coordsy]) <= 0.00000001:
                        for obstacle in walls + pushables + robots:
                            if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy]:
                                return False
                            if self.coordsx + xvel * 2 < 0 or self.coordsx + xvel * 2 > tilesx - 1 or self.coordsy + yvel * 2 < 0 or self.coordsy + yvel * 2 > tilesy - 1:
                                return False
                        for obstacle in doors:
                            if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy] and obstacle.frame == 1:
                                return False
            if robots != []:
                for robot in robots:
                    if [self.coordsx + xvel, self.coordsy + yvel] == [robot.coordsx, robot.coordsy] and robot.state != "idle":
                        return False
            return True
    def updatepush(self, pushables, robots, xvel, yvel): #This took way to long 😭
        if pushables != []:
            for pushable in pushables:
                if math.dist([self.coordsx + xvel, self.coordsy + yvel], [pushable.coordsx, pushable.coordsy]) <= 0.00000001:
                    pushable.move(xvel / 15, yvel / 15)
                if self.aniframes - self.pastaniframes == 15:
                    pushable.coordsx = round(pushable.coordsx)
                    pushable.coordsy = round(pushable.coordsy)
        if robots != []:
            for robot in robots:
                if math.dist([self.coordsx + xvel, self.coordsy + yvel], [robot.coordsx, robot.coordsy]) <= 0.00000001:
                    robot.coordsx += xvel / 15
                    robot.coordsy += yvel / 15
                if self.aniframes - self.pastaniframes == 15:
                    robot.coordsx = round(robot.coordsx)
                    robot.coordsy = round(robot.coordsy)

    def updatepos(self, walls, pushables, doors, robots):
        self.aniframes += 1
        if self.state == "idle":
            if pygame.key.get_pressed()[pygame.K_UP]:
                if self.checkcollisions(walls, 0, -1, pushables, self.tilesx, self.tilesy, doors, robots):
                    self.state = "movingup"
                    self.pastaniframes = self.aniframes
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if self.checkcollisions(walls, 0, 1, pushables, self.tilesx, self.tilesy, doors, robots):
                    self.state = "movingdown"
                    self.pastaniframes = self.aniframes
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if self.checkcollisions(walls, -1, 0, pushables, self.tilesx, self.tilesy, doors, robots):
                    self.state = "movingleft"
                    self.pastaniframes = self.aniframes
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if self.checkcollisions(walls, 1, 0, pushables, self.tilesx, self.tilesy, doors, robots):
                    self.state = "movingright"
                    self.pastaniframes = self.aniframes
        if self.state == "movingup":
            if self.aniframes - self.pastaniframes > 15:
                self.state = "movecooldown"
                self.pastaniframes = self.aniframes
            else:
                self.updatepush(pushables, robots, 0, -1)
                self.coordsy -= 1 / 15
        if self.state == "movingdown":
            if self.aniframes - self.pastaniframes > 15:
                self.state = "movecooldown"
                self.pastaniframes = self.aniframes
            else:
                self.updatepush(pushables, robots, 0, 1)
                self.coordsy += 1 / 15
        if self.state == "movingleft":
            if self.aniframes - self.pastaniframes > 15:
                self.state = "movecooldown"
                self.pastaniframes = self.aniframes
            else:
                self.updatepush(pushables, robots, -1, 0)
                self.coordsx -= 1 / 15
        if self.state == "movingright":
            if self.aniframes - self.pastaniframes > 15:
                self.state = "movecooldown"
                self.pastaniframes = self.aniframes
            else:
                self.updatepush(pushables, robots, 1, 0)
                self.coordsx += 1 / 15
        if self.state == "movecooldown":
            self.coordsx = round(self.coordsx)
            self.coordsy = round(self.coordsy)
            #print(self.coordsx, self.coordsy)
            if self.aniframes - self.pastaniframes >= 2:
                self.state = "idle"
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)

    def update(self, screen, walls, pushables, doors, robots):
        self.updatepos(walls, pushables, doors, robots)
        self.render(screen)

class Flag:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilexy = tilesy
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, [self.w, self.h])
        self.image.set_colorkey([0,0,0])
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / tilesx, self.coordsy * HEIGTH / tilesy, w, h)

    def render(self, screen):
        screen.blit(self.image, self.rect)

class Wall:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilexy = tilesy
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, [self.w, self.h])
        self.image.set_colorkey([0,0,0])
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / tilesx, self.coordsy * HEIGTH / tilesy, w, h)

    def render(self, screen):
        screen.blit(self.image, self.rect)

class Pushable:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, frame, command=None, dir = 0, color=[0,1,6]):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.spritesheet = SpriteSheet(image)
        self.frame = frame
        self.image = self.spritesheet.get_sprite(self.frame, 32, 32, self.w, self.h)
        self.pixelarray = PixelArray(self.image)
        self.pixelarray.replace((255, 255, 255), tuple(color))
        self.image = self.pixelarray.make_surface()
        self.pixelarray = None
        self.image = pygame.transform.rotate(self.image, dir)
        self.image = pygame.transform.scale(self.image, [self.w, self.h])
        self.image.set_colorkey([0, 0, 0])
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.command = command

    def update(self, screen):
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.render(screen)
    def move(self, xvel, yvel):
        self.coordsx += xvel
        self.coordsy += yvel

    def render(self, screen):
        screen.blit(self.image, self.rect)

class Door:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, frame, color):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.image = image
        self.frame = frame
        if self.frame == 0:
            self.type = "plate"
        else:
            self.type = "door"
        self.color = color
        self.pixelarray = PixelArray(pygame.image.load(self.image))
        self.pixelarray.replace((255, 255, 255), tuple(color))
        self.spritesheet = SpriteSheet(self.pixelarray.make_surface(), False)
        self.rect = pygame.rect.Rect(coordsx * WIDTH / tilesx, coordsy * HEIGTH / tilesy, w, h)

    def render(self, screen):
        screen.blit(self.spritesheet.get_sprite(self.frame, 32, 32, self.w, self.h), self.rect)

    def update(self, screen, pushables, players, doors, robots):
        self.render(screen)
        self.updatestate(pushables, players, doors, robots)

    def updatestate(self, pushables, players, doors, robots):
        if self.frame == 0:
            self.activate = False
            for interactable in pushables + [players] + robots:
                if interactable.coordsx == self.coordsx and interactable.coordsy == self.coordsy:
                    self.activate = True
            for door in doors:
                if door.frame != 0 and door.color == self.color:
                    if self.activate:
                        door.frame = 2
                    else:
                        door.frame = 1
class Robot:
        def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, color):
            self.coordsx = coordsx
            self.coordsy = coordsy
            self.w = w
            self.h = h
            self.tilesx = tilesx
            self.tilesy = tilesy
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(self.image, [w, h])
            self.image.set_colorkey([0, 0, 0])
            self.state = "idle"
            self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
            self.aniframes = 0
            self.pastaniframes = 0
            self.move = None
            self.color = color
            self.pixelarray = PixelArray(self.image)
            self.pixelarray.replace((255, 255, 255), tuple(self.color))
            self.image = self.pixelarray.make_surface()
            self.pixelarray = None

        def render(self, screen):
            # pygame.draw.rect(screen, "red", self.rect)
            screen.blit(self.image, self.rect)

        def checkcollisions(self, walls, xvel, yvel, pushables, tilesx, tilesy, doors):
            if self.coordsx + xvel < 0 or self.coordsx + xvel > tilesx - 1 or self.coordsy + yvel < 0 or self.coordsy + yvel > tilesy - 1:
                return False
            if walls == []:
                return True
            else:
                for obstacle in walls:
                    if [self.coordsx + xvel, self.coordsy + yvel] == [obstacle.coordsx, obstacle.coordsy]:
                        return False
                for door in doors:
                    if [self.coordsx + xvel, self.coordsy + yvel] == [door.coordsx, door.coordsy] and door.frame == 1:
                        return False
                if pushables != []:
                    for pushable in pushables:
                        if math.dist([self.coordsx + xvel, self.coordsy + yvel],
                                     [pushable.coordsx, pushable.coordsy]) <= 0.00000001:
                            for obstacle in walls + pushables:
                                if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx,
                                                                                          obstacle.coordsy]:
                                    return False
                                if self.coordsx + xvel * 2 < 0 or self.coordsx + xvel * 2 > tilesx - 1 or self.coordsy + yvel * 2 < 0 or self.coordsy + yvel * 2 > tilesy - 1:
                                    return False
                            for obstacle in doors:
                                if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy] and obstacle.frame == 1:
                                    return False

                return True

        def updatepush(self, pushables, xvel, yvel):
            if pushables != []:
                for pushable in pushables:
                    if math.dist([self.coordsx + xvel, self.coordsy + yvel],
                                 [pushable.coordsx, pushable.coordsy]) <= 0.00000001:
                        pushable.move(xvel / 15, yvel / 15)
                    if self.aniframes - self.pastaniframes == 15:
                        pushable.coordsx = round(pushable.coordsx)
                        pushable.coordsy = round(pushable.coordsy)

        def updatepos(self, walls, pushables, doors):
            self.aniframes += 1
            if self.state == "idle":
                if self.move == "up":
                    if self.checkcollisions(walls, 0, -1, pushables, self.tilesx, self.tilesy, doors):
                        self.state = "movingup"
                        self.pastaniframes = self.aniframes
                if self.move == "down":
                    if self.checkcollisions(walls, 0, 1, pushables, self.tilesx, self.tilesy, doors):
                        self.state = "movingdown"
                        self.pastaniframes = self.aniframes
                if self.move == "left":
                    if self.checkcollisions(walls, -1, 0, pushables, self.tilesx, self.tilesy, doors):
                        self.state = "movingleft"
                        self.pastaniframes = self.aniframes
                if self.move == "right":
                    if self.checkcollisions(walls, 1, 0, pushables, self.tilesx, self.tilesy, doors):
                        self.state = "movingright"
                        self.pastaniframes = self.aniframes
                self.move = None
            if self.state == "movingup":
                if self.aniframes - self.pastaniframes > 15:
                    self.state = "movecooldown"
                    self.pastaniframes = self.aniframes
                else:
                    self.updatepush(pushables, 0, -1)
                    self.coordsy -= 1 / 15
            if self.state == "movingdown":
                if self.aniframes - self.pastaniframes > 15:
                    self.state = "movecooldown"
                    self.pastaniframes = self.aniframes
                else:
                    self.updatepush(pushables, 0, 1)
                    self.coordsy += 1 / 15
            if self.state == "movingleft":
                if self.aniframes - self.pastaniframes > 15:
                    self.state = "movecooldown"
                    self.pastaniframes = self.aniframes
                else:
                    self.updatepush(pushables, -1, 0)
                    self.coordsx -= 1 / 15
            if self.state == "movingright":
                if self.aniframes - self.pastaniframes > 15:
                    self.state = "movecooldown"
                    self.pastaniframes = self.aniframes
                else:
                    self.updatepush(pushables, 1, 0)
                    self.coordsx += 1 / 15
            if self.state == "movecooldown":
                self.coordsx = round(self.coordsx)
                self.coordsy = round(self.coordsy)
                # print(self.coordsx, self.coordsy)
                if self.aniframes - self.pastaniframes >= 2:
                    self.state = "idle"
            self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)

        def update(self, screen, walls, pushables, doors):
            self.updatepos(walls, pushables, doors)
            self.render(screen)

class ProgramHeader:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, spritesheet, frame1, frame2, dir, color):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.spritesheet = SpriteSheet(spritesheet)
        self.frame1 = frame1
        self.frame2 = frame2
        # IMAGEBASE
        self.imagebase = self.spritesheet.get_sprite(self.frame1, 32, 32, self.w, self.h)
        self.pixelarray = PixelArray(self.imagebase)
        self.pixelarray.replace((255, 255, 255), tuple(color))
        self.imagebase = self.pixelarray.make_surface()
        self.imagebase = pygame.transform.scale(self.imagebase, [self.w, self.h])
        self.pixelarray = None
        self.imagebase = pygame.transform.rotate(self.imagebase, dir)
        self.imagebase.set_colorkey([0, 0, 0])
        # IMAGEARROW
        self.imagearrow = self.spritesheet.get_sprite(self.frame2, 32, 32, self.w, self.h)
        self.image = pygame.transform.scale(self.imagearrow, [self.w, self.h])
        self.imagearrow.set_colorkey([0, 0, 0])

        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.command = None
        self.dir = dir
        self.color = color

    def update(self, screen):
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.render(screen)
    def move(self, xvel, yvel):
        self.coordsx += xvel
        self.coordsy += yvel

    def render(self, screen):
        screen.blit(self.imagebase, self.rect)
        screen.blit(self.imagearrow, self.rect)
