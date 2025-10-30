import pygame
from spritesheet import SpriteSheet
import math
from pygame import PixelArray

WIDTH = 750
HEIGTH = 750
class Player:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.imageName = image
        self.frontImage = pygame.image.load("FrontPOV.png")
        self.backImage = pygame.image.load("BackPOV.png")
        self.sideImage = pygame.image.load("SidePOV.png")
        self.image = self.frontImage
        self.image = pygame.transform.scale(self.image, [w, h])
        self.image.set_colorkey([0,0,0])
        self.state = "idle"
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.aniframes = 0
        self.pastaniframes = 0
        self.facing = "Front"
        self.reverseSideImage = pygame.transform.flip(self.sideImage, True, False)
        self.gridx = coordsx
        self.gridy = coordsy

    def copy(self):
        return Player(self.coordsx, self.coordsy, self.w, self.h, self.tilesx, self.tilesy, self.image)

    def render(self, screen):
        if self.state == "movingdown":
            screen.blit(self.frontImage, self.rect)
        if self.state == "movingleft":
            screen.blit(self.reverseSideImage, self.rect)
        if self.state == "movingright":
            screen.blit(self.sideImage, self.rect)
        if self.state == "movingup":
            screen.blit(self.backImage, self.rect)
        if self.state == "idle":
            screen.blit(self.image, self.rect)


    def checkcollisions(self, walls, xvel, yvel, pushables, tilesx, tilesy, doors, robots, gates):
        if self.coordsx + xvel < 0 or self.coordsx + xvel > tilesx - 1 or self.coordsy + yvel < 0 or self.coordsy + yvel > tilesy - 1:
            return False
        if walls != []:
            for obstacle in walls:
                if [self.coordsx + xvel, self.coordsy + yvel] == [obstacle.coordsx, obstacle.coordsy]:
                    return False
        for door in doors:
            if [self.coordsx + xvel, self.coordsy + yvel] == [door.coordsx, door.coordsy] and door.frame == 1:
                return False
        for gate in gates:
            if [self.coordsx + xvel, self.coordsy + yvel] == [gate.coordsx, gate.coordsy] and gate.passables != "player":
                return False
        if pushables + robots != []:
            self.check1 = None
            self.check2 = None
            for pushable in pushables:
                if [self.coordsx + xvel, self.coordsy + yvel] == [pushable.coordsx, pushable.coordsy]:
                    self.check1 = pushable
                elif [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [pushable.coordsx, pushable.coordsy]:
                    self.check2 = pushable
            if self.check1 != None and self.check2 != None and self.check1.frame == 3 and self.check2.frame == 4:
                return True

            for pushable in pushables + robots:
                if [self.coordsx + xvel, self.coordsy + yvel] == [pushable.coordsx, pushable.coordsy]:
                    for obstacle in walls + pushables + robots:
                        if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy]:
                            return False
                    if self.coordsx + xvel * 2 < 0 or self.coordsx + xvel * 2 > tilesx - 1 or self.coordsy + yvel * 2 < 0 or self.coordsy + yvel * 2 > tilesy - 1:
                        return False
                    for obstacle in doors:
                        if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy] and obstacle.frame == 1:
                            return False
                    for gate in gates:
                        if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [gate.coordsx, gate.coordsy]:
                            if str(type(pushable)) != "<class 'player.Robot'>":
                                return False
                            elif pushable.color != gate.passablecolor:
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

    def updatepos(self, walls, pushables, doors, robots, gates):
        self.aniframes += 1
        if self.state == "idle":
            if pygame.key.get_pressed()[pygame.K_UP]:
                if self.checkcollisions(walls, 0, -1, pushables, self.tilesx, self.tilesy, doors, robots, gates):
                    self.state = "movingup"
                    self.pastaniframes = self.aniframes
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if self.checkcollisions(walls, 0, 1, pushables, self.tilesx, self.tilesy, doors, robots, gates):
                    self.state = "movingdown"
                    self.pastaniframes = self.aniframes
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if self.checkcollisions(walls, -1, 0, pushables, self.tilesx, self.tilesy, doors, robots, gates):
                    self.state = "movingleft"
                    self.pastaniframes = self.aniframes
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if self.checkcollisions(walls, 1, 0, pushables, self.tilesx, self.tilesy, doors, robots, gates):
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
            self.gridx = self.coordsx
            self.gridy = self.coordsy
            if self.aniframes - self.pastaniframes >= 2:
                self.state = "idle"
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)

    def update(self, screen, walls, pushables, doors, robots, gates):
        self.updatepos(walls, pushables, doors, robots, gates)
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
        self.imageName = image
        self.spritesheet = SpriteSheet(self.imageName)
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
        self.dir = dir
        self.color = color

    def update(self, screen):
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.render(screen)
    def move(self, xvel, yvel):
        self.coordsx += xvel
        self.coordsy += yvel

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def copy(self):
        return Pushable(self.coordsx, self.coordsy, self.w, self.h, self.tilesx, self.tilesy, self.imageName, self.frame, self.command, self.dir, self.color)

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
            if players != None:
                for interactable in pushables + [players] + robots:
                    try:
                        if interactable.coordsx == self.coordsx and interactable.coordsy == self.coordsy:
                            self.activate = True
                    except:
                        print(type(interactable))
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
            self.ogimage = pygame.image.load(image)
            self.ogimage = pygame.transform.scale(self.ogimage, [w, h])
            self.ogimage.set_colorkey([0, 0, 0])
            self.state = "idle"
            self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
            self.aniframes = 0
            self.pastaniframes = 0
            self.move = None
            self.color = color
            self.gridx = self.coordsx
            self.gridy = self.coordsy

        def render(self, screen):
            self.pixelarray = PixelArray(self.ogimage.copy())
            self.pixelarray.replace((255, 255, 255), tuple(self.color))
            self.image = self.pixelarray.make_surface()
            self.pixelarray = None
            screen.blit(self.image, self.rect)

        def checkcollisions(self, walls, xvel, yvel, pushables, tilesx, tilesy, doors, player, robots, gates):
            if self.coordsx + xvel < 0 or self.coordsx + xvel > tilesx - 1 or self.coordsy + yvel < 0 or self.coordsy + yvel > tilesy - 1:
                return False
            if walls != []:
                for obstacle in walls + [player]:
                    if [self.coordsx + xvel, self.coordsy + yvel] == [obstacle.coordsx, obstacle.coordsy]:
                        return False
            for door in doors:
                if [self.coordsx + xvel, self.coordsy + yvel] == [door.coordsx, door.coordsy] and door.frame == 1:
                    return False
            for gate in gates:
                if [self.coordsx + xvel, self.coordsy + yvel] == [gate.coordsx, gate.coordsy] and gate.passablecolor != self.color:
                    return False
            if robots != []:
                for robot in robots:
                    if [self.coordsx + xvel, self.coordsy + yvel] == [robot.coordsx, robot.coordsy] and robot.state != "idle":
                        return False
            if pushables + robots != []:
                self.check1 = None
                self.check2 = None
                for pushable in pushables:
                    if [self.coordsx + xvel, self.coordsy + yvel] == [pushable.coordsx, pushable.coordsy]:
                        self.check1 = pushable
                    elif [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [pushable.coordsx, pushable.coordsy]:
                        self.check2 = pushable
                if self.check1 != None and self.check2 != None and self.check1.frame == 3 and self.check2.frame == 4:
                    return True
                for pushable in pushables + robots:
                    if [self.coordsx + xvel, self.coordsy + yvel ] == [pushable.coordsx, pushable.coordsy]:
                        for obstacle in walls + pushables:
                            if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy]:
                                return False
                            if self.coordsx + xvel * 2 < 0 or self.coordsx + xvel * 2 > tilesx - 1 or self.coordsy + yvel * 2 < 0 or self.coordsy + yvel * 2 > tilesy - 1:
                                return False
                        for obstacle in doors:
                            if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [obstacle.coordsx, obstacle.coordsy] and obstacle.frame == 1:
                                return False
                for gate in gates:
                    if [self.coordsx + xvel * 2, self.coordsy + yvel * 2] == [gate.coordsx, gate.coordsy]:
                        if str(type(pushable)) != "<class 'player.Robot'>":
                            return False
                        elif pushable.color != gate.passablecolor:
                            return False

            return True

        def updatepush(self, pushables, robots, xvel, yvel):  # This took way to long 😭
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

        def updatepos(self, walls, pushables, doors, player, robots, gates):
            self.aniframes += 1
            if self.state == "idle":
                if self.move == "up":
                    if self.checkcollisions(walls, 0, -1, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                        self.state = "movingup"
                        self.pastaniframes = self.aniframes
                if self.move == "down":
                    if self.checkcollisions(walls, 0, 1, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                        self.state = "movingdown"
                        self.pastaniframes = self.aniframes
                if self.move == "left":
                    if self.checkcollisions(walls, -1, 0, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                        self.state = "movingleft"
                        self.pastaniframes = self.aniframes
                if self.move == "right":
                    if self.checkcollisions(walls, 1, 0, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                        self.state = "movingright"
                        self.pastaniframes = self.aniframes
                self.move = None
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
                self.gridx = self.coordsx
                self.gridy = self.gridy
                if self.aniframes - self.pastaniframes >= 2:
                    self.state = "idle"
            self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)

        def update(self, screen, walls, pushables, doors, player, robots, gates):
            self.updatepos(walls, pushables, doors, player, robots, gates)
            self.render(screen)

class ProgramHeader:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, spritesheet, frame, frame2, dir, color):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.imageName = spritesheet
        self.spritesheet = SpriteSheet(self.imageName)
        self.frame = frame
        self.frame2 = frame2
        # IMAGEBASE
        self.imagebase = self.spritesheet.get_sprite(self.frame, 32, 32, self.w, self.h)
        self.imagebase = pygame.transform.rotate(self.imagebase, dir)
        self.imagebase = pygame.transform.scale(self.imagebase, [self.w, self.h])
        self.pixelarray = PixelArray(self.imagebase)
        self.pixelarray.replace((255, 255, 255), tuple(color))
        self.imagebase = self.pixelarray.make_surface()
        self.imagebase.set_colorkey([0, 0, 0])
        # IMAGEARROW
        self.imagetop = self.spritesheet.get_sprite(self.frame2, 32, 32, self.w, self.h)
        self.imagetop = pygame.transform.scale(self.imagetop, [self.w, self.h])
        self.imagetop.set_colorkey([0, 0, 0])
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.command = None
        self.dir = dir
        self.color = color

        self.xdir = round(math.cos(math.radians(dir)))
        self.ydir = -round(math.sin(math.radians(dir)))
        self.state = "idle"
        self.aniframes = 0
        self.pastaniframes = 0
        self.flashlist = []
        self.swapflashlist = []

    def copy(self):
        return ProgramHeader(self.coordsx, self.coordsy, self.w, self.h, self.tilesx, self.tilesy, self.imageName, self.frame, self.frame2, self.dir, self.color)

    def update(self, screen, pushables, robots):
        self.aniframes += 1
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)

        # TEMPORARY
        if self.state == "idle" and pygame.key.get_pressed()[pygame.K_d]:
            self.state = "activated"
            self.totaltimes = 1

        if self.state == "idle":
            for pushable in pushables:
                if str(type(pushable)) == "<class 'player.Pushable'>":
                    if pushable.frame == 3 and pushable.coordsx == self.coordsx and pushable.coordsy == self.coordsy:
                        self.state = "activated"
                        self.totaltimes = 1
                        pushables.remove(pushable)


        if self.state == "activated":
            if self.aniframes - self.pastaniframes > 15:
                self.updaterobots(pushables, robots)
                self.totaltimes += 1
                self.pastaniframes = self.aniframes
        self.render(screen)

    def move(self, xvel, yvel):
        self.coordsx += xvel
        self.coordsy += yvel

    def render(self, screen):
        screen.blit(self.imagebase, self.rect)
        screen.blit(self.imagetop, self.rect)

    def findblock(self, x, y, xdir, ydir, pushables, depth):
        startval = 1
        while self.currenttimes <= self.totaltimes:
            self.robotcommand = None
            for pushable in pushables:
                if pushable.coordsx == x + xdir * startval and pushable.coordsy == y + ydir * startval and pushable.command != None:
                    self.robotcommand = pushable.command
                    self.pushablecoordsx = pushable.coordsx
                    self.pushablecoordsy = pushable.coordsy
                    if self.robotcommand == "function":
                        frame3 = pushable.frame3
            if self.robotcommand == None:
                if depth == 1:
                    self.state = "idle"
                break
            else:
                if self.currenttimes <= self.totaltimes:
                    self.currenttimes += 1
                    startval += 1
            if self.robotcommand == "function":
                for pushable2 in pushables:
                    if pushable2.frame == 11:
                        if pushable2.frame3 == frame3:
                            if pushable2.dir == 0:
                                pushablexdir = 1
                                pushableydir = 0
                            if pushable2.dir == 90:
                                pushablexdir = 0
                                pushableydir = -1
                            if pushable2.dir == -90:
                                pushablexdir = 0
                                pushableydir = 1
                            if pushable2.dir == 180:
                                pushablexdir = -1
                                pushableydir = 0
                            self.findblock(pushable2.coordsx, pushable2.coordsy, pushablexdir, pushableydir, pushables, depth + 1)
            #Failsafe
            if self.totaltimes >= 300:
                self.state = "idle"
    def updaterobots(self, pushables, robots):
        self.currenttimes = 1
        self.findblock(self.coordsx, self.coordsy, self.xdir, self.ydir, pushables, 1)
        if self.robotcommand != None:
            for robot in robots:
                if robot.color == self.color:
                    if self.robotcommand != "wait" and str(type(self.robotcommand)) != "<class 'list'>":
                        robot.move = self.robotcommand
                    self.flashlist.append(Flash(self.pushablecoordsx, self.pushablecoordsy, WIDTH / self.tilesx, HEIGTH / self.tilesy, self.tilesx, self.tilesy, [0, 255, 255]))
            if str(type(self.robotcommand)) == "<class 'list'>":
                for robot in robots:
                    if robot.color == self.color:
                        robot.color = [0, 0, 0]
                    elif robot.color == self.robotcommand:
                        self.swapflashlist.append(SwapFlash(robot.coordsx, robot.coordsy, robot.w, robot.h, self.tilesx, self.tilesy, self.robotcommand, "swapflare.png"))
                        robot.color = self.color
                    if robot.color == [0, 0, 0]:
                        self.swapflashlist.append(SwapFlash(robot.coordsx, robot.coordsy, robot.w, robot.h, self.tilesx, self.tilesy, self.color, "swapflare.png"))
                        robot.color = self.robotcommand


class Gate:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, passables, passablecolor):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.passables = passables
        if self.passables == "player":
            self.color = [255, 145, 122]
            self.passablesimage = pygame.image.load("Player.png")
        else:
            self.color = [131, 255, 122]
            self.passablesimage = pygame.image.load("Robot.png")
        self.passablecolor = passablecolor
        if self.passablecolor != None:
            self.pixelarray = PixelArray(self.passablesimage)
            self.pixelarray.replace((255, 255, 255), tuple(self.passablecolor))
            self.passablesimage = self.pixelarray.make_surface()
            self.pixelarray = None
        self.passablesimage = pygame.transform.scale(self.passablesimage, (self.w * 0.6, self.h * 0.6))
        self.imagerect = pygame.rect.Rect(self.w * 0.2, self.h * 0.2, self.w * 0.6, self.h * 0.6)
        self.surface = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, tuple(self.color + [50]), pygame.rect.Rect(0, 0, self.w, self.h))
        self.surface.blit(self.passablesimage, self.imagerect)


    def render(self, screen):
        screen.blit(self.surface, (self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy))

    def update(self, screen):
        self.render(screen)

