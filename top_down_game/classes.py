import pygame, math, constants, ui, mods
from pygame.math import Vector2
from animation import Animation

SCREENWIDTH, SCREENHEIGHT = constants.SCREENWIDTH, constants.SCREENWIDTH


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.direction = Vector2(0)
        self.img = pygame.Surface([40, 80])
        self.img.fill("red")
        self.rect = self.img.get_rect(center=self.pos)
        self.speed = 275
        self.hpbar = ui.Bar(93, 22, 173, 30, "hpbar.png")
        self.maxhp = 100
        self.hp = 100
        self.manabar = ui.Bar(93, 62, 173, 30, "manabar.png")
        self.maxmana = 100
        self.mana = 100
        self.projectiles = []
        self.pmods = []
        self.mods = []
        self.money = 0
        self.defense = 0
        self.moneytext = ui.Text(f"${self.money}", 50, 107, 25, 50, [238, 255, 0])
        self.backwardsWalk = Animation("characterMoves.png", [64, 64], 0, 3, 5)
        self.forwardWalk = Animation("characterMoves.png", [64, 64], 3, 2, 5)
        self.rightWalk = Animation("characterMoves.png", [64, 64], 5, 4, 5)
        self.leftWalk = Animation("characterMoves.png", [64, 64], 9, 3, 5)
        self.backIdle = Animation("characterMoves.png", [64, 64], 10, 1, 5)
        self.leftIdle = Animation("characterMoves.png", [64, 64], 10, 1, 5)
        self.rightIdle = Animation("characterMoves.png", [64, 64], 5, 1, 5)
        self.idle = Animation("idleMoves.png", [64, 64], 0, 2, 5)
        self.facing = 0
        self.idleFacing = 0
    def addmods(self, *modifiers):
        for mod in modifiers:
            if mod[0] in mods.projectilemods:
                self.pmods.append(mod)
            else:
                self.mods.append(mod[0](self, mod[1]))

    def removemod(self, modifier, level):
        for mod in self.mods:
            if isinstance(mod, modifier) and mod.level == level:
                self.mods.remove(mod)
                break
        for pmod in self.pmods:
            if pmod == [modifier, level]:
                self.pmods.remove(pmod)
                break
    def hurt(self, damage):
        self.hp -= damage - self.defense * damage

    def update(self, camerapos, dt, bgrect, enemies, screen):
        self.screen = screen
        self.dt = dt
        self.enemies = enemies
        self.camerapos = camerapos
        self.maxmana = 100
        self.maxhp = 100
        self.manaregenmultiplier = 1
        self.manausemultiplier = 1
        mods.updatemods(self)
        self.direction = self.getInput()
        self.pos += self.direction * dt * self.speed

        if not self.rect.colliderect(bgrect):
            self.hp -= self.maxhp / 3 * dt
        else:
            self.hp += 1.25  * dt
        self.mana += 5 * self.manaregenmultiplier * dt
        self.hp = pygame.math.clamp(self.hp, 0, self.maxhp)
        self.mana = pygame.math.clamp(self.mana, 0, self.maxmana)

        self.rect.center = self.pos
        self.attack(enemies, bgrect, camerapos, dt, screen)
        self.draw(camerapos, dt, screen)



    def draw(self, camerapos, dt, screen):
        mods.renderunder(self)
        if pygame.key.get_just_pressed()[pygame.K_w] or pygame.key.get_just_pressed()[pygame.K_UP]:
            self.facing = 1
        if pygame.key.get_just_pressed()[pygame.K_a] or pygame.key.get_just_pressed()[pygame.K_LEFT]:
            self.facing = 2
        if pygame.key.get_just_pressed()[pygame.K_s] or pygame.key.get_just_pressed()[pygame.K_DOWN]:
            self.facing = 0
        if pygame.key.get_just_pressed()[pygame.K_d] or pygame.key.get_just_pressed()[pygame.K_RIGHT]:
            self.facing = 3
        if pygame.key.get_just_released()[pygame.K_s] or pygame.key.get_just_released()[pygame.K_DOWN]:
            self.facing = 4
        if pygame.key.get_just_released()[pygame.K_w] or pygame.key.get_just_released()[pygame.K_UP]:
            self.facing = 5
        if pygame.key.get_just_released()[pygame.K_a] or pygame.key.get_just_released()[pygame.K_LEFT]:
            self.facing = 6
        if pygame.key.get_just_released()[pygame.K_d] or pygame.key.get_just_released()[pygame.K_RIGHT]:
            self.facing = 7
        if self.facing == 1:
            self.backwardsWalk.playAnimation(dt)
            screen.blit(self.backwardsWalk.playAnimation(dt), self.rect.topleft - camerapos)
        self.idleMove = self.idle.playAnimation(self.dt)
        #screen.blit(self.idleMove, self.rect.topleft - camerapos)
        mods.renderover(self)
        self.hpbar.render(screen, self.hp / self.maxhp)
        self.hptext = ui.Text(f"{math.ceil(self.hp)}/{self.maxhp}", 93, 22, 10, 20, [255, 255, 255])
        self.hptext.render(screen)
        self.manabar.render(screen, self.mana / self.maxmana)
        self.manatext = ui.Text(f"{math.ceil(self.mana)}/{self.maxmana}", 93, 62, 10, 20, [255, 255, 255])
        self.manatext.render(screen)
        self.moneytext.text = f"${self.money}"
        self.moneytext.render(screen)

    def attack(self, enemies, bgrect, camerapos, dt, screen):
        if pygame.mouse.get_just_pressed()[0] or pygame.key.get_just_pressed()[pygame.K_SPACE]:
            self.shootangle = pygame.mouse.get_pos() - (self.pos - camerapos)
            self.newprojectile = Projectile(self.pos[0], self.pos[1], 30, 20, "playerprojectile.png", self.shootangle, 300, 60, self.pmods)
            if self.newprojectile.manacost <= self.mana:
                self.projectiles.append(self.newprojectile)
                self.mana -= self.newprojectile.manacost

        for projectile in self.projectiles:
            projectile.update(enemies, dt, camerapos, screen)
            if not projectile.rect.colliderect(bgrect) or projectile.lifetime <= 0:
                self.projectiles.remove(projectile)


    def getInput(self):
        direction = Vector2(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x = 1
        if direction != Vector2(0):
            direction.normalize_ip()
        return direction

class Enemy:
    def __init__(self, cx, cy, w, h, image, hp, spd, dmg, atkspd, cost, mods=[]):
        self.pos = [cx, cy]
        self.w = w
        self.h = h
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, [self.w, self.h])
        self.image.set_colorkey([0, 0, 0])
        self.imagemask = pygame.mask.from_surface(self.image)
        self.hurtimage = self.imagemask.to_surface(None, None, None, [255, 191, 191])
        self.hurtimage.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect(center=self.pos)
        self.pasthp = hp
        self.pastaniframes = 0
        self.hp = hp
        self.MAXHP = hp
        self.spd = spd
        self.dmg = dmg
        self.atkspd = atkspd
        self.atkcooldown = 1 / self.atkspd
        self.mods = mods
        self.aniframes = 0
        self.state = "idle"
        self.cost = cost
        self.defense = 0
        self.mods = []
        for mod in mods:
            self.mods.append(mod(self))


    def render(self, dt, camerapos, screen):
        mods.renderunder(self)
        screen.blit(self.image, self.rect.topleft - camerapos)
        mods.renderover(self)
        self.redflash(dt, camerapos, screen)
        self.bar = ui.Bar(self.rect.centerx, self.rect.top - 15, self.rect.w + 10, 10, "hpbar.png", 5, 5)
        self.bar.center = self.bar.center - camerapos
        self.bar.render(screen, self.hp / self.MAXHP)

    def updatepos(self, player, dt):
        self.velocity = pygame.math.Vector2(player.pos - self.pos)
        self.velocity.normalize_ip()
        self.velocity *= self.spd
        self.pos += self.velocity * dt
        self.rect.center = self.pos

    def attack(self, player, dt):
        self.atkcooldown -= dt
        self.atkcooldown = max(0, self.atkcooldown)
        if self.atkcooldown == 0 and self.rect.colliderect(player.rect):
            player.hurt(self.dmg)
            self.atkcooldown = 1 / self.atkspd

    def updatestate(self):
        if self.hp != self.pasthp and self.hp > 0:
            self.pasthp = self.hp
            self.pastaniframes = self.aniframes
            self.state = "hurt"
        if self.hp <= 0 and self.state != "dying":
            self.pastaniframes = self.aniframes
            self.state = "dying"

    def redflash(self, dt, camerapos, screen):
        if (self.aniframes - self.pastaniframes) * dt <= 0.1:
            self.hurtrender = self.hurtimage.copy()
            self.weight = (self.aniframes - self.pastaniframes) * dt / 0.1
            self.hurtrender.set_alpha(pygame.math.lerp(200, 0, self.weight))
            screen.blit(self.hurtrender, self.rect.topleft - camerapos)
        else:
            self.state = "idle"

    def hurt(self, damage):
        self.hp -= damage - self.defense * damage

    def repel(self, enemies, player, dt):
        if math.dist(self.pos, player.pos) >= 100:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    self.repelvel = Vector2(self.pos - enemy.pos)
                    if self.repelvel.length() != 0:
                        self.repelvel.normalize_ip()
                        self.repelvel *= self.spd * dt
                        self.pos += self.repelvel
    def dead(self, dt, camerapos, screen):
        if (self.aniframes - self.pastaniframes) * dt <= 0.2:
            self.weight = (self.aniframes - self.pastaniframes) * dt / 0.2
            self.deathimage = self.image.copy()
            self.deathimage = pygame.transform.scale(self.deathimage, [pygame.math.lerp(self.w, self.w * 1.5, self.weight), pygame.math.lerp(self.h, self.h * 1.5, self.weight)])
            self.deathimage.set_colorkey([0, 0, 0])
            self.deathimage.set_alpha(pygame.math.lerp(255, 0, self.weight))
            self.rect = self.deathimage.get_rect(center=self.pos)
            screen.blit(self.deathimage, self.rect.topleft - camerapos)
        else:
            self.state = "dead"


    def update(self, player, enemies, camerapos, dt, screen):
        self.dt = dt
        mods.updatemods(self)
        self.updatestate()
        if self.state != "dying" and self.state != "dead":
            self.attack(player, dt)
            self.updatepos(player, dt)
            self.repel(enemies, player, dt)
            self.render(dt, camerapos, screen)
        if self.state == "hurt":
            self.redflash(dt, camerapos, screen)
        elif self.state == "dying":
            self.dead(dt, camerapos, screen)
        self.aniframes += 1


class Projectile:
    def __init__(self, cx, cy, w, h, image, velocity, spd, dmg, mods=[]):
        self.cx = cx
        self.cy = cy
        self.pos = [self.cx, self.cy]
        self.w = w
        self.h = h
        self.velocity = velocity.normalize()
        self.image = pygame.image.load(image)
        self.image.set_colorkey([0, 0, 0])
        self.image = pygame.transform.scale(self.image, [self.w, self.h])
        self.image = pygame.transform.rotate(self.image, self.velocity.angle_to(pygame.Vector2(1, 0)))
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect(center=self.pos)
        self.spd = spd
        self.dmg = dmg
        self.alreadycollide = []
        self.lifetime = 0.75
        self.manacost = 8
        self.mods = []
        for mod in mods:
            self.mods.append(mod[0](self, mod[1]))

    def render(self, camerapos, screen):
        mods.renderover(self)
        screen.blit(self.image, self.pos - camerapos)
        mods.renderover(self)

    def updatepos(self, dt):
        self.velocity = self.velocity.normalize()
        self.velocity *= self.spd
        self.pos += self.velocity * dt
        self.rect.center = self.pos

    def collide(self, collidables):
        self.collidables = collidables
        if not isinstance(self.collidables, list):
            self.collidables = [collidables]
        for collidable in self.collidables:
            if collidable in self.alreadycollide and not self.rect.colliderect(collidable.rect):
                self.alreadycollide.remove(collidable)
            if self.rect.colliderect(collidable.rect) and not collidable in self.alreadycollide:
                collidable.hurt(self.dmg)
                self.alreadycollide.append(collidable)

    def fade(self):
        self.weight = self.lifetime / 0.15
        self.image.set_alpha(pygame.math.lerp(0, 255, self.weight))

    def update(self, collidables, dt, camerapos, screen):
        self.dt = dt
        self.screen = screen
        self.updatepos(dt)
        self.collidables = collidables
        mods.updatemods(self)
        self.collide(collidables)
        self.render(camerapos, screen)
        if self.lifetime <= 0.15:
            self.fade()
        self.lifetime -= dt


