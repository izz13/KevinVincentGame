import pygame, random, math
pygame.init()


#PROJECTILE
class Fast:
    shopimage = "speed.png"
    maxlevel = 9
    def __init__(self, projectile, level):
        self.projectile = projectile
        self.updateinput = "[]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.projectile.spd *= 1.5
        self.projectile.dmg -= 6.5
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
        self.updateinput = "[]"
        self.underinput = "[]"
        self.overinput = "[]"
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
        self.updateinput = "[self.collidables]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.projectile.manacost += 3.5
        self.level = level

    def update(self, enemies):
        for enemy in enemies:
            if self.projectile.rect.colliderect(enemy.rect):
                if not enemy in self.projectile.alreadycollide:
                    enemy.mods.append(StatusPoison(enemy, 32))



    def renderunder(self):
        pass

    def renderover(self):
        pass

class GoldenArrow:
    shopimage = "GoldenArrow.png"
    maxlevel = 9
    def __init___(self, projectile, level):
        self.projectile = projectile
        self.level = level
        self.updateinput = "[self.dt, self.collidables, self.screen]"
        self.underinput = "[self.dt, self.screen]"
        self.overinput = "[]"
        self.projectile.manacost += 1.5
        self.anitime = 0
        self.firesurf = pygame.surface.Surface([20, 20])
        pygame.draw.circle(self.firesurf, [255, 100, 0], [10, 10], 10)

    def update(self, dt, screen):
        self.anitime += dt

#PLAYER
class Heal:
    shopimage = "heal.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.updateinput = "[self.dt]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.level = level

    def update(self, dt):
        if self.player.mana >= 3:
            self.player.hp += 2 * dt
            self.player.mana -= 3 * dt
    def renderunder(self):
        pass
    def renderover(self):
        pass

class Antiheal:
    shopimage = "antiheal.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.updateinput = "[self.dt]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.level = level

    def update(self, dt):
        if pygame.key.get_pressed()[pygame.K_c]:
            self.player.hp -= 18 * dt
            self.player.mana += 9 * dt

    def renderunder(self):
        pass
    def renderover(self):
        pass

class Teleport:
    shopimage = "teleportanchor.png"
    maxlevel = 3
    def __init__(self, player, level):
        self.player = player
        self.updateinput = "[self.dt]"
        self.underinput = "[self.dt, self.screen, self.camerapos]"
        self.overinput = "[]"
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

    def update(self, dt):
        if pygame.key.get_just_pressed()[pygame.K_v] and self.state == "inactive" and self.cooldown <= 0 and self.player.mana >= 50:
            self.pos = self.player.pos.copy()
            self.state = "active"
            self.player.mana -= 50
        if self.state == "active":
            if pygame.key.get_just_pressed()[pygame.K_b]:
                self.player.pos = self.pos
                self.state = "inactive"
                self.cooldown = 10
        self.direction += 60 * dt
        self.direction = self.direction % 360
        self.weight = 0.5 * math.sin(self.aniframes) + 0.5
        self.scale = pygame.math.lerp(100, 150, self.weight)
        self.cooldown -= dt
        self.aniframes += dt


    def renderunder(self, dt, screen, camerapos):
        if self.state == "active":
            self.image = pygame.transform.rotate(self.ogimage, self.direction)
            self.image = pygame.transform.scale(self.image, [self.scale, self.scale])
            self.rect = self.image.get_rect(center=self.pos)
            screen.blit(self.image, self.rect.topleft - camerapos)
            self.player.mana -= 3 * dt
    def renderover(self):
        pass

class Morehealth:
    shopimage = "morehealth.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.updateinput = "[]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.level = level
    def update(self):
        self.player.maxhp += 50
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
        self.updateinput = "[self.dt]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.cooldown = 0
        self.duration = 5
        self.state = "idle"
        self.manamultiplier = 1
        self.level = level

    def update(self, dt):
        self.player.manaregenmultiplier *= self.manamultiplier
        if self.state == "idle":
            self.cooldown -= dt
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
            self.duration -= dt
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
        self.updateinput = "[self.dt]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.duration = 10
        self.cooldown = 0
        self.state ="inactive"
        self.level = level

    def update(self, dt):
        self.cooldown -= dt
        if pygame.key.get_just_pressed()[pygame.K_x] and self.cooldown <= 0 and self.state == "inactive":
            self.duration = 10
            self.state = "increase"
        if self.state == "increase":
            self.player.mana += 6 * dt
            self.duration -= dt
            if self.duration <= 5:
                self.state = "decrease"
        if self.state == "decrease":
            self.duration -= dt
            self.player.mana -= 6 * dt
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
        self.updateinput = "[self.dt]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.level = level

    def update(self, dt):
        self.player.mana += 3 * dt * self.player.manaregenmultiplier

    def renderunder(self):
        pass
    def renderover(self):
        pass

class Moremana:
    shopimage = "moremana.png"
    maxlevel = 9
    def __init__(self, player, level):
        self.player = player
        self.updateinput = "[]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.level = level
    def update(self):
        self.player.maxmana += 30
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
        self.updateinput = "[self.dt, self.mods]"
        self.underinput = "[]"
        self.overinput = "[]"


    def update(self, dt, mods):
        self.target.hp -= self.dps / self.total * dt
        self.duration -= dt
        if self.duration <= 0:
            mods.remove(self)

    def renderunder(self):
        pass
    def renderover(self):
        pass

#ENEMY MODS
class Enemyfast:
    shopimage = "moremana.png"
    maxlevel = 9
    def __init__(self, enemy):
        self.enemy = enemy
        self.updateinput = "[]"
        self.underinput = "[]"
        self.overinput = "[]"
        self.enemy.spd = 8
    def update(self):
        pass
    def renderunder(self):
        pass
    def renderover(self):
        pass



#UTILS
def updatemods(self):
    for mod in self.mods:
        exec("self.input = " + mod.updateinput)
        mod.update(*self.input)
def renderunder(self):
    for mod in self.mods:
        exec("self.input = " + mod.underinput)
        mod.renderunder(*self.input)
def renderover(self):
    for mod in self.mods:
        exec("self.input = " + mod.overinput)
        mod.renderover(*self.input)


projectilemods = [Fast, Sharptip, Poisontip]
playermods = [Heal, Antiheal, Teleport, Morehealth]
manamods = [Managamble, Manaburst, Managain, Moremana]

#14 total mod slots