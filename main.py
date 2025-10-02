import pygame
from grid import Grid
from player import Player, Flag, Wall, Pushable, Door, Robot, ProgramHeader
import level
#from spritesheet import SpriteSheet

pygame.init()

WIDTH = 800
HEIGTH = 640
pygame.display.init()
screen = pygame.display.set_mode([WIDTH, HEIGTH])
clock = pygame.time.Clock()
fps = 60
dt = 0

''''
test = SpriteSheet("Doors.png")
testimage = test.get_sprite(0, 32, 32, 50, 50)
pixelarray = pygame.PixelArray(testimage)
pixelarray.replace((255, 255, 255), (255, 0, 0))
testimage = pixelarray.make_surface()
pixelarray = None
'''

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
            elif type(currenttile) == type([5,6,7,8,9]):
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

    return [tilesx, tilesy, grid, player, flag, walls, pushables, doors, robots]

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

#grid = Grid(10, 10, 3)
#player = Player(5, 5, 80, 64, 10, 10, "Player.png")
isrunning = True
while isrunning:
    screen.fill([100, 100, 100])
    dt = clock.tick(fps) / 1000
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isrunning = False

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
            pushable.update(screen)
            if checkcrush(pushable, doors):
                pushables.remove(pushable)
    if robots != []:
        for robot in robots:
            robot.update(screen, walls, pushables, doors)
            if checkcrush(robot, doors):
                robots.remove(robot)
    if player != None:
        player.update(screen, walls, pushables, doors, robots)
        if checkcrush(player, doors):
            player = None

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
    #screen.blit(testimage, pygame.rect.Rect(WIDTH / 2, HEIGTH / 2, 50, 50))
    pygame.display.flip()

    #GAMELOOP


pygame.quit()
