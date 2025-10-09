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

manAnimation = pygame.image.load_animation("coachStuff/05 zx .gif")
print(manAnimation)
aniTimer = 0
aniCooldown = 1/15
index = 0
dt = 0

soundPlay = False

def draw(screen,dt):
    global aniTimer,aniCooldown,index
    screen.fill("grey")
    length = len(manAnimation)
    frame = manAnimation[index%length][0]
    screen.blit(frame,frame.get_rect(center = [WIDTH/2,HEIGHT/2]))
    if aniTimer > aniCooldown:
        index += 1
        aniTimer = 0
    else:
        aniTimer += dt
    print(aniTimer)
    #g.draw(screen)


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
    draw(screen,dt)
    dt = clock.tick(fps)/1000
    pygame.display.update()
pygame.quit()
    