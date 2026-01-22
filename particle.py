import math
import pygame
import random
pygame.init()
class Particle:
    def __init__(self, x, y, w, h,  direction, friction, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.Surface([w, h])
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.img.fill("yellow")
        self.direction = direction
        self.friction = friction
        self.speed = speed
        self.xv = math.cos(math.radians(direction)) * speed
        self.yv = -math.sin(math.radians(direction)) * speed
        self.aniframes = 0
        self.color = [255, 255, 0]

    def updatepos(self):
        self.x += self.xv
        self.y += self.yv
        self.xv *= self.friction
        self.yv *= self.friction
        self.rect.centerx = self.x
        self.rect.centery = self.y
    def render(self, screen):
        self.img.fill(self.color)
        screen.blit(self.img, self.rect)
    def update(self, screen):
        self.updatepos()
        self.render(screen)
if __name__ == "__main__":
    pygame.init()
    particles = []
    screen = pygame.display.set_mode((500, 500))
    running = True
    clock = pygame.time.Clock()
    fps = 60
    def spawnparticles():
        global particles
        mousepos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        particlenum = random.randint(10, 15)
        if clicked:
            for x in range(particlenum):
                particles.append(Particle(mousepos[0], mousepos[1], 5, 5, random.randint(0, 360), 0.9, random.randint(5, 20)))
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill("black")
        spawnparticles()
        for particle in particles:
            if particle.xv**2 + particle.yv **2 < 0.01:
                particles.remove(particle)
            particle.update(screen)
        clock.tick(fps)
        pygame.display.update()