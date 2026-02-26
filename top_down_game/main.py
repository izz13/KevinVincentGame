import pygame

from player import Player
#Import the player class from the player file

pygame.init()

SCREENWIDTH, SCREENHEIGHT = 800,640

screen = pygame.display.set_mode([SCREENWIDTH,SCREENHEIGHT])
clock = pygame.time.Clock()
fps = 60
player = Player([SCREENWIDTH/2, SCREENHEIGHT/2])

dt = 0

#you should make the player object here


def draw(screen):
    screen.fill("black")
    player.draw(screen)

def update(events,dt):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
    player.update(dt)




while True:
    events = pygame.event.get()
    update(events,dt)
    draw(screen)
    dt = clock.tick(fps)/1000
    pygame.display.update()