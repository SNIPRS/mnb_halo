import pygame 
import numpy as np
from math import ceil
from typing import Tuple, Optional
from random import randint

import G
from sprite.decal import BulletImpact
from utils import displacement, rect_center, distance

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start: Tuple[float, float], end: Optional[Tuple[float, float]] = None,
                 initial_delay: Optional[int] = 0):
        super().__init__()
        self.start = start
        self.end = end
        self.initial_delay = initial_delay
        self.dmg = 0
        self.r = 1

    def frame(self):
        if self.initial_delay <= 0:
            self.apply()
        self.initial_delay -= 1
        if self.initial_delay <= -2:
            self.kill()

    def _damage(self):
        for c in G.CHARS_ALL:
            c.hit(self.end, self.dmg)

    def _r_damage(self):
        for c in G.CHARS_ALL:
            d = distance((c.x, c.y), self.end)
            if d < self.r:
                c.hit(self.end, int(self.dmg*(1-d/(self.r+1))))


class ProjectileBullet(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)

        self.colour = (255, 234, 0)
        self.width = 1
        self.dmg = 10
        self.done = False

    def apply(self):
        pygame.draw.line(G.WINDOW, (255, 255, 255), self.start, self.end, 2)
        pygame.draw.line(G.WINDOW, self.colour, self.start, self.end, self.width)
        _, dx, dy = displacement(self.start, self.end)
        impact = BulletImpact(self.end, (dx, dy))
        G.DECALS.add(impact)
        self._damage()
        self.done = True

class ProjectileShotgunShell(ProjectileBullet):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        self.colour = (255, 234, 0)
        self.width = 1
        self.dmg = 20

class ProjectileBolt(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        self.colour = (100, 100, 255)
        self.dmg = 20
        self.drawr = 3
        self.x, self.y = start
        self.speed = 5
        self.done = False
        dis, self.dx, self.dy = displacement(start, end)
        self.apply_frames = ceil(dis/self.speed)

    def frame(self):
        if self.initial_delay > 0:
            self.initial_delay -= 1
            return
        self.apply_frames -= 1
        if self.apply_frames > 0:
            pygame.draw.circle(G.WINDOW, self.colour, (self.x, self.y), self.drawr)
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed
        else:
            pygame.draw.circle(G.WINDOW, self.colour, self.end, self.drawr)
            self._damage()
            self.done = True
            self.kill()

class ProjectileFragGrenade(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        print('grenade')
        self.theta = randint(-180, 180) # Degrees
        self.omega = randint(int(-360 * 4 / G.FPS), int(360 * 4 / G.FPS))
        self.dmg = 300 + randint(-100, 100)
        self.x, self.y = start
        self.end = end
        self.r = 2 * G.UNIT
        self.n_frag = randint(3, 8)
        self.n_spark = randint(6, 10)

        fpath = 'assets/weapons/grenade.png'
        self.max_img = pygame.transform.smoothscale(pygame.image.load(fpath).convert_alpha(), (20, 20))
        self.img = self.max_img.copy()

        self.speed = 3
        dis, self.dx, self.dy = displacement(start, end)
        self.apply_frames = ceil(dis/self.speed)

    def frame(self):
        if self.initial_delay > 0:
            self.initial_delay -= 1
            return
        self.apply_frames -= 1
        self.theta += self.omega
        # self.img = pygame.transform.rotate(self.img, self.omega) # Change
        if self.apply_frames > 0:
            G.WINDOW.blit(self.img, (self.x, self.y))
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed
        else:
            G.WINDOW.blit(self.img, self.end)
            self._r_damage()
            self.done = True
            self.kill()


class ProjectileTracking(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0,
                 target: pygame.Rect = None):
        super().__init__(start, end, initial_delay)
        self.colour = (255, 100, 100)
        self.dmg = 30
        self.drawr = 3
        self.x, self.y = start
        self.speed = 5
        self.done = False
        self.target = target
        self.end = end
        d, _, _ = displacement(start, end)
        self.max_lifetime = ceil(d/self.speed)*2
        xp, yp = rect_center(target) if self.target is not None else self.end
        self.dx, self.dy = end[0] - xp, end[1] - yp

    def frame(self):
        if self.initial_delay > 0:
            self.initial_delay -= 1
            return
        try:
            xp, yp = rect_center(self.target) if self.target is not None else self.end
        except NameError:
            self.done = True
            self.kill()
            return
        self.max_lifetime -= 1
        if self.max_lifetime <= 0:
            self.done = True
            self.kill()
            return
        dstx, dsty = xp + self.dx, yp + self.dy
        self.end = dstx, dsty
        dis, ux, uy = displacement((self.x, self.y), self.end)
        if dis <= self.speed:
            self.x, self.y = self.end
            pygame.draw.circle(G.WINDOW, self.colour, (self.x, self.y), self.drawr)
            self._damage()
            self.done = True
            self.kill()
            return
        self.x += ux * self.speed
        self.y += uy * self.speed
        pygame.draw.circle(G.WINDOW, self.colour, (self.x, self.y), self.drawr)


class ProjectileNeedler(ProjectileTracking):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0,
                 target: pygame.Rect = None):
        super().__init__(start, end, initial_delay, target)
        self.dmg = 15
        self.supercombine_dmg = 15


