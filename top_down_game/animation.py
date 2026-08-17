import pygame


class Animation:
    def __init__(self, image_path, size, startFrame, numframes, fps):
        self.spritesheet = pygame.image.load(image_path)
        self.size = size
        self.frames = []
        self.startFrame = startFrame
        self.numframes = numframes + 1
        self.endFrame = self.startFrame + self.numframes - 1
        self.setAnimationframes()
        self.framenum = 0
        self.totalFPS = 0
        self.spf = 1/fps

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
    def playAnimation(self, dt):
        self.totalFPS += dt
        if self.totalFPS >= self.spf:
            self.framenum += 1
            if self.framenum >= self.numframes - 1:
                self.framenum = 0
            self.totalFPS = 0
        return self.frames[self.framenum]



dt = 0
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode([750, 750])
    clock = pygame.time.Clock()
    fps = 60
    totalFPS = 0
    test = Animation("characterMoves.png", [64, 64], 0, 11, 30)
    backwardWalk = Animation("characterMoves.png", [64, 64], 0, 3, 5)
    forwardWalk = Animation("characterMoves.png", [64,64], 3, 2, 5)
    rightWalk = Animation("characterMoves.png", [64,64], 5, 4, 5)
    leftWalk = Animation("characterMoves.png", [64, 64], 9, 3, 5)
    idleWalk = Animation("idleMoves.png", [64, 64], 0, 2, 5)
    rightIdle = Animation("characterMoves.png", [64, 64], 5, 1, 5)
    leftIdle = Animation("characterMoves.png", [64, 64], 10, 1, 5)
    backIdle = Animation("characterMoves.png", [64, 64], 0, 1, 5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        screen.fill("gray")
        img = backwardWalk.playAnimation(dt)
        img2 = forwardWalk.playAnimation(dt)
        img3 = rightWalk.playAnimation(dt)
        img4 = leftWalk.playAnimation(dt)
        img5 = idleWalk.playAnimation(dt)
        img6 = rightIdle.playAnimation(dt)
        #screen.blit(img, [750/2, 750/2])
        #screen.blit(img2, [750/2, 750/2])
        #screen.blit(img3, [750/2, 750/2])
        #screen.blit(img4, [750/2, 750/2])
        #screen.blit(img6, [750/2, 750/2])
        #screen.blit(img5, [750/2, 750/2])
        pygame.display.update()
        dt = clock.tick(fps) / 1000
