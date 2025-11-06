import pygame
from grid import Grid
from player import Player, Flag, Wall, Pushable, Door, Robot, ProgramHeader, Gate, Function
from ui import Button, TypeField, text
import time
import pyperclip



pygame.init()

WIDTH = 750
HEIGTH = 750
pygame.display.init()
screen = pygame.display.set_mode([WIDTH + 600, HEIGTH])
clock = pygame.time.Clock()
fps = 60
dt = 0

#testlevelw = 5
#testlevelh = 5
testlevel = [[0] * 5] * 5


def checkcrush(object, doors):
    for door in doors:
        if object.coordsx == door.coordsx and object.coordsy == door.coordsy and door.frame == 1:
            return True
    return False

def generatelevel():
    currentlevel = testlevel
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
                    frame3 = {"a": 7, "b": 8, "c": 9, "d": 10}[currenttile[1]]
                    pushables.append(Function(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 11, 6, frame3, None, dir))
                if currenttile[0] == "gate":
                    gates.append(Gate(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, currenttile[1], currenttile[2]))
                if currenttile[0] == "function":
                    frame3 = {"a": 7, "b": 8, "c": 9, "d": 10}[currenttile[1]]
                    pushables.append(Function(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 2, None, frame3, "function"))

    return [tilesx, tilesy, grid, player, flag, walls, pushables, doors, robots, gates]




tilesx = generatelevel()[0]
tilesy = generatelevel()[1]
grid = generatelevel()[2]
player = generatelevel()[3]
flag = generatelevel()[4]
walls = generatelevel()[5]
pushables = generatelevel()[6]
doors = generatelevel()[7]
robots = generatelevel()[8]
gates = generatelevel()[9]




#GAMELOOP
isrunning = True

undomoves = []
gridstatetracker = 0
if player != None:
    oldplayerpos = [player.gridx, player.gridy]
else:
    oldplayerpos = None
newplayerpos = oldplayerpos
oldrobotpos = []
for robot in robots:
    oldrobotpos.append([robot.gridx, robot.gridy])
newrobotpos = oldrobotpos

widthincreasebutton = Button(850, 75, 100, 100, 0.7, 0.7, "Button.png", None, "+w")
widthdecreasebutton = Button(850 + 125, 75, 100, 100, 0.7, 0.7, "Button.png", None, "-w")
heightincreasebutton = Button(850, 75 + 125, 100, 100, 0.7, 0.7, "Button.png", None, "+h")
heightdecreasebutton = Button(850 + 125, 75 + 125, 100, 100, 0.7, 0.7, "Button.png", None, "-h")
playerbutton = Button(850, 75 + 125 * 2, 100, 100, 0.7, 0.7, "Button.png", None, "player")
emptybutton = Button(850 + 125, 75 + 125 * 2, 100, 100, 0.7, 0.7, "Button.png", None, "empty")
flagbutton = Button(850, 75 + 125 * 3, 100, 100, 0.7, 0.7, "Button.png", None, "flag")
wallbutton = Button(850 + 125, 75 + 125 * 3, 100, 100, 0.7, 0.7, "Button.png", None, "wall")
pushablebutton = Button(850, 75 + 125 * 4, 100, 100, 0.7, 0.7, "Button.png", None, "pushable")
pblockbutton = Button(850 + 125, 75 + 125 * 4, 100, 100, 0.7, 0.7, "Button.png", None, "pblock")
robotbutton = Button(850, 75 + 125 * 5, 100, 100, 0.7, 0.7, "Button.png", None, "robot")
pheadbutton = Button(850 + 125, 75 + 125 * 5, 100, 100, 0.7, 0.7, "Button.png", None, "phead")
batterybutton = Button(850 + 125 * 2, 75, 100, 100, 0.7, 0.7, "Button.png", None, "battery")
doorbutton = Button(850 + 125 * 2, 75 + 125, 100, 100, 0.7, 0.7, "Button.png", None, "door")
gatebutton = Button(850 + 125 * 2, 75 + 125 * 2, 100, 100, 0.7, 0.7, "Button.png", None, "gate")
defbutton = Button(850 + 125 * 2, 75 + 125 * 3, 100, 100, 0.7, 0.7, "Button.png", None, "def")
funcbutton = Button(850 + 125 * 2, 75 + 125 * 4, 100, 100, 0.7, 0.7, "Button.png", None, "func")
portbutton = Button(850 + 125 * 2, 75 + 125 * 5, 100, 100, 0.7, 0.7, "Button.png", None, "port")

