import pygame 
import numpy as np
from math import ceil
from typing import Tuple, Optional
from random import randint, choice

import G
from sprite.decal import *
from utils import displacement, rect_center, distance, random_sample_circle

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start: Tuple[float, float], end: Optional[Tuple[float, float]] = None,
                 initial_delay: Optional[int] = 0):
        super().__init__()
        self.start = start
        self.end = end
        self.initial_delay = initial_delay
        self.dmg = 0
        self.r = 1
        self.impact_type = None

    def frame(self):
        if self.initial_delay <= 0:
            self.apply()
        self.initial_delay -= 1
        if self.initial_delay <= -2:
            self.kill()

    def apply(self):
        self._apply_impact()
        self._damage()
        self.done = True
        self.kill()

    def _damage(self):
        for c in G.CHARS_ALL:
            c.hit(self.end, self.dmg)

    def _r_damage(self):
        for c in G.CHARS_ALL:
            d = distance((c.x, c.y), self.end)
            if d < self.r:
                c.hit((c.x, c.y), int(self.dmg*(1-d/(self.r+1))))

    def _apply_impact(self):
        if self.impact_type is None:
            return
        if self.impact_type == 'bullet':
            _, dx, dy = displacement(self.start, self.end)
            impact = BulletImpact(self.end, (dx, dy))
            G.DECALS.add(impact)
        elif self.impact_type == 'explosion':
            impact = Explosion(self.end)
            G.DECALS.add(impact)
        if self.impact_type == 'mini_burn':
            impact = SimpleBurn(self.end, size='mini')
            G.DECALS.add(impact)
        if self.impact_type == 'micro_burn':
            impact = SimpleBurn(self.end, size='micro')
            G.DECALS.add(impact)

class ProjectileBullet(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)

        self.colour = (255, 234, 0)
        self.width = 1
        self.dmg = 20
        self.done = False
        self.impact_type = 'bullet'

    def apply(self):
        pygame.draw.line(G.WINDOW, (255, 255, 255), self.start, self.end, 2)
        pygame.draw.line(G.WINDOW, self.colour, self.start, self.end, self.width)
        self._apply_impact()
        self._damage()
        self.done = True

class ProjectileShotgun(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        self.dmg = 25
        self.done = False
        self.impact_type = 'mini_burn'

    def apply(self):
        self._apply_impact()
        self._damage()
        self.done = True

class ProjectileShotgunShell(ProjectileBullet):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        self.colour = (255, 234, 0)
        self.width = 1
        self.dmg = 20
        self.impact_type = 'bullet'

class ProjectileBolt(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        self.colour = (100, 100, 255)
        self.dmg = 20
        self.drawr = 3
        self.x, self.y = start
        self.speed = 10
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
            self._apply_impact()
            self._damage()
            self.done = True
            self.kill()

class ProjectilePlasmaRifle(ProjectileBolt):
    def __init__(self, start, end, initial_delay = 0):
        super().__init__(start, end, initial_delay)


class ProjectileSpark(ProjectileBolt):
    def __init__(self, start, end = None, initial_delay = 0):
        super().__init__(start, end, initial_delay)
        self.dmg = 0
        self.colour = (200, 200, 100)
        self.drawr = 1
        self.speed = randint(5, 20)
        dis, self.dx, self.dy = displacement(start, end)
        self.apply_frames = ceil(dis/self.speed)

class ProjectileShrapnel(ProjectileSpark):
    def __init__(self, start, end = None, initial_delay = 0):
        super().__init__(start, end, initial_delay)
        self.dmg = randint(5, 25)
        self.colour = (200, 200, 100)
        self.impact_type = 'micro_burn'

class ProjectileFragGrenade(Projectile):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        print('grenade')
        self.theta = randint(-180, 180) # Degrees
        self.omega = randint(2, 6) * choice([-1, 1]) * 360/G.FPS
        self.dmg = 200 + randint(-25, 100)
        self.x, self.y = start
        self.impact_type = 'explosion'
        self.end = end
        self.r = 5 * G.UNIT
        self.fragr = 1.3 * self.r
        self.n_frag = randint(5, 8)
        self.n_spark = randint(5, 10)

        fpath = 'assets/weapons/grenade.png'
        self.max_size = 20
        self.max_img = pygame.transform.smoothscale(pygame.image.load(fpath).convert_alpha(),
                                                    (self.max_size , self.max_size))
        self.img = self.max_img.copy()

        self.speed = 6
        dis, self.dx, self.dy = displacement(start, end)
        self.apply_frames = dis//self.speed

        # Scale factor polynomial
        m = 0.3
        self.a, self.b, self.c = 4*(m-1)/self.apply_frames**2, (4-4*m)/self.apply_frames, m

    def frame(self):
        if self.initial_delay > 0:
            self.initial_delay -= 1
            return
        self.apply_frames -= 1
        self.theta += self.omega
        fac = self.a*self.apply_frames**2 + self.b*self.apply_frames + self.c
        self.img = pygame.transform.scale_by(pygame.transform.rotate(self.max_img, int(self.theta)), fac) # Change
        if self.apply_frames > 0:
            G.WINDOW.blit(self.img, (self.x, self.y))
            self.x += self.dx * self.speed
            self.y += self.dy * self.speed
        else:
            G.WINDOW.blit(self.img, self.end)
            self._r_damage()
            self._apply_impact()
            self._create_fragments()
            self.done = True
            self.kill()

    def _create_fragments(self):
        for _ in range(self.n_frag):
            dst = random_sample_circle(self.end, self.fragr)
            proj = ProjectileShrapnel(self.end, dst)
            G.FIRING_EFFECTS.add(proj)
        for _ in range(self.n_spark):
            dst = random_sample_circle(self.end, self.fragr)
            proj = ProjectileSpark(self.end, dst)
            G.FIRING_EFFECTS.add(proj)


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
            self._apply_impact()
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
        self.drawr = 1.5
        self.colour = (255, 50, 100)
        self.tail_len = 3
        self.tail_colour = (255, 150, 200)
        self.dmg = 15
        self.supercombine_dmg = 15

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
            # Apply impact
            circle_params = (self.colour, (self.x, self.y), self.drawr)
            line_params = (self.tail_colour, (self.x, self.y),
                         (self.x - ux*self.tail_len, self.y - uy*self.tail_len))
            impact = NeedlerImpact(self.end, circle_params=circle_params, line_params=line_params)
            G.DECALS.add(impact)
            self.done = True
            self.kill()
            return
        self.x += ux * self.speed
        self.y += uy * self.speed
        pygame.draw.circle(G.WINDOW, self.colour, (self.x, self.y), self.drawr)
        pygame.draw.line(G.WINDOW, self.tail_colour, (self.x, self.y),
                         (self.x - ux*self.tail_len, self.y - uy*self.tail_len))



