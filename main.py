import pygame
from grid import Grid
from player import Player, Flag, Wall, Pushable, Door, Robot, ProgramHeader, Gate, Function, LevelBlock, LevelChange, LevelUnlock
import level
from ui import Button, text, Slider
from particle import Particle
import random

pygame.init()
WIDTH = 750
HEIGTH = 750
FIRSTLEVELNUM = 3
pygame.display.init()
screen = pygame.display.set_mode([WIDTH, HEIGTH])
clock = pygame.time.Clock()
fps = 60
dt = 0
controls = 0



def checkcrush(object, doors):
   for door in doors:
       if object.coordsx == door.coordsx and object.coordsy == door.coordsy and door.frame == 1:
           return True
   return False




def generatelevel(index):
   currentlevel = level.levels[index][0]
   tilesy = len(currentlevel)
   tilesx = len(currentlevel[0])
   grid = Grid(tilesx, tilesy, 3)
   player = None
   flag = None
   walls = []
   pushables = []
   doors = []
   robots = []
   gates = []
   levelblocks = []
   levelchanges = []
   levelunlocks = []
   for i in range(tilesy):
       for n in range(tilesx):
           currenttile = currentlevel[i][n]
           if currenttile == 1:
               player = Player(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "boy.png")
           elif currenttile == 2:
               flag = Flag(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Flag.png")
           elif currenttile == 3:
               walls.append(Wall(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "wall.png"))
           elif currenttile == 4:
               pushables.append(Pushable(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 0, "wait"))
           elif currenttile == 5:
               pushables.append(Pushable(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 3))
           elif str(type(currenttile)) == "<class 'list'>":
               if currenttile[0] == "door":
                   doors.append(Door(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Doors.png", currenttile[1], currenttile[2]))
               if currenttile[0] == "robot":
                   robots.append(Robot(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Robot.png", currenttile[1]))
               if currenttile[0] == "programblock":
                   if currenttile[1] == "up":
                       dir = 90
                       command = "up"
                   elif currenttile[1] == "down":
                       dir = -90
                       command = "down"
                   elif currenttile[1] == "left":
                       dir = 180
                       command = "left"
                   elif currenttile[1] == "right":
                       dir = 0
                       command = "right"
                   elif currenttile[1] == "swap":
                       dir = 0
                       command = currenttile[2]
                       color = currenttile[2]
                   if currenttile[1] != "swap":
                       pushables.append(Pushable(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 1, command, dir))
                   else:
                       pushables.append(Pushable(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 12, command, dir, color))
               if currenttile[0] == "programheader":
                   if currenttile[1] == "up":
                       dir = 90
                   elif currenttile[1] == "down":
                       dir = -90
                   elif currenttile[1] == "left":
                       dir = 180
                   elif currenttile[1] == "right":
                       dir = 0
                   pushables.append(ProgramHeader(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 4, 5, dir, currenttile[2]))
               if currenttile[0] == "gate":
                   gates.append(Gate(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, currenttile[1], currenttile[2]))
               if currenttile[0] == "deffunction":
                   if currenttile[2] == "up":
                       dir = 90
                   elif currenttile[2] == "down":
                       dir = -90
                   elif currenttile[2] == "left":
                       dir = 180
                   elif currenttile[2] == "right":
                       dir = 0
                   frame3 = {"a":7, "b":8, "c":9, "d":10}[currenttile[1]]
                   pushables.append(Function(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 11, 6, frame3, None, dir))
               if currenttile[0] == "gate":
                   gates.append(Gate(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, currenttile[1], currenttile[2]))
               if currenttile[0] == "function":
                   frame3 = {"a":7, "b":8, "c":9, "d":10}[currenttile[1]]
                   pushables.append(Function(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 2, None, frame3, "function"))
               if currenttile[0] == "levelblock":
                   levelblocks.append(LevelBlock(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "levelblock.png", currenttile[1]))
               if currenttile[0] == "levelchange":
                   levelchanges.append(LevelChange(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "levelchange.png", {"up":90, "down":-90, "right":0, "left":180}[currenttile[1]], currenttile[2]))
               if currenttile[0] == "levelunlock":
                   levelunlocks.append(LevelUnlock(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "levelunlock.png", currenttile[1], currenttile[2], currenttile[3]))






   return [tilesx, tilesy, grid, player, flag, walls, pushables, doors, robots, gates, levelblocks, levelchanges, levelunlocks]


isanim = False
def anim(newlevelnum, screen):
   global isanim, aniframes, iswin
   global tilesx, tilesy, grid, player, flag, walls, pushables, doors, robots, gates, levelblocks, undomoves, levelchanges, levelnumber, levelunlocks
   global levelselectundomoves
   surface = pygame.surface.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
   if isanim:
       if aniframes <= 45:
           surface = pygame.surface.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
           pygame.draw.rect(surface, [0, 0, 0, (aniframes / 45) * 255], pygame.rect.Rect(0, 0, WIDTH, HEIGTH))
       if aniframes == 46:
           pygame.draw.rect(surface, [0, 0, 0, 255], pygame.rect.Rect(0, 0, WIDTH, HEIGTH))
           levelnumber = newlevelnum
           if levelnumber < FIRSTLEVELNUM and levelselectundomoves[levelnumber] != []:
                   undoframe = levelselectundomoves[levelnumber][-1]


                   undodoorattr = undoframe["doors"]
                   doors = []
                   for doorattr in undodoorattr:
                       doors.append(Door(doorattr[0], doorattr[1], doorattr[2], doorattr[3], doorattr[4], doorattr[5], doorattr[6], doorattr[7], doorattr[8]))


                   flag = undoframe["flag"]


                   walls = undoframe["walls"]


                   grid = Grid(undoframe["gridsize"][0], undoframe["gridsize"][1], 3)


                   undopushattr = undoframe["pushables"]
                   pushables = []
                   for pushattr in undopushattr:
                       if pushattr[-1] == "pushable":
                           pushables.append(Pushable(pushattr[0], pushattr[1], pushattr[2], pushattr[3], pushattr[4], pushattr[5], pushattr[6], pushattr[7], pushattr[8], pushattr[9], pushattr[10]))
                       elif pushattr[-1] == "ProgramHeader":
                           pushables.append(ProgramHeader(pushattr[0], pushattr[1], pushattr[2], pushattr[3], pushattr[4], pushattr[5], pushattr[6], pushattr[7], pushattr[8], pushattr[9], pushattr[10]))
                       elif pushattr[-1] == "Function":
                           pushables.append(Function(pushattr[0], pushattr[1], pushattr[2], pushattr[3], pushattr[4], pushattr[5], pushattr[6], pushattr[7], pushattr[8], pushattr[9], pushattr[10], pushattr[11]))


                   undorobotattr = undoframe["robots"]
                   robots = []
                   for robotattr in undorobotattr:
                       robots.append(Robot(robotattr[0], robotattr[1], robotattr[2], robotattr[3], robotattr[4], robotattr[5], robotattr[6], robotattr[7]))


                   undoplayerattr = undoframe["player"]
                   player = Player(undoplayerattr[0], undoplayerattr[1], undoplayerattr [2], undoplayerattr[3], undoplayerattr[4], undoplayerattr[5], undoplayerattr[6])


                   gates = undoframe["gates"]


                   levelblocks = undoframe["levelblocks"]


                   levelchanges = undoframe["levelchanges"]


                   levelunlocks = undoframe["levelunlocks"]


           else:
               levelList = generatelevel(levelnumber)


               tilesx = levelList[0]
               tilesy = levelList[1]
               grid = levelList[2]
               player = levelList[3]
               flag = levelList[4]
               walls = levelList[5]
               pushables = levelList[6]
               doors = levelList[7]
               robots = levelList[8]
               gates = levelList[9]
               levelblocks = levelList[10]
               levelchanges = levelList[11]
               levelunlocks = levelList[12]
           undomoves = []
       if aniframes > 46 and aniframes <= 91:
           pygame.draw.rect(surface, [0, 0, 0, 255 - (((aniframes - 46) / 45) * 255)], pygame.rect.Rect(0, 0, WIDTH, HEIGTH))
       if aniframes > 91:
           isanim = False
           iswin = False

       else:
           screen.blit(surface, (0, 0))
           aniframes += 1


levelnumber = 0


levelList = generatelevel(levelnumber)


tilesx = levelList[0]
tilesy = levelList[1]
grid = levelList[2]
player = levelList[3]
flag = levelList[4]
walls = levelList[5]
pushables = levelList[6]
doors = levelList[7]
robots = levelList[8]
gates = levelList[9]
levelblocks = levelList[10]
levelchanges = levelList[11]
levelunlocks = levelList[12]


#GAMELOOP
isrunning = True
gamestate = "startmenu"
iswin = False
aniframes = 0
undomoves = []
levelselectundomoves = []
for i in range(FIRSTLEVELNUM):
   levelselectundomoves.append([])
gridstatetracker = 0


startbutton = Button(375, 375, 567, 67, 0.5, 0.95, "Button.png", "placeholder", "Start Game")
charactercustombutton = Button(375, 450, 567, 67, 0.5, 0.95, "Button.png", "placeholder", "Character Select")
cutscenebutton = Button(WIDTH//2,HEIGTH//2 , WIDTH, HEIGTH, 0.5, 0.95, "Button.png", "placeholder", "Next Cutscene")
levelselectbutton = Button(WIDTH // 2, HEIGTH // 2 + 75, 300, 50, 0.5, 0.95, "Button.png", "placeholder", "Level Select")
exitbutton = Button(WIDTH // 2, HEIGTH // 2 + 150, 100, 50, 0.5, 0.95, "Button.png", "placeholder", "Exit")



brightslider = Slider(382, 290, [100, 100, 100], 167, 5, 1, "Slider.png", 35, 35)
completedlevels = set()
pastgamestate = "startmenu"
brightsurface = pygame.surface.Surface([WIDTH, HEIGTH], pygame.SRCALPHA)
winimg = pygame.image.load("wintext.png")
winimg = pygame.transform.scale(winimg, [250, 250])
winrect = winimg.get_rect(center=(WIDTH // 2, HEIGTH // 2))
pastscreensurface = None
cutsceneimages = []
particles = []
for filename in ["Cut1.png", "Cut2.png", "Cut3.png"]:
   image = pygame.image.load(filename)
   image = pygame.transform.scale(image, [WIDTH, HEIGTH])
   cutsceneimages.append(image)


cutsceneframe = 0


while isrunning:
   pygame.display.set_icon(pygame.image.load("Player.png"))
   if gamestate == "startmenu":
       screen.fill([150, 150, 150])
       pygame.display.set_caption("")
       text(375, 50, 500, 50, "Game Title", [100, 100, 100], screen)
       startbutton.update(screen)
       charactercustombutton.update(screen)
       if charactercustombutton.checkcollisions():
           gamestate = "cs"
       if startbutton.checkcollisions():
           gamestate = "cutscene"
   elif gamestate == "cutscene":
       cutscenebutton.update(screen)
       if cutsceneframe <= 2:
           screen.blit(cutsceneimages[cutsceneframe], [0, 0])
           if cutscenebutton.checkcollisions():
               cutsceneframe += 1
       else:
           gamestate = "game"
   #Player(self.coordsx, self.coordsy, self.w, self.h, self.tilesx, self.tilesy, None)
   elif gamestate == "game":
           screen.fill([100, 100, 100])
           grid.render(screen)


           if levelnumber < FIRSTLEVELNUM:
               prevlevelselectnum = levelnumber
               pygame.display.set_caption("Level Select")
           else:
               pygame.display.set_caption(f"Level {levelnumber - FIRSTLEVELNUM + 1}: {level.levels[levelnumber][1]}")


           if doors != []:
               for door in doors:
                   door.update(screen, pushables, player, doors, robots)


           if flag != None:
               flag.render(screen)
           if walls != []:
               for wall in walls:
                   wall.render(screen, walls)
           if pushables != []:
               for pushable in pushables:
                   if str(type(pushable)) == "<class 'player.ProgramHeader'>":
                       pushable.update(screen, pushables, robots)
                   else:
                        pushable.update(screen)
                   if checkcrush(pushable, doors):
                       pushables.remove(pushable)
               for pushable in pushables:
                   if pushable.frame == 4:
                       if pushable.flashlist != []:
                           for flash in pushable.flashlist:
                               flash.update(screen)
                               if flash.aniframes > 15:
                                   pushable.flashlist.remove(flash)
           if robots != []:
               for robot in robots:
                   robot.update(screen, walls, pushables, doors, player, robots, gates, levelunlocks)
                   if checkcrush(robot, doors):
                       robots.remove(robot)
           for pushable in pushables:
               if str(type(pushable)) == "<class 'player.ProgramHeader'>":
                   for swapflash in pushable.swapflashlist:
                       swapflash.update(screen)
                       if swapflash.aniframes > 30:
                           pushable.swapflashlist.remove(swapflash)


           for levelblock in levelblocks:
               levelblock.render(screen, completedlevels)
               if levelblock.checkcollisions(player) and pygame.key.get_just_pressed()[pygame.K_SPACE] and not isanim:
                   isanim = True
                   aniframes = 0
                   newlevel = levelblock.number + FIRSTLEVELNUM - 1
                   levelselectpos = [levelblock.coordsx, levelblock.coordsy]


           for levelchange in levelchanges:
               levelchange.render(screen)
               if levelchange.checkcollisions(player) and not isanim:
                   isanim = True
                   aniframes = 0
                   if levelchange.progress == "forward":
                       newlevel = levelnumber + 1
                   else:
                       newlevel = levelnumber - 1
           if player != None:
               if not isanim:
                   player.update(screen, walls, pushables, doors, robots, gates, levelunlocks)
                   player.controls = controls


               else:
                   player.render(screen)
               if checkcrush(player, doors):
                   player = None


           if gates != []:
               for gate in gates:
                   gate.update(screen)


           if levelnumber < FIRSTLEVELNUM:
               curundomoves = levelselectundomoves
           else:
               curundomoves = undomoves


           if pygame.key.get_just_pressed()[pygame.K_u]:
                   if levelnumber < FIRSTLEVELNUM:
                       if len(levelselectundomoves[levelnumber]) > 0:
                           levelselectundomoves[levelnumber].remove(levelselectundomoves[levelnumber][-1])
                           if levelselectundomoves[levelnumber] == []:
                               undoframe = "undefined"
                           else:
                               undoframe = levelselectundomoves[levelnumber][-1]
                       else:
                           undoframe = "undefined"
                   else:
                       if len(undomoves) > 0:
                           curundomoves.remove(curundomoves[-1])
                           if curundomoves == []:
                               undoframe = "undefined"
                           else:
                               undoframe = undomoves[-1]
                       else:
                           undoframe = "undefined"


                   if undoframe != "undefined":
                       undodoorattr = undoframe["doors"]
                       doors = []
                       for doorattr in undodoorattr:
                           doors.append(Door(doorattr[0], doorattr[1], doorattr[2], doorattr[3], doorattr[4], doorattr[5], doorattr[6], doorattr[7], doorattr[8]))


                       flag = undoframe["flag"]


                       walls = undoframe["walls"]


                       undopushattr = undoframe["pushables"]
                       pushables = []
                       for pushattr in undopushattr:
                           if pushattr[-1] == "pushable":
                               pushables.append(Pushable(pushattr[0], pushattr[1], pushattr[2], pushattr[3], pushattr[4], pushattr[5], pushattr[6], pushattr[7], pushattr[8], pushattr[9], pushattr[10]))
                           elif pushattr[-1] == "ProgramHeader":
                               pushables.append(ProgramHeader(pushattr[0], pushattr[1], pushattr[2], pushattr[3], pushattr[4], pushattr[5], pushattr[6], pushattr[7], pushattr[8], pushattr[9], pushattr[10]))
                           elif pushattr[-1] == "Function":
                               pushables.append(Function(pushattr[0], pushattr[1], pushattr[2], pushattr[3], pushattr[4], pushattr[5], pushattr[6], pushattr[7], pushattr[8], pushattr[9], pushattr[10], pushattr[11]))


                       undorobotattr = undoframe["robots"]
                       robots = []
                       for robotattr in undorobotattr:
                           robots.append(Robot(robotattr[0], robotattr[1], robotattr[2], robotattr[3], robotattr[4], robotattr[5], robotattr[6], robotattr[7]))


                       undoplayerattr = undoframe["player"]
                       player = Player(undoplayerattr[0], undoplayerattr[1], undoplayerattr [2], undoplayerattr[3], undoplayerattr[4], undoplayerattr[5], undoplayerattr[6])
                       gates = undoframe["gates"]


                       gridstatetracker = undoframe["statenum"]
                       if curundomoves == levelselectundomoves:
                           curundomoves[levelnumber].remove(undoframe)
                       else:
                           curundomoves.remove(undoframe)


           updateframe = False
           if curundomoves == levelselectundomoves:
               if curundomoves[levelnumber] == []:
                   updateframe = True
               elif [player.gridx, player.gridy] != curundomoves[levelnumber][-1]["player"][7]:
                   updateframe = True
               else:
                   for robotnum in range(len(robots)):
                       if [robots[robotnum].gridx, robots[robotnum].gridy] != curundomoves[levelnumber][-1]["robots"][robotnum][8]:
                           updateframe = True
                           break
           else:
               if curundomoves == []:
                   updateframe = True
               elif [player.gridx, player.gridy] != curundomoves[-1]["player"][7]:
                   updateframe = True
               else:
                   for robotnum in range(len(robots)):
                       if [robots[robotnum].gridx, robots[robotnum].gridy] != curundomoves[-1]["robots"][robotnum][8]:
                           updateframe = True
                           break




           for levelunlock in levelunlocks:
               levelunlock.update(screen, completedlevels, isanim)
           for levelunlock in levelunlocks:
               if levelunlock.aniframes > 25:
                   levelunlocks.remove(levelunlock)




           for robot in robots:
               if robot.state != "idle" and robot.state != "movecooldown" or player.state != "idle" and player.state != "movecooldown":
                   updateframe = False
           for particle in particles:
               if particle.xv ** 2 + particle.yv ** 2 <= 0.01:
                   particles.remove(particle)
               else:
                   particle.update(screen)


           if updateframe:
               gridstatetracker += 1
               pastpushables = []
               for pushable in pushables:
                   if isinstance(pushable, Pushable):
                       pastpushables.append([pushable.coordsx, pushable.coordsy, pushable.w, pushable.h, pushable.tilesx, pushable.tilesy, pushable.ogimage, pushable.frame, pushable.command, pushable.dir, pushable.color, "pushable"])
                   elif isinstance(pushable, ProgramHeader):
                       pastpushables.append([pushable.coordsx, pushable.coordsy, pushable.w, pushable.h, pushable.tilesx, pushable.tilesy, pushable.ogspritesheet, pushable.frame, pushable.frame2, pushable.dir, pushable.color, "ProgramHeader"])
                   elif isinstance(pushable, Function):
                       pastpushables.append([pushable.coordsx, pushable.coordsy, pushable.w, pushable.h, pushable.tilesx, pushable.tilesy, pushable.ogimage, pushable.frame, pushable.frame2, pushable.frame3, pushable.command, pushable.dir, "Function"])
                    

               pastdoors = []
               for door in doors:
                   pastdoors.append([door.coordsx, door.coordsy, door.w, door.h, door.tilesx, door.tilesy, door.image, door.frame, door.color])


               pastrobots = []
               for robot in robots:
                   pastrobots.append([robot.coordsx, robot.coordsy, robot.w, robot.h, robot.tilesx, robot.tilesy, robot.ogimage, robot.color, [robot.gridx, robot.gridy]])


               newGridState = {
                   "doors": pastdoors,
                   "flag": flag,
                   "walls": walls,
                   "pushables": pastpushables,
                   "robots": pastrobots,
                   "player": [player.coordsx, player.coordsy, player.w, player.h, player.tilesx, player.tilesy, player.image, [player.gridx, player.gridy]],
                   "gates": gates,
                   "gridsize" : [grid.tilesx, grid.tilesy],
                   "levelblocks" : levelblocks,
                   "levelchanges": levelchanges,
                   "levelunlocks": levelunlocks,
                   "statenum": gridstatetracker,
               }
               if levelnumber < FIRSTLEVELNUM:
                   levelselectundomoves[levelnumber].append(newGridState)
               else:
                   undomoves.append(newGridState)


           if player != None and flag != None:
               if player.state == "movecooldown" or player.state == "idle":
                   if [player.coordsx, player.coordsy] == [flag.coordsx, flag.coordsy] and not isanim:
                       isanim = True
                       iswin = True
                       aniframes = -95
                       newlevel = prevlevelselectnum
                       completedlevels.add(levelnumber)
                       for i in range(12):
                           particlex = random.randint(0, WIDTH)
                           particley = random.randint(0, HEIGTH)
                           for n in range(10):
                                particles.append(Particle(particlex, particley, 5, 5, random.randint(0, 360), 0.9,
                                                 random.randint(5, 20)))
                       #pygame.mixer.Sound("Winsound.wav").play()


           if pygame.key.get_just_pressed()[pygame.K_e] and not isanim and levelnumber >= FIRSTLEVELNUM:
               isanim = True
               aniframes = 0
               completedlevels.add(levelnumber)
               newlevel = prevlevelselectnum


           if pygame.key.get_just_pressed()[pygame.K_r] and not isanim and levelnumber >= FIRSTLEVELNUM:
               isanim = True
               aniframes = 0
               newlevel = levelnumber




           #HANDLE ANIMATION BETWEEN LEVELS
           if isanim:
               if iswin:
                 if aniframes <= 46:
                    screen.blit(winimg, winrect)
                 if aniframes >= 0:
                     anim(newlevel, screen)
                 else:
                     aniframes += 1
               else:
                   anim(newlevel, screen)


   if gamestate != "settings" and pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
       pastscreensurface = screen.copy()
       darkensurface = pygame.surface.Surface([WIDTH, HEIGTH], pygame.SRCALPHA)
       pygame.draw.rect(darkensurface, [0, 0, 0, 255 * 0.5], (0, 0, WIDTH, HEIGTH))
       pastscreensurface.blit(darkensurface, [0, 0])
       pastgamestate = gamestate
       gamestate = "settings"




   elif gamestate == "settings":
       mouse = pygame.mouse.get_pos()
       screen.blit(pastscreensurface)
       text(WIDTH / 2, 50, 250, 75, "Settings", [255, 255, 255], screen)
       text(382, 257, 125, 35, "Brightness", [255, 255, 255], screen)
       brightslider.update(screen)
       controlButton = Button(WIDTH // 2, HEIGTH // 2, 200, 50, 0.5, 0.95, "Button.png", "placeholder", ["arrow", "wasd"][int(controls)])
       controlButton.update(screen)
       exitbutton.update(screen)
       levelselectbutton.update(screen)
       if controlButton.checkcollisions():
           controls = int(controls)
           controls += 1
           controls = controls % 2
       if levelselectbutton.checkcollisions() and not isanim and levelnumber >= FIRSTLEVELNUM:
           isanim = True
           aniframes = 0
           newlevel = prevlevelselectnum
           gamestate = pastgamestate
       if exitbutton.checkcollisions():
           gamestate = "startmenu"
       if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
           gamestate = pastgamestate
   elif gamestate == "cs":
       mouse = pygame.mouse.get_pos()
       screen.fill([100, 100, 100])







   #HANDLE AT ALL TIMES
   opacity = round(brightslider.findvalue(255, 0))
   pygame.draw.rect(brightsurface, [0, 0, 0, opacity], (0, 0, WIDTH, HEIGTH))
   screen.blit(brightsurface)
   dt = clock.tick(fps) / 1000
   events = pygame.event.get()
   for event in events:
       if event.type == pygame.QUIT:
           isrunning = False
   pygame.display.update()








pygame.quit()

