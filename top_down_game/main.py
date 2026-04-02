import pygame, constants, ui, classes, wavedata, popup

pygame.init()

SCREENWIDTH, SCREENHEIGHT = constants.SCREENWIDTH, constants.SCREENWIDTH

screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
clock = pygame.time.Clock()
fps = 60

#PLAYER
player = classes.Player([SCREENWIDTH / 2, SCREENHEIGHT / 2])
dt = 0
debug = False

camerapos = pygame.math.Vector2(0)

gamestate = "game"
bg = pygame.image.load("bg.png")
bg = pygame.transform.smoothscale(bg, [SCREENWIDTH * 2, SCREENHEIGHT * 2])
bg.set_colorkey([0, 0, 0])
bgrect = bg.get_rect(center=[SCREENWIDTH/2, SCREENHEIGHT/2])

totalenemies = 0
enemies = []
wavestate = "nowave"
wavenum = 0
wavebutton = ui.Button(-3, 634, 75, 75, "wavebutton.png", isui=False)
wavetext = ui.Text("PLACEHOLDER", -2, 568, 10, 30, [255, 255, 255])
inventorybutton = ui.Button(35, 165, 50, 50, "inventorybutton.png")

shoprect = pygame.rect.Rect(391, 308, 112, 167)
shoptext = ui.Text("Press SPACE to open shop", 436, 260, 10, 30, [255, 255, 255])
shop = popup.Shop(593, 515, 400, 500)
inventory = popup.Inventory(204, 384, 400, 500)
forgerect = pygame.rect.Rect(-143, 43, 170, 138)
forgetext = ui.Text("Press SPACE to open forge", -58, 3, 10, 30, [255, 255, 255])
forge = popup.Forge(424, 384, 700, 500)
shopopen = False
inventoryopen = False
forgeopen = False

def drawgamebg(screen):
    screen.fill([255, 210, 210])
    screen.blit(bg, bgrect.topleft - camerapos)

def updategame(dt):
    global wavestate, enemies, totalenemies, wavetext, wavenum, shopopen, inventoryopen, forgeopen, isrunning

    #UPDATE WAVE
    wavebutton.render(screen, camerapos)
    if wavebutton.checkcollisions(player):
        if wavestate == "nowave":
            wavetext = ui.Text(f"Press SPACE to start wave {wavenum + 1}", -2, 568, 10, 30, [255, 255, 255])
            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                enemies = wavedata.summon(wavenum)
                totalenemies = len(enemies)
                wavestate = "wave"
        wavetext.render(screen, camerapos)
    if wavestate == "wave":
        wavetext = ui.Text(f"Wave {wavenum + 1}: {len(enemies)}/{totalenemies} enemies remaining", -2, 568, 10, 30, [255, 255, 255])
        wavetext.render(screen, camerapos)
        if enemies == []:
            wavenum += 1
            shop.restockshop()
            wavestate = "nowave"

    #UPDATE PLAYER
    player.update(camerapos, dt, bgrect, enemies, screen)
    if debug:
        player.money = 9999
    if player.hp <= 0 and not debug:
        isrunning = False

    #UPDATE ENEMIES 
    for enemy in enemies:
        enemy.update(player, enemies, camerapos, dt, screen)
        #enemy.render(dt, camerapos, screen)
        if enemy.state == "dead":
            player.money += enemy.cost
            enemies.remove(enemy)
    if pygame.key.get_just_pressed()[pygame.K_e]:
        print("playerpos", player.pos)
        print("mousepos", pygame.mouse.get_pos())
    camerapos.x = pygame.math.lerp(camerapos.x, player.pos.x - SCREENWIDTH / 2, 0.075)
    camerapos.y = pygame.math.lerp(camerapos.y, player.pos.y - SCREENHEIGHT / 2, 0.075)

    #UPDATE SHOP
    if player.rect.colliderect(shoprect) and wavestate == "nowave":
        shoptext.render(screen, camerapos)
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            shopopen = True
    if shopopen:
        shop.update(player, inventory, screen)
        if shop.exitbutton.checkcollisions():
            shopopen = False

    #UPDATE FORGE
    if player.rect.colliderect(forgerect) and wavestate == "nowave":
        forgetext.render(screen, camerapos)
        if pygame.key.get_just_pressed()[pygame.K_SPACE]:
            forgeopen = True
    if forgeopen:
        forge.update(player, inventory, screen)
        if forge.exitbutton.checkcollisions():
            forgeopen = False



    #UPDATE INVENTORY
    inventorybutton.render(screen)
    if inventorybutton.checkcollisions() and not inventoryopen:
        inventoryopen = True
    if inventoryopen:
        inventory.update(player, screen)
        if inventory.exitbutton.checkcollisions():
            inventoryopen = False

isrunning = True
while isrunning:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isrunning = False
    if gamestate == "game":
        drawgamebg(screen)
        updategame(dt)
    dt = clock.tick(fps)/1000
    pygame.display.update()

pygame.quit()