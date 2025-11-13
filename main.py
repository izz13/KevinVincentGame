import pygame
from grid import Grid
from player import Player, Flag, Wall, Pushable, Door, Robot, ProgramHeader, Gate, Function
import level
from ui import Button, text, Slider


pygame.init()

WIDTH = 750
HEIGTH = 750
pygame.display.init()
screen = pygame.display.set_mode([WIDTH, HEIGTH])
clock = pygame.time.Clock()
fps = 60
dt = 0

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
    for i in range(tilesy):
        for n in range(tilesx):
            currenttile = currentlevel[i][n]
            if currenttile == 1:
                player = Player(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Player.png")
            elif currenttile == 2:
                flag = Flag(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Flag.png")
            elif currenttile == 3:
                walls.append(Wall(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Walls.png"))
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

    return [tilesx, tilesy, grid, player, flag, walls, pushables, doors, robots, gates]
'''
def startsound(soundfilename, duration):
    soundplay[soundfilename][0] = duration
'''

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



#GAMELOOP
isrunning = True
gamestate = "startmenu"
aniframes = 0
isanim = False
'''
soundplay = {"Winsound.wav":[0,0],
             "crushsound":[0,0],
             }
'''

undomoves = []
gridstatetracker = 0

startbutton = Button(375, 375, 567, 67, 0.5, 0.95, "Button.png", "placeholder", "Start Game")
brightslider = Slider(382, 290, [100, 100, 100], 167, 5, 1, "Slider.png", 35, 35)
pastgamestate = "startmenu"
brightsurface = pygame.surface.Surface([WIDTH, HEIGTH], pygame.SRCALPHA)


while isrunning:
    pygame.display.set_icon(pygame.image.load("Player.png"))
    if gamestate == "startmenu":
        screen.fill([150, 150, 150])
        pygame.display.set_caption("")
        text(375, 50, 500, 50, "Game Title", [100, 100, 100], screen)
        startbutton.update(screen)
        if startbutton.checkcollisions():
            gamestate = "game"

    #Player(self.coordsx, self.coordsy, self.w, self.h, self.tilesx, self.tilesy, None)
    elif gamestate == "game":
            pygame.display.set_caption(f"Level {levelnumber}: {level.levels[levelnumber][1]}")
            screen.fill([100, 100, 100])
            grid.render(screen)

            if doors != []:
                for door in doors:
                    door.update(screen, pushables, player, doors, robots)

            if flag != None:
                flag.render(screen)
            if walls != []:
                for wall in walls:
                    wall.render(screen)
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
                    robot.update(screen, walls, pushables, doors, player, robots, gates)
                    if checkcrush(robot, doors):
                        robots.remove(robot)
            for pushable in pushables:
                if str(type(pushable)) == "<class 'player.ProgramHeader'>":
                    for swapflash in pushable.swapflashlist:
                        swapflash.update(screen)
                        if swapflash.aniframes > 30:
                            pushable.swapflashlist.remove(swapflash)

            if player != None:
                player.update(screen, walls, pushables, doors, robots, gates)
                if checkcrush(player, doors):
                    player = None

            if gates != []:
                for gate in gates:
                    gate.update(screen)

            #print(len(undomoves))
            if pygame.key.get_just_pressed()[pygame.K_u]:
                if undomoves != []:
                    if len(undomoves) > 1:
                        undomoves.remove(undomoves[-1])
                        undoframe = undomoves[-1]
                    else:
                        undoframe = undomoves[0]

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
                    undomoves.remove(undoframe)

            updateframe = False
            if undomoves == []:
                updateframe = True
            elif [player.gridx, player.gridy] != undomoves[-1]["player"][7]:
                updateframe = True
            else:
                for robotnum in range(len(robots)):
                    if [robots[robotnum].gridx, robots[robotnum].gridy] != undomoves[-1]["robots"][robotnum][8]:
                        updateframe = True
                        break
            for robot in robots:
                if isinstance(robot.coordsx, float) or isinstance(robot.coordsy, float) or isinstance(player.coordsx, float) or isinstance(player.coordsy, float):
                    updateframe = False

            if updateframe:
                gridstatetracker += 1
                # (self, coordsx, coordsy, w, h, tilesx, tilesy, image, frame, frame2, frame3, command=None, dir = 0)

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
                    "player": [player.coordsx, player.coordsy, player.w, player.h, player.tilesx, player.tilesy, None, [player.gridx, player.gridy]],
                    "gates": gates,
                    "statenum": gridstatetracker
                }
                undomoves.append(newGridState)

            if player != None and flag != None:
                if player.state == "movecooldown" or player.state == "idle":
                    if [player.coordsx, player.coordsy] == [flag.coordsx, flag.coordsy] and not isanim:
                        isanim = True
                        pygame.mixer.Sound("Winsound.wav").play()

            if pygame.key.get_just_pressed()[pygame.K_e] and not isanim:
                isanim = True
                pygame.mixer.Sound("Winsound.wav").play()

            if pygame.key.get_just_pressed()[pygame.K_r]:
                tilesx = generatelevel(levelnumber)[0]
                tilesy = generatelevel(levelnumber)[1]
                grid = generatelevel(levelnumber)[2]
                player = generatelevel(levelnumber)[3]
                flag = generatelevel(levelnumber)[4]
                walls = generatelevel(levelnumber)[5]
                pushables = generatelevel(levelnumber)[6]
                doors = generatelevel(levelnumber)[7]
                robots = generatelevel(levelnumber)[8]
                gates = generatelevel(levelnumber)[9]
                undomoves = []

            #HANDLE ANIMATION BETWEEN LEVELS
            if isanim:
                if aniframes <= 45:
                    surface = pygame.surface.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
                    pygame.draw.rect(surface, [0, 0, 0, (aniframes / 45) * 255], pygame.rect.Rect(0, 0, WIDTH, HEIGTH))
                if aniframes == 46:
                    levelnumber += 1
                    tilesx = generatelevel(levelnumber)[0]
                    tilesy = generatelevel(levelnumber)[1]
                    grid = generatelevel(levelnumber)[2]
                    player = generatelevel(levelnumber)[3]
                    flag = generatelevel(levelnumber)[4]
                    walls = generatelevel(levelnumber)[5]
                    pushables = generatelevel(levelnumber)[6]
                    doors = generatelevel(levelnumber)[7]
                    robots = generatelevel(levelnumber)[8]
                    gates = generatelevel(levelnumber)[9]
                    undomoves = []
                if aniframes > 46 and aniframes <= 91:
                    surface = pygame.surface.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
                    pygame.draw.rect(surface, [0, 0, 0, 255 - (((aniframes - 46) / 45) * 255)], pygame.rect.Rect(0, 0, WIDTH, HEIGTH))
                if aniframes > 91:
                    isanim = False
                else:
                    screen.blit(surface, (0,0))

            if not isanim:
                aniframes = 0
            else:
                aniframes += 1


    if gamestate != "settings" and pygame.key.get_just_pressed()[pygame.K_s]:
        pastgamestate = gamestate
        gamestate = "settings"

    elif gamestate == "settings":
        mouse = pygame.mouse.get_pos()
        #print(mouse)
        screen.fill([50, 50, 50])
        text(WIDTH / 2, 50, 250, 75, "Settings", [255, 255, 255], screen)
        text(382, 257, 125, 35, "Brightness", [255, 255, 255], screen)
        brightslider.update(screen)
        if pygame.key.get_just_pressed()[pygame.K_s]:
            gamestate = pastgamestate




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
