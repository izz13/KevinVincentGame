import pygame
from grid import Grid
from player import Player, Flag, Wall, Pushable, Door, Robot, ProgramHeader, Gate, Function
import level
from ui import Button, text
import copy
from pygame.math import Vector2

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

soundplay = {"winsound":False,
             "crushsound":False,
             }
winsound = pygame.mixer.Sound("Win.wav")

undomoves = []
gridstatetracker = 0
if player != None:
    oldplayerpos = [player.gridx, player.gridy]
    newplayerpos = oldplayerpos
else:
    oldplayerpos = None
    newplayerpos = oldplayerpos
oldrobotpos = []
for robot in robots:
    oldrobotpos.append([robot.gridx, robot.gridy])
newrobotpos = oldrobotpos

while isrunning:
    pygame.display.set_icon(pygame.image.load("Player.png"))
    screen.fill([150, 150, 150])
    if gamestate == "startmenu":
        pygame.display.set_caption("")
        text(375, 50, 500, 50, "Game Title", [100, 100, 100], screen)
        startbutton = Button(375, 375, 567, 67, 0.5, 0.95, "Button.png", "placeholder", "Start Game")
        startbutton.update(screen)
        if startbutton.checkcollisions():
            gamestate = "game"

    elif gamestate == "game":
            gridstate = {
                "doors":doors,
                "flag":flag,
                "walls":walls,
                "pushables":pushables,
                "robots":robots,
                "player":player,
                "gates":gates,
                "statenum":gridstatetracker
            }

            # if newplayerpos != oldplayerpos or newrobotpos != oldrobotpos:
            #     gridstatetracker += 1
            #     #undomoves.append(copy.deepcopy(gridstate))
            #     newGridState = {
            #         "doors":[],
            #         "flag":[],
            #         "walls":[],
            #         "pushables":[],
            #         "robots":[],
            #         "player":[],
            #         "gates":[],
            #         "statenum":gridstatetracker
            #     }
            #     for key in gridstate:
            #         # print(f"{key}, {gridstate[key]}")
            #         try:
            #             newGridState[key] = copy.deepcopy(gridstate[key])
            #         except:
            #             print(f"{key} could not be deep copied")
            #             if key == "doors":
            #                 for door in gridstate["doors"]:
            #                     newGridState["doors"].append(Door(door.coordsx,door.coordsy,door.w,door.h,door.tilesx,door.tilesy,door.image,door.frame,door.color))
            #             if key == "pushables":
            #                 for pu in gridstate["pushables"]:
            #                     newGridState["pushables"].append(pu.copy())
            #             if key == "player":
            #                 newGridState["player"] = player.copy()
            #     # for key in newGridState:
            #         # print(f"{key}, {newGridState[key]}")
            #     undomoves.append(newGridState)
            #     oldplayerpos = newplayerpos
            #     oldrobotpos = newrobotpos


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
                input = Vector2(0)
                keys_clicked = pygame.key.get_just_pressed()
                if keys_clicked[pygame.K_UP]:
                    input.y = -1
                if keys_clicked[pygame.K_DOWN]:
                    input.y = 1
                if keys_clicked[pygame.K_RIGHT]:
                    input.x = 1
                if keys_clicked[pygame.K_LEFT]:
                    input.x = -1
                if input != Vector2(0):
                    gridstatetracker += 1
                    #undomoves.append(copy.deepcopy(gridstate))
                    newGridState = {
                        "doors":[],
                        "flag":[],
                        "walls":[],
                        "pushables":[],
                        "robots":[],
                        "player":[],
                        "gates":[],
                        "statenum":gridstatetracker
                    }
                    for key in gridstate:
                        # print(f"{key}, {gridstate[key]}")
                        try:
                            newGridState[key] = copy.deepcopy(gridstate[key])
                        except:
                            print(f"{key} could not be deep copied")
                            if key == "doors":
                                for door in gridstate["doors"]:
                                    newGridState["doors"].append(Door(door.coordsx,door.coordsy,door.w,door.h,door.tilesx,door.tilesy,door.image,door.frame,door.color))
                            if key == "pushables":
                                for pu in gridstate["pushables"]:
                                    newGridState["pushables"].append(pu.copy())
                            if key == "player":
                                newGridState["player"] = player.copy()
                    # for key in newGridState:
                        # print(f"{key}, {newGridState[key]}")
                    undomoves.append(newGridState)
                    oldplayerpos = newplayerpos
                    oldrobotpos = newrobotpos
                player.update(screen, walls, pushables, doors, robots, gates,input)
                if checkcrush(player, doors):
                    player = None
                newplayerpos = [player.gridx, player.gridy]
            else:
                newplayerpos = None

            if gates != []:
                for gate in gates:
                    gate.update(screen)


            #print(len(undomoves))
            if pygame.key.get_just_pressed()[pygame.K_u]:
                if undomoves != []:
                    if len(undomoves) > 1:
                        undoframe = undomoves[-1]
                    else:
                        undoframe = undomoves[0]
                    doors = undoframe["doors"]
                    flag = undoframe["flag"]
                    walls = undoframe["walls"]
                    pushables = undoframe["pushables"]
                    robots = undoframe["robots"]
                    if player == undoframe["player"]:
                        print("undo player same as current player")
                    else:
                        player = undoframe["player"]
                    gates = undoframe["gates"]
                    gridstatetracker = undoframe["statenum"]
                    undomoves.remove(undoframe)

            if player != None and flag != None:
                if player.state == "movecooldown" or player.state == "idle":
                    if [player.coordsx, player.coordsy] == [flag.coordsx, flag.coordsy] and not isanim:
                        isanim = True

            if pygame.key.get_just_pressed()[pygame.K_s] and not isanim:
                isanim = True

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
                soundplay["winsound"] = False
            else:
                aniframes += 1
                soundplay["winsound"] = True

            #HANDLE SOUND
            if soundplay["winsound"]:
                winsound.play()


    dt = clock.tick(fps) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isrunning = False
    pygame.display.update()



pygame.quit()
