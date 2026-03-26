import pygame


class Animation:
    def __init__(self, image_path, size, startFrame, numframes):
        self.spritesheet = pygame.image.load(image_path)
        self.size = size
        self.frames = []
        self.startFrame = startFrame
        self.numframes = numframes
        self.endFrame = self.startFrame + self.numframes
        self.setAnimationframes()
        self.framenum = 0
        self.totalFPS = 0

    def getframe(self, index):
        w = self.size[0]
        h = self.size[1]
        captureRect = pygame.Rect(index*w, 0, w, h)
        image = pygame.Surface((w, h)).convert_alpha()
        image.set_colorkey([0,0,0])
        image.blit(self.spritesheet, [0,0], captureRect)
        return image
    def setAnimationframes(self):
        for i in range(self.startFrame, self.endFrame):
              self.frames.append(self.getframe(i))
    def playAnimation(self, screen, pos):
        if self.framenum >= self.numframes -1:
            self.framenum = 0

        else:
            self.totalFPS += 1
            if self.totalFPS % 10 == 0:
                self.framenum += 1


        screen.blit(self.frames[self.framenum], pos)




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([750, 750])
    clock = pygame.time.Clock()
    fps = 60
    totalFPS = 0
    test = Animation("characterMoves.png", [64, 64], 0, 11)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        screen.fill("gray")
        test.playAnimation(screen, [300, 300])
        pygame.display.update()
        clock.tick(fps)
