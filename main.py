import pygame
from grid import Grid
from player import Player, Flag, Wall, Pushable, Door, Robot, ProgramHeader, Gate, Function
import level
from ui import Button

pygame.init()

WIDTH = 750
HEIGTH = 750
pygame.display.init()
screen = pygame.display.set_mode([WIDTH, HEIGTH])
clock = pygame.time.Clock()
fps = 60
dt = 0
undomoves = []

def checkcrush(object, doors):
    for door in doors:
        if object.coordsx == door.coordsx and object.coordsy == door.coordsy and door.frame == 1:
            return True
    return False

def generatelevel(index):
    currentlevel = level.levels[index]
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
                    pushables.append(Pushable(n, i, WIDTH / tilesx, HEIGTH / tilesy, tilesx, tilesy, "Pushables.png", 1, command, dir))
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

def text(centerx, centery, w, h, txt, color):
    font = pygame.font.Font("pixelfont.ttf")
    fontrect = pygame.rect.Rect(3, 4, w, h)
    fontrect.center = [centerx, centery]
    fontsurface = font.render(txt, False, color)
    fontsurface = pygame.transform.scale(fontsurface, (w, h))
    screen.blit(fontsurface, fontrect)

levelnumber = 0

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



#GAMELOOP
isrunning = True
gamestate = "startmenu"
while isrunning:
    screen.fill([150, 150, 150])
    if gamestate == "startmenu":
        text(375, 50, 500, 50, "Game Title", [100, 100, 100])
        startbutton = Button(375, 375, 567, 67, 0.5, 0.95, "Button.png", "placeholder", "Start Game")
        startbutton.update(screen)
        if startbutton.checkcollisions():
            gamestate = "game"

    elif gamestate == "game":
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
        if player != None:
            player.update(screen, walls, pushables, doors, robots, gates)
            if checkcrush(player, doors):
                player = None

        if gates != []:
            for gate in gates:
                gate.update(screen)
        '''
        if undomoves == [] or undomoves[-1] != [doors, flag, walls, pushables, robots, player, gates]:
            undomoves.append([doors, flag, walls, pushables, robots, player, gates].copy())
        print(len(undomoves))
        '''

        if player != None and flag != None:
            if player.state == "movecooldown" or player.state == "idle":
                if [player.coordsx, player.coordsy] == [flag.coordsx, flag.coordsy]:
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

        if pygame.key.get_pressed()[pygame.K_r]:
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

    dt = clock.tick(fps) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isrunning = False
    #screen.blit(testimage, pygame.rect.Rect(WIDTH / 2, HEIGTH / 2, 50, 50))
    pygame.display.update()

    #GAMELOOP


pygame.quit()