rtypefield = TypeField(850 + 125 * 3 + 40, 75, 150, 75, 0.9, 0.9, "textfield.png", "R:", 3, [255, 0, 0])
gtypefield = TypeField(850 + 125 * 3 + 40 , 75 + 125, 150, 75, 0.9, 0.9, "textfield.png", "G:", 3, [0, 255, 0])
btypefield = TypeField(850 + 125 * 3 + 40, 75 + 125 * 2, 150, 75, 0.9, 0.9, "textfield.png", "B:", 3, [0, 0, 255])

testmode = False
tpressed = False

mousemode = "empty"
index = 0
index2 = 0


while isrunning:
    if pygame.key.get_pressed()[pygame.K_t] and not tpressed:
        tpressed = True
    if tpressed and not pygame.key.get_pressed()[pygame.K_t]:
        tpressed = False
        testmode = not testmode




    screen.fill([150, 150, 150])

    grid.render(screen)

    if not testmode:
        tilesx = generatelevel()[0]
        tilesy = generatelevel()[1]
        grid = generatelevel()[2]
        player = generatelevel()[3]
        flag = generatelevel()[4]
        walls = generatelevel()[5]
        pushables = generatelevel()[6]
        doors = generatelevel()[7]
        robots = generatelevel()[8]
        gates = generatelevel()[9]

        widthincreasebutton.update(screen)
        widthdecreasebutton.update(screen)
        heightincreasebutton.update(screen)
        heightdecreasebutton.update(screen)
        playerbutton.update(screen)
        emptybutton.update(screen)
        flagbutton.update(screen)
        wallbutton.update(screen)
        pushablebutton.update(screen)
        pblockbutton.update(screen)
        robotbutton.update(screen)
        pheadbutton.update(screen)
        batterybutton.update(screen)
        doorbutton.update(screen)
        gatebutton.update(screen)
        defbutton.update(screen)
        funcbutton.update(screen)
        portbutton.update(screen)


        text(1300, 725, 80, 20, str(tilesx) + " by " + str(tilesy), [255, 255, 255], screen)

        if widthincreasebutton.checkcollisions():
            newtestlevel = []
            for row in testlevel:
                newtestlevel.append(row + [0])
            testlevel = newtestlevel
            time.sleep(0.1)
        if heightincreasebutton.checkcollisions():
            testlevel.append([0] * len(testlevel[0]))
            time.sleep(0.1)
        if widthdecreasebutton.checkcollisions() and len(testlevel[0]) > 1:
            newtestlevel = []
            for row in testlevel:
                row.remove(row[-1])
                newtestlevel.append(row)
            testlevel = newtestlevel
            time.sleep(0.1)
        if heightdecreasebutton.checkcollisions() and len(testlevel) > 1:
            testlevel.remove(testlevel[-1])
            time.sleep(0.1)
        if playerbutton.checkcollisions():
            mousemode = "player"
        if emptybutton.checkcollisions():
            mousemode = "empty"
        if flagbutton.checkcollisions():
            mousemode = "flag"
        if wallbutton.checkcollisions():
            mousemode = "wall"
        if pushablebutton.checkcollisions():
            mousemode = "pushable"
        if pblockbutton.checkcollisions():
            mousemode = "pblock"
        if robotbutton.checkcollisions():
            mousemode = "robot"
        if pheadbutton.checkcollisions():
            mousemode = "phead"
        if batterybutton.checkcollisions():
            mousemode = "battery"
        if doorbutton.checkcollisions():
            mousemode = "door"
        if gatebutton.checkcollisions():
            mousemode = "gate"
        if defbutton.checkcollisions():
            mousemode = "def"
        if funcbutton.checkcollisions():
            mousemode = "func"
        if portbutton.checkcollisions():
            mousemode = "port"

        if mousemode == "pblock":
            index = index % 5
            dirbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 3, 150, 75, 0.7, 0.7, "Button.png", None, ["up", "down", "left", "right", "swap"][index])
            if dirbutton.checkcollisions():
                index = index + 1
                time.sleep(0.2)
            dirbutton.update(screen)
            if index == 4:
                rtypefield.update(screen)
                gtypefield.update(screen)
                btypefield.update(screen)

        if mousemode == "robot":
            rtypefield.update(screen)
            gtypefield.update(screen)
            btypefield.update(screen)
        if mousemode == "phead":
            index = index % 4
            dirbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 3, 150, 75, 0.7, 0.7, "Button.png", None, ["up", "down", "left", "right"][index])
            if dirbutton.checkcollisions():
                index = index + 1
                time.sleep(0.2)
            dirbutton.update(screen)
            rtypefield.update(screen)
            gtypefield.update(screen)
            btypefield.update(screen)
        if mousemode == "door":
            index = index % 2
            dirbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 3, 150, 75, 0.7, 0.7, "Button.png", None, ["sensor", "door"][index])
            if dirbutton.checkcollisions():
                index = index + 1
                time.sleep(0.2)
            dirbutton.update(screen)
            rtypefield.update(screen)
            gtypefield.update(screen)
            btypefield.update(screen)
        if mousemode == "gate":
            index = index % 2
            dirbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 3, 150, 75, 0.7, 0.7, "Button.png", None, ["player", "robot"][index])
            if dirbutton.checkcollisions():
                index = index + 1
                time.sleep(0.2)
            dirbutton.update(screen)
            if index == 1:
                rtypefield.update(screen)
                gtypefield.update(screen)
                btypefield.update(screen)
        if mousemode == "def":
            index = index % 4
            index2 = index2 % 4
            dirbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 3, 150, 75, 0.7, 0.7, "Button.png", None, ["up", "down", "left", "right"][index])
            letterbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 4, 150, 75, 0.7, 0.7, "Button.png", None, ["a", "b", "c", "d"][index2])
            if dirbutton.checkcollisions():
                index = index + 1
                time.sleep(0.2)
            if letterbutton.checkcollisions():
                index2 = index2 + 1
                time.sleep(0.2)
            dirbutton.update(screen)
            letterbutton.update(screen)
        if mousemode == "func":
            index2 = index2 % 4
            letterbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 4, 150, 75, 0.7, 0.7, "Button.png", None, ["a", "b", "c", "d"][index2])
            if letterbutton.checkcollisions():
                index2 = index2 + 1
                time.sleep(0.2)
            letterbutton.update(screen)
        if mousemode == "port":
            index = index % 2
            dirbutton = Button(850 + 125 * 3 + 40, 75 + 125 * 3, 150, 75, 0.7, 0.7, "Button.png", None, ["export", "import"][index])
            if dirbutton.checkcollisions():
                index = index + 1
                time.sleep(0.2)
            dirbutton.update(screen)


        for square in grid.squares:
            if square.rect.collidepoint(pygame.mouse.get_pos()) and pygame.key.get_pressed()[pygame.K_SPACE]:
                squarecoords = square.coords
                text(1250, 675, 200, 30, str(testlevel[squarecoords[1]][squarecoords[0]]), [255, 255, 255], screen)

            if square.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                squarecoords = square.coords

                if mousemode != "port":
                    testlevel[squarecoords[1]][squarecoords[0]] = 0

                if mousemode == "player":
                    newtestlevel = []
                    for z in range(tilesy):
                        newtestlevel.append([])
                    for i in range(tilesy):
                        for n in range(tilesx):
                            if testlevel[i][n] != 1:
                                newtestlevel[i].append(testlevel[i][n])
                            else:
                                newtestlevel[i].append(0)
                    testlevel = newtestlevel
                    testlevel[squarecoords[1]][squarecoords[0]] = 1
                if mousemode == "flag":
                    newtestlevel = []
                    for z in range(tilesy):
                        newtestlevel.append([])
                    for i in range(tilesy):
                        for n in range(tilesx):
                            if testlevel[i][n] != 2:
                                newtestlevel[i].append(testlevel[i][n])
                            else:
                                newtestlevel[i].append(0)
                    testlevel = newtestlevel
                    testlevel[squarecoords[1]][squarecoords[0]] = 2
                if mousemode == "wall":
                    testlevel[squarecoords[1]][squarecoords[0]] = 3
                if mousemode == "pushable":
                    testlevel[squarecoords[1]][squarecoords[0]] = 4
                if mousemode == "pblock":
                    if index != 4:
                        testlevel[squarecoords[1]][squarecoords[0]] = ["programblock", ["up", "down", "left", "right"][index]]
                    else:
                        if rtypefield.textstr != "" and gtypefield.textstr != "" and btypefield.textstr != "":
                            color = [int(rtypefield.textstr), int(gtypefield.textstr), int(btypefield.textstr)]
                            isvalid = True
                            for value in color:
                                if value > 255:
                                    isvalid = False
                            if isvalid:
                                testlevel[squarecoords[1]][squarecoords[0]] = ["programblock", "swap", color]
                if mousemode == "robot":
                    if rtypefield.textstr != "" and gtypefield.textstr != "" and btypefield.textstr != "":
                        color = [int(rtypefield.textstr), int(gtypefield.textstr), int(btypefield.textstr)]
                        isvalid = True
                        for value in color:
                            if value > 255:
                                isvalid = False
                        if isvalid:
                            testlevel[squarecoords[1]][squarecoords[0]] = ["robot", color]
                if mousemode == "phead":
                    if rtypefield.textstr != "" and gtypefield.textstr != "" and btypefield.textstr != "":
                        color = [int(rtypefield.textstr), int(gtypefield.textstr), int(btypefield.textstr)]
                        isvalid = True
                        for value in color:
                            if value > 255:
                                isvalid = False
                        if isvalid:
                            testlevel[squarecoords[1]][squarecoords[0]] = ["programheader", ["up", "down", "left", "right"][index], color]
                if mousemode == "battery":
                    testlevel[squarecoords[1]][squarecoords[0]] = 5
                if mousemode == "door":
                    if rtypefield.textstr != "" and gtypefield.textstr != "" and btypefield.textstr != "":
                        color = [int(rtypefield.textstr), int(gtypefield.textstr), int(btypefield.textstr)]
                        isvalid = True
                        for value in color:
                            if value > 255:
                                isvalid = False
                        if isvalid:
                            testlevel[squarecoords[1]][squarecoords[0]] = ["door", index, color]
                if mousemode == "gate":
                    if index == 1:
                        if rtypefield.textstr != "" and gtypefield.textstr != "" and btypefield.textstr != "":
                            color = [int(rtypefield.textstr), int(gtypefield.textstr), int(btypefield.textstr)]
                            isvalid = True
                            for value in color:
                                if value > 255:
                                    isvalid = False
                            if isvalid:
                                testlevel[squarecoords[1]][squarecoords[0]] = ["gate", "robot", color]
                    else:
                        testlevel[squarecoords[1]][squarecoords[0]] = ["gate", ["player", "player"][index], None]
                if mousemode == "def":
                    testlevel[squarecoords[1]][squarecoords[0]] = ["deffunction", ["a", "b", "c", "d"][index2], ["up", "down", "left", "right"][index]]
                if mousemode == "func":
                    testlevel[squarecoords[1]][squarecoords[0]] = ["function", ["a", "b", "c", "d"][index2]]
                if mousemode == "port":
                    if index == 0:
                        pyperclip.copy(testlevel)
                    if index == 1:
                        paste = pyperclip.paste()
                        paste = "testlevel = " + paste
                        exec(paste)


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
        newplayerpos = [player.gridx, player.gridy]

    if gates != []:
        for gate in gates:
            gate.update(screen)

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

    if newplayerpos != oldplayerpos or newrobotpos != oldrobotpos:
        undomoves.append(gridstate)
        oldplayerpos = newplayerpos
        oldrobotpos = newrobotpos
        gridstatetracker += 1


    dt = clock.tick(fps) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isrunning = False


    pygame.display.update()



pygame.quit()
