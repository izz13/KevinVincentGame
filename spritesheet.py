import pygame
class SpriteSheet:
  def __init__(self, image, load=True):
    if load:
      self.sheet = pygame.image.load(image)
    else:
      self.sheet = image

  def get_sprite(self, frame, w, h, sw, sh):
    image = pygame.Surface((w, h)).convert_alpha()
    image.blit(self.sheet, (0, 0), [(frame * w), 0, w, h])
    image = pygame.transform.scale(image, [sw, sh])
    image.set_colorkey([0, 0, 0])
    return image
