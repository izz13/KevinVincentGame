import pygame, random, math
pygame.init()


#PROJECTILE
class Lifetime:
    shopimage = "lifetime.png"
    maxlevel = 3
    def __init__(self, projectile, level):
        self.projectile = projectile
        self.projectile.lifetime += 0.25
        self.level = level

    def update(self):
        pass
    def renderunder(self):
        pass
    def renderover(self):
        pass

class Sharptip:
    shopimage = "sharp.png"
    def __init__(self, projectile, level):
        self.projectile = projectile
        self.projectile.dmg += 22
        self.projectile.manacost += 3
        self.level = level

    def update(self):
        pass
    def renderunder(self):
        pass
    def renderover(self):
        pass


class Poisontip:
    shopimage = "poison.png"
    maxlevel = 9
    def __init__(self, projectile, level):
        self.projectile = projectile
        self.projectile.manacost += 3.5
        self.level = level

    def update(self):
        for enemy in self.projectile.collidables:
            if self.projectile.rect.colliderect(enemy.rect):
                if not enemy in self.projectile.alreadycollide:
                    enemy.mods.append(StatusPoison(enemy, 52))


    def renderunder(self):
        pass

    def renderover(self):
        pass


#PLAYER
class Heal:
    shopimage = "heal.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.level = level

    def update(self):
        if self.player.mana >= 3:
            self.player.hp += 6 * self.player.dt
            self.player.mana -= 3 * self.player.dt
    def renderunder(self):
        pass
    def renderover(self):
        pass

class Antiheal:
    shopimage = "antiheal.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.level = level

    def update(self):
        if pygame.key.get_pressed()[pygame.K_c]:
            self.player.hp -= 30 * self.player.dt
            self.player.mana += 9 * self.player.dt

    def renderunder(self):
        pass
    def renderover(self):
        pass

class Teleport:
    shopimage = "teleportanchor.png"
    maxlevel = 3
    def __init__(self, player, level):
        self.player = player
        self.state = "inactive"
        self.cooldown = 0
        self.direction = 0
        self.scale = 125
        self.ogimage = pygame.image.load("teleportanchor.png")
        self.ogimage = pygame.transform.scale(self.ogimage, [100, 100])
        self.ogimage.set_colorkey([0, 0, 0])
        self.pos = [0, 0]
        self.rect = self.ogimage.get_rect(center = self.pos)
        self.aniframes = 0
        self.level = level

    def update(self):
        if pygame.key.get_just_pressed()[pygame.K_v] and self.state == "inactive" and self.cooldown <= 0 and self.player.mana >= 50:
            self.pos = self.player.pos.copy()
            self.state = "active"
            self.player.mana -= 50
        if self.state == "active":
            if pygame.key.get_just_pressed()[pygame.K_b]:
                self.player.pos = self.pos
                self.state = "inactive"
                self.cooldown = 10
        self.direction += 60 * self.player.dt
        self.direction = self.direction % 360
        self.weight = 0.5 * math.sin(self.aniframes) + 0.5
        self.scale = pygame.math.lerp(100, 150, self.weight)
        self.cooldown -= self.player.dt
        self.aniframes += self.player.dt


    def renderunder(self):
        if self.state == "active":
            self.image = pygame.transform.rotate(self.ogimage, self.direction)
            self.image = pygame.transform.scale(self.image, [self.scale, self.scale])
            self.rect = self.image.get_rect(center=self.pos)
            self.player.screen.blit(self.image, self.rect.topleft - self.player.camerapos)
            self.player.mana -= 3 * self.player.dt
    def renderover(self):
        pass

class Morehealth:
    shopimage = "morehealth.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.level = level
    def update(self):
        self.player.maxhp += 25
    def renderunder(self):
        pass
    def renderover(self):
        pass
#MANA
class Managamble:
    shopimage = "managamble.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.cooldown = 0
        self.duration = 5
        self.state = "idle"
        self.manamultiplier = 1
        self.level = level

    def update(self):
        self.player.manaregenmultiplier *= self.manamultiplier
        if self.state == "idle":
            self.cooldown -= self.player.dt
            if self.cooldown <= 0 and pygame.key.get_just_pressed()[pygame.K_z]:
                self.state = "active"
                self.cooldown = 8.5
                if self.player.manaregenmultiplier == 1:
                    if random.randint(1,2) == 1:
                        self.manamultiplier = 2
                    else:
                        self.manamultiplier = 1 / 2
                elif self.player.manaregenmultiplier > 1:
                    self.manamultiplier = 2
                else:
                    self.manamultiplier = 1 / 2
        if self.state == "active":
            self.duration -= self.player.dt
            if self.duration <= 0:
                self.state = "idle"
                self.duration = 5
                self.manamultiplier = 1



    def renderunder(self):
        pass
    def renderover(self):
        pass

class Manaburst:
    shopimage = "manaburst.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.duration = 10
        self.cooldown = 0
        self.state ="inactive"
        self.level = level

    def update(self):
        self.cooldown -= self.player.dt
        if pygame.key.get_just_pressed()[pygame.K_x] and self.cooldown <= 0 and self.state == "inactive":
            self.duration = 10
            self.state = "increase"
        if self.state == "increase":
            self.player.mana += 6 * self.player.dt
            self.duration -= self.player.dt
            if self.duration <= 5:
                self.state = "decrease"
        if self.state == "decrease":
            self.duration -= self.player.dt
            self.player.mana -= 6 * self.player.dt
            if self.duration <= 0:
                self.state = "inactive"
                self.cooldown = 15



    def renderunder(self):
        pass
    def renderover(self):
        pass

class Managain:
    shopimage = "managain.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.level = level

    def update(self):
        self.player.mana += 3 * self.player.dt * self.player.manaregenmultiplier

    def renderunder(self):
        pass
    def renderover(self):
        pass

class Moremana:
    shopimage = "moremana.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.level = level
    def update(self):
        self.player.maxmana += 25
    def renderunder(self):
        pass
    def renderover(self):
        pass

#STATUS
class StatusPoison:
    def __init__(self, target, dps):
        self.target = target
        self.dps = dps
        self.duration = 6.7
        self.total = 6.7


    def update(self):
        self.target.hp -= self.dps / self.total * self.target.dt
        self.duration -= self.target.dt
        if self.duration <= 0:
            self.target.mods.remove(self)

    def renderunder(self):
        pass
    def renderover(self):
        pass

#ENEMY MODS




#UTILS
def updatemods(self):
    for mod in self.mods:
        mod.update()
def renderunder(self):
    for mod in self.mods:
        mod.renderunder()
def renderover(self):
    for mod in self.mods:
        mod.renderover()


projectilemods = [Lifetime, Sharptip, Poisontip]
playermods = [Heal, Antiheal, Teleport, Morehealth]
manamods = [Managamble, Manaburst, Managain, Moremana]

#14 total mod slots