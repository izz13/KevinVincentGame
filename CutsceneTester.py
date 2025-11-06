import pygame
import ui
from ui import *
pygame.init()

WIDTH = 750
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
events = pygame.event.get()
img1 = pygame.image.load("Cut3.png")
img1 = pygame.transform.scale(img1, [750, 750])
img2 = pygame.image.load("Cut2.png")
img2 = pygame.transform.scale(img2, [750, 750])
img3 = pygame.image.load("Cut1.png")
img3 = pygame.transform.scale(img3, [750, 750])
list = [img1, img2, img3]
number = 0
nextframebutton = Button(750/2, 750/2, 200, 100, 0.8, 0.9, "Buton.png", None, "NEXT")


def Button():
    global number
    if event.type == pygame.MOUSEBUTTONDOWN:
        number +=1
    if number == 1:
        screen.blit(list[0])
    elif number == 2:
        screen.blit(list[1])
    elif number == 3:
        screen.blit(list[2])


hasclicked = False
while running:
    global buttonRect
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if number == 1:
        screen.blit(list[0])
    elif number == 2:
        screen.blit(list[1])
    elif number == 3:
        screen.blit(list[2])

    nextframebutton.update(screen)
    if nextframebutton.checkcollisions():
        hasclicked = True
    elif hasclicked:
        hasclicked = False
        number += 1

    pygame.display.update()

    #Button()
pygame.quit()

