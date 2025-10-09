import pygame
from grid import Grid

pygame.init()


WIDTH,HEIGHT = 800,640
screen = pygame.display.set_mode([WIDTH,HEIGHT])
clock = pygame.time.Clock()
fps = 60
dt = 0

g = Grid([WIDTH,HEIGHT])

kevinSound = pygame.mixer.Sound("kevinSound.wav")



soundPlay = False

def draw(screen):
    screen.fill("grey")
    g.draw(screen)


def update():
    global soundPlay
    g.update()
    if not soundPlay:
        kevinSound.play()
        soundPlay = True

isRunning = True
while isRunning:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            isRunning = False

    update()
    draw(screen)
    dt = clock.tick(fps)/1000
    pygame.display.update()
pygame.quit()
    