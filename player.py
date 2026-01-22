import pygame
from spritesheet import SpriteSheet
import math
from pygame import PixelArray
from ui import text


pygame.init()


FIRSTLEVELNUM = 3


WIDTH = 750
HEIGTH = 750
class Player:
   def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image):
       self.coordsx = coordsx
       self.coordsy = coordsy
       self.w = w
       self.h = h
       self.facing = None
       self.tilesx = tilesx
       self.tilesy = tilesy

       self.frontImage = pygame.transform.scale(pygame.image.load("FrontPOV.png"), [w, h])
       self.backImage = pygame.transform.scale(pygame.image.load("BackPOV.png"), [w, h])
       self.sideImage = pygame.transform.scale(pygame.image.load("SidePOV.png"), [w, h])
       self.frontImage.set_colorkey([0, 0, 0])
       self.backImage.set_colorkey([0, 0, 0])
       self.sideImage.set_colorkey([0, 0, 0])
       self.reverseSideImage = pygame.transform.flip(self.sideImage, True, False)
       self.images = {"movingup" : self.backImage, "movingdown" : self.frontImage, "movingleft" : self.reverseSideImage, "movingright" : self.sideImage}
       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
       self.aniframes = 0
       self.pastaniframes = 0
       self.state = "idle"
       self.gridx = coordsx
       self.gridy = coordsy
       self.currentimage = self.frontImage
       self.controls = 0
       self.keys = [[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]]




   def render(self, screen):
       if self.state in self.images.keys():
           self.currentimage = self.images[self.state]
       screen.blit(self.currentimage, self.rect)




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
   def updatepos(self, walls, pushables, doors, robots, gates, levelunlocks):
       self.keys = [[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT], [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]]
       self.aniframes += 1
       if self.state == "idle":
           if pygame.key.get_pressed()[self.keys[int(self.controls)][0]]:
               self.facing = "movingup"
               if self.checkcollisions(walls + levelunlocks, 0, -1, pushables, self.tilesx, self.tilesy, doors, robots, gates):
                   self.state = "movingup"
                   self.pastaniframes = self.aniframes
           if pygame.key.get_pressed()[self.keys[int(self.controls)][1]]:
               self.facing = "movingdown"
               if self.checkcollisions(walls + levelunlocks, 0, 1, pushables, self.tilesx, self.tilesy, doors, robots, gates):
                   self.state = "movingdown"
                   self.pastaniframes = self.aniframes
           if pygame.key.get_pressed()[self.keys[int(self.controls)][2]]:
               self.facing = "movingleft"
               if self.checkcollisions(walls + levelunlocks, -1, 0, pushables, self.tilesx, self.tilesy, doors, robots, gates):
                   self.state = "movingleft"
                   self.pastaniframes = self.aniframes
           if pygame.key.get_pressed()[self.keys[int(self.controls)][3]]:
               self.facing = "movingright"
               if self.checkcollisions(walls + levelunlocks, 1, 0, pushables, self.tilesx, self.tilesy, doors, robots, gates):
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
           self.facing = None
           self.coordsx = round(self.coordsx)
           self.coordsy = round(self.coordsy)
           self.gridx = self.coordsx
           self.gridy = self.coordsy
           if self.aniframes - self.pastaniframes >= 2:
               self.state = "idle"
       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)


   def update(self, screen, walls, pushables, doors, robots, gates, levelunlocks):
       self.updatepos(walls, pushables, doors, robots, gates, levelunlocks)
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
       self.tilesy = tilesy
       self.ogimage = image
       self.spritesheet = SpriteSheet(self.ogimage)
       self.collisions = [True, True, True, True]


       #BASE IMAGE
       self.image = self.spritesheet.get_sprite(0, 32, 32, self.w, self.h)
       self.image.set_colorkey([0,0,0])
       #EDGE IMAGE
       self.edgeimage = self.spritesheet.get_sprite(1, 32, 32, self.w, self.h)
       self.edgeimage.set_colorkey([0,0,0])
       #CORNER IMAGE
       self.cornerimage = self.spritesheet.get_sprite(2, 32, 32, self.w, self.h)
       self.cornerimage.set_colorkey([0,0,0])
       #FLIP CORNER IMAGE
       self.flipcornerimage = self.spritesheet.get_sprite(3, 32, 32, self.w, self.h)
       self.flipcornerimage.set_colorkey([0,0,0])


       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / tilesx, self.coordsy * HEIGTH / tilesy, w, h)


   def render(self, screen, walls):
       self.walls = walls
       self.collisions = [True, True, True, True]
       self.edges = []
       self.corners = []
       for wall in self.walls:
           if [self.coordsx + 1, self.coordsy] == [wall.coordsx, wall.coordsy] or self.coordsx + 1 > self.tilesx - 1:
               self.collisions[0] = False
           if [self.coordsx, self.coordsy - 1] == [wall.coordsx, wall.coordsy] or self.coordsy - 1 < 0:
               self.collisions[1] = False
           if [self.coordsx - 1, self.coordsy] == [wall.coordsx, wall.coordsy] or self.coordsx - 1 < 0:
               self.collisions[2] = False
           if [self.coordsx, self.coordsy + 1] == [wall.coordsx, wall.coordsy] or self.coordsy + 1 > self.tilesy - 1:
               self.collisions[3] = False


       if self.collisions[0]:
           self.edges.append(pygame.transform.scale(pygame.transform.rotate(self.edgeimage, 180), [self.w, self.h]))
       if self.collisions[1]:
           self.edges.append(pygame.transform.scale(pygame.transform.rotate(self.edgeimage, -90), [self.w, self.h]))
       if self.collisions[2]:
           self.edges.append(self.edgeimage)
       if self.collisions[3]:
           self.edges.append(pygame.transform.scale(pygame.transform.rotate(self.edgeimage, 90), [self.w, self.h]))


       if self.collisions[0] and self.collisions[1]:
           self.corners.append(pygame.transform.scale(pygame.transform.rotate(self.cornerimage, -90), [self.w, self.h]))
       if self.collisions[1] and self.collisions[2]:
           self.corners.append(self.cornerimage)
       if self.collisions[2] and self.collisions[3]:
           self.corners.append(pygame.transform.scale(pygame.transform.rotate(self.cornerimage, 90), [self.w, self.h]))
       if self.collisions[3] and self.collisions[0]:
           self.corners.append(pygame.transform.scale(pygame.transform.rotate(self.cornerimage, 180), [self.w, self.h]))


       self.adg = [None, None, None, None]
       for wall in self.walls:
           if [self.coordsx + 1, self.coordsy] == [wall.coordsx, wall.coordsy]:
               self.adg[0] = wall
           if [self.coordsx , self.coordsy - 1] == [wall.coordsx, wall.coordsy]:
               self.adg[1] = wall
           if [self.coordsx - 1, self.coordsy] == [wall.coordsx, wall.coordsy]:
               self.adg[2] = wall
           if [self.coordsx, self.coordsy + 1] == [wall.coordsx, wall.coordsy]:
               self.adg[3] = wall


       if self.adg[0] != None and self.adg[1] != None:
           if self.adg[0].collisions[1] and self.adg[1].collisions[0]:
               self.corners.append(pygame.transform.scale(pygame.transform.rotate(self.flipcornerimage, -90), [self.w, self.h]))
       if self.adg[1] != None and self.adg[2] != None:
           if self.adg[1].collisions[2] and self.adg[2].collisions[1]:
               self.corners.append(pygame.transform.scale(self.flipcornerimage, [self.w, self.h]))
       if self.adg[2] != None and self.adg[3] != None:
           if self.adg[2].collisions[3] and self.adg[3].collisions[2]:
               self.corners.append(pygame.transform.scale(pygame.transform.rotate(self.flipcornerimage, 90), [self.w, self.h]))
       if self.adg[3] != None and self.adg[0] != None:
           if self.adg[3].collisions[0] and self.adg[0].collisions[3]:
               self.corners.append(pygame.transform.scale(pygame.transform.rotate(self.flipcornerimage, 180), [self.w, self.h]))


       for i in self.edges + self.corners:
           i.set_colorkey([0, 0, 0])


       screen.blit(self.image, self.rect)


       for edge in self.edges:
           screen.blit(edge, self.rect)


       for corner in self.corners:
           screen.blit(corner, self.rect)




class Pushable:
   def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, frame, command=None, dir = 0, color=[0,1,6]):
       self.coordsx = coordsx
       self.coordsy = coordsy
       self.w = w
       self.h = h
       self.tilesx = tilesx
       self.tilesy = tilesy
       self.ogimage = image
       self.spritesheet = SpriteSheet(self.ogimage)
       self.frame = frame
       self.image = self.spritesheet.get_sprite(self.frame, 32, 32, self.w, self.h)
       self.pixelarray = PixelArray(self.image)
       self.pixelarray.replace((255, 255, 255), tuple(color))
       self.color = color
       self.image = self.pixelarray.make_surface()
       self.pixelarray = None
       self.dir = dir
       self.image = pygame.transform.rotate(self.image, self.dir)
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
           if players != None:
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
           self.ogimage = image
           self.image = pygame.image.load(self.ogimage)
           self.image = pygame.transform.scale(self.image, [w, h])
           self.image.set_colorkey([0, 0, 0])
           self.state = "idle"
           self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
           self.aniframes = 0
           self.pastaniframes = 0
           self.move = None
           self.color = color
           self.gridx = self.coordsx
           self.gridy = self.coordsy


       def render(self, screen):
           self.pixelarray = PixelArray(self.image.copy())
           self.pixelarray.replace((255, 255, 255), tuple(self.color))
           self.newimage = self.pixelarray.make_surface()
           self.pixelarray = None
           screen.blit(self.newimage, self.rect)


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


       def updatepos(self, walls, pushables, doors, player, robots, gates, levelunlocks):
           self.aniframes += 1
           if self.state == "idle":
               if self.move == "up":
                   if self.checkcollisions(walls + levelunlocks, 0, -1, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                       self.state = "movingup"
                       self.pastaniframes = self.aniframes
               if self.move == "down":
                   if self.checkcollisions(walls + levelunlocks, 0, 1, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                       self.state = "movingdown"
                       self.pastaniframes = self.aniframes
               if self.move == "left":
                   if self.checkcollisions(walls + levelunlocks, -1, 0, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
                       self.state = "movingleft"
                       self.pastaniframes = self.aniframes
               if self.move == "right":
                   if self.checkcollisions(walls + levelunlocks, 1, 0, pushables, self.tilesx, self.tilesy, doors, player, robots, gates):
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


       def update(self, screen, walls, pushables, doors, player, robots, gates, levelunlocks):
           self.updatepos(walls, pushables, doors, player, robots, gates, levelunlocks)
           self.render(screen)


class ProgramHeader:
   def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, spritesheet, frame, frame2, dir, color):
       self.coordsx = coordsx
       self.coordsy = coordsy
       self.w = w
       self.h = h
       self.tilesx = tilesx
       self.tilesy = tilesy
       self.ogspritesheet = spritesheet
       self.spritesheet = SpriteSheet(self.ogspritesheet)
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


   def update(self, screen, pushables, robots):
       self.aniframes += 1
       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)


       # TEMPORARY
       if self.state == "idle" and pygame.key.get_pressed()[pygame.K_f]:
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
       self.ogimage = image
       self.spritesheet = SpriteSheet(self.ogimage)
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




class LevelBlock:
   def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, number):
       self.coordsx = coordsx
       self.coordsy = coordsy
       self.w = w
       self.h = h
       self.tilesx = tilesx
       self.tilesy = tilesy
       self.spritesheet = SpriteSheet(image)
       self.images = [self.spritesheet.get_sprite(0, 32, 32, self.w, self.h), self.spritesheet.get_sprite(1, 32, 32, self.w, self.h)]
       self.number = number
       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)


   def render(self, screen, completedlevels):
       if self.number + FIRSTLEVELNUM - 1 in completedlevels:
           screen.blit(self.images[1], self.rect)
       else:
           screen.blit(self.images[0], self.rect)
       text(self.rect.centerx, self.rect.centery, self.w * 0.85, self.h * 0.75, self.number, [0, 0, 0], screen)


   def checkcollisions(self, player):
       return [player.coordsx, player.coordsy] == [self.coordsx, self.coordsy]


class LevelChange:
   def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, dir, progress):
       self.coordsx = coordsx
       self.coordsy = coordsy
       self.w = w
       self.h = h
       self.tilesx = tilesx
       self.tilesy = tilesy
       self.dir = dir
       self.facingstate = {0:"movingright", 90:"movingup", 180:"movingleft", -90:"movingdown"}[self.dir]
       self.progress = progress
       if self.progress == "forward":
           self.color = [18, 135, 0]
       else:
           self.color = [135, 0, 0]
       self.image = pygame.image.load(image)
       self.image = pygame.transform.scale(self.image, [self.w, self.h])
       self.image = pygame.transform.rotate(self.image, self.dir)
       self.image.set_colorkey([0, 0, 0])
       self.pixelarray = PixelArray(self.image)
       self.pixelarray.replace((255, 255, 255), tuple(self.color))
       self.image = self.pixelarray.make_surface()
       self.pixelarray = None
       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)


   def render(self, screen):
       screen.blit(self.image, self.rect)


   def checkcollisions(self, player):
       return [player.coordsx, player.coordsy] == [self.coordsx, self.coordsy] and player.facing == self.facingstate


class LevelUnlock:
   def __init__(self, coordsx, coordsy, w, h, tilesx, tilesy, image, minlevel, maxlevel, totallevels):
       self.coordsx = coordsx
       self.coordsy = coordsy
       self.w = w
       self.h = h
       self.tilesx = tilesx
       self.tilesy = tilesy
       self.image = pygame.image.load(image)
       self.image = pygame.transform.scale(self.image, [self.w, self.h])
       self.image.set_colorkey([0, 0, 0])
       self.minlevel = minlevel
       self.maxlevel = maxlevel
       self.totallevels = totallevels
       self.currentlevels = 0
       self.rect = pygame.rect.Rect(self.coordsx * WIDTH / self.tilesx, self.coordsy * HEIGTH / self.tilesy, self.w, self.h)
       self.surface = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA)
       self.aniframes = 0
       #TEXT DIMENSIONS
       self.textcenterx = self.w / 2
       self.textcentery = self.h * 7 / 32
       self.textw = self.w
       self.texth = self.h * 16 / 32


   def render(self, screen):
       if self.aniframes <= 25:
           self.surface.blit(self.image, (0, 0))
           text(self.textcenterx, self.textcentery, self.textw * 0.9, self.texth * 0.9, str(self.currentlevels) + "/" + str(self.totallevels),[0, 255, 255], self.surface)
           self.surface.set_alpha(pygame.math.lerp(255, 0, self.aniframes / 25))
           screen.blit(self.surface, self.rect)


   def updatenumber(self, completedlevels, isanim):
       self.currentlevels = 0
       for level in completedlevels:
           if self.minlevel <= level - FIRSTLEVELNUM + 1 <= self.maxlevel:
               self.currentlevels += 1
       if self.currentlevels >= self.totallevels and not isanim:
           self.aniframes += 1




   def update(self, screen, completedlevels, isanim = True):
       self.updatenumber(completedlevels, isanim)
       self.render(screen)



