import pygame 
import numpy as np
from math import ceil
from typing import Tuple, Optional

import G
from utils import displacement

class Effect(pygame.sprite.Sprite):
    def __init__(self, start: Tuple[float, float], end: Optional[Tuple[float, float]] = None,
                 initial_delay: Optional[int] = 0):
        super().__init__()
        self.start = start
        self.end = end
        self.initial_delay = initial_delay
        self.dmg = 0

    def frame(self):
        if self.initial_delay <= 0:
            self.apply()
        self.initial_delay -= 1
        if self.initial_delay <= -2:
            self.kill()

    def _damage(self):
        for c in G.CHARS_ALL:
            c.hit(self.end, self.dmg)


class BulletEffect(Effect):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)

        self.colour = (255, 234, 0)
        self.width = 1
        self.dmg = 10
        self.done = False

    def apply(self):
        pygame.draw.line(G.WINDOW, self.colour, self.start, self.end, self.width)
        self._damage()
        self.done = True
                
class ProjectileEffect(Effect):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], initial_delay: int=0):
        super().__init__(start, end, initial_delay)
        self.colour = (100, 100, 255)
        self.dmg = 30
        self.drawr = 3
        self.x = start[0]
        self.y = start[1]
        self.speed = 5
        self.done = False
        dis, dx, dy = displacement(start, end)
        self.apply_frames = ceil(dis/self.speed)
        self.dx = dx 
        self.dy = dy

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