class Flash:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, color):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.color = color
        self.aniframes = 0
        self.surface = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = pygame.rect.Rect(0, 0, self.w, self.h)

    def update(self, screen):
        self.surface = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA)
        if self.aniframes <= 15:
            if self.aniframes <= 6:
                self.weight = self.aniframes / 6
            if self.aniframes > 6:
                self.weight = 216 / (self.aniframes ** 3)
            self.opacity = self.weight * 255
            pygame.draw.rect(self.surface, tuple(self.color + [round(self.opacity)]), self.rect)
        self.aniframes += 1
        self.render(screen)

    def render(self, screen):
        screen.blit(self.surface, (self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy))

class Function:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, frame, frame2, frame3, command=None, dir = 0):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.imageName = image
        self.spritesheet = SpriteSheet(self.imageName)
        self.frame = frame
        self.frame2 = frame2
        self.frame3 = frame3
        self.dir = dir
        # base image
        self.baseimage = self.spritesheet.get_sprite(self.frame, 32, 32, self.w, self.h)
        self.baseimage = pygame.transform.rotate(self.baseimage, dir)
        self.baseimage = pygame.transform.scale(self.baseimage, [self.w, self.h])
        self.baseimage.set_colorkey([0, 0, 0])
        # mid image
        if self.frame2 != None:
            self.midimage = self.spritesheet.get_sprite(self.frame2, 32, 32, self.w, self.h)
            self.midimage = pygame.transform.scale(self.midimage, [self.w, self.h])
            self.midimage.set_colorkey([0, 0, 0])
        # top image
        self.topimage = self.spritesheet.get_sprite(self.frame3, 32, 32, self.w, self.h)
        self.topimage = pygame.transform.scale(self.topimage, [self.w, self.h])
        self.topimage.set_colorkey([0, 0, 0])

        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.command = command
        self.image = image

    def copy(self):
        return Function(self.coordsx, self.coordsy, self.w, self.h, self.tilesx, self.tilesy, self.imageName, self.frame, self.frame2, self.frame3, self.command, self.dir)

    def update(self, screen):
        self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
        self.render(screen)
    def move(self, xvel, yvel):
        self.coordsx += xvel
        self.coordsy += yvel

    def render(self, screen):
        screen.blit(self.baseimage, self.rect)
        if self.frame2 != None:
            screen.blit(self.midimage, self.rect)
        screen.blit(self.topimage, self.rect)

class SwapFlash:
    def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, color, image):
        self.coordsx = coordsx
        self.coordsy = coordsy
        self.w = w
        self.h = h
        self.tilesx = tilesx
        self.tilesy = tilesy
        self.color = color
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        pixelarray = PixelArray(self.image)
        pixelarray.replace((255, 255, 255), tuple(self.color))
        self.image = pixelarray.make_surface()
        pixelarray = None
        self.aniframes = 0
        self.rect = pygame.rect.Rect(coordsx * WIDTH / self.tilesx, coordsy * HEIGTH / self.tilesy, self.w, self.h)

    def render(self, screen):
        screen.blit(self.image, self.newrect)

    def update(self, screen):
        if self.aniframes <= 30:
            self.weight = math.sin(self.aniframes / 30 * math.pi)
            self.scaleby = pygame.math.lerp(self.w, 2 * self.w, self.weight)
            self.aniframes += 1
        self.image = pygame.transform.scale(self.image, (self.scaleby, self.scaleby))
        self.image.set_colorkey([0, 0, 0])
        self.newrect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.render(screen)


