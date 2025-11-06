import pygame

pygame.init()
pygame.mixer.init()

kevinSound = pygame.mixer.Sound("ppm.wav")

kevinSound.play()

while True:
    print(kevinSound.get_length())

