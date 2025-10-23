import pygame

WIDTH = 750
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
events = pygame.event.get()
img1 = pygame.image.load("Cut3.png")
img1 = pygame.transform.scale(img1, [750, 750])



def Button():
    button = pygame.Surface((100, 100))
    buttonRect = pygame.Rect(375, 375, 100, 100)
    screen.blit(button, buttonRect)

while running:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


    pygame.display.update()
    screen.blit(img1, [0,0])
    Button()
pygame.quit()

