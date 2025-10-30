import pygame

pygame.init()
pygame.mixer.init()

kevinSound = pygame.mixer.Sound("ppm.wav")

while True:
    kevinSound.play()
