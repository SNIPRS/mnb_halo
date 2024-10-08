import pygame 
import numpy as np
from random import random
from typing import Tuple, Optional

import G
from utils import displacement, rect_center

class Decal(pygame.sprite.Sprite):
    def __init__(self, start: Tuple[float, float], duration: Optional[int] = 1 * G.FPS):
        super().__init__()
        self.start = start
        self.duration = duration

    def frame(self):
        self.duration -= 1
        if self.duration < 0:
            self.kill()

class DecalBulletCasing(Decal):
    def __init__(self, start: Tuple[float, float], direction: Tuple[float, float], duration: int = 7*G.FPS,
                 flight_duration: int = 1*G.FPS, speed: float = 3, omega: float = 6, r: int = 2,
                 spread: float = 0.5, colour: Tuple[int, int, int] = ((150, 100, 0)),
                 thickness: int = 1): # Everything in radians
        super().__init__(start, duration)
        self.start = start
        alpha = np.arctan2(direction[1], direction[0]) + G.PI/2 + (random() - 0.5)*spread
        self.direction = (np.cos(alpha), np.sin(alpha))
        self.duration = duration
        self.flight_duration = max(30, int(flight_duration * random()))
        self.speed = max(1, speed * random())
        self.r = r
        self.omega = omega * random()
        self.colour = colour
        self.thickness = thickness
        self.fade_duration = 6 * G.FPS
        self.fade_step = 255//self.fade_duration

        self.theta = alpha + G.PI/2
        self.x, self.y = start
    
    def _draw(self):
        c, s = np.cos(self.theta) * self.r, np.sin(self.theta) * self.r
        start = (self.x + c, self.y + s)
        end = (self.x - c, self.y - s)
        # if self.duration < self.fade_duration:
        #     colour = self.colour + (255 - self.fade_step,)
        # else:
        #     colour = self.colour
        colour = self.colour # Alpha not used yet
        pygame.draw.line(G.WINDOW, colour, start, end, self.thickness)

    def frame(self):
        self.duration -= 1
        self.flight_duration -= 1
        if self.flight_duration > 0:
            self.x += self.speed * self.direction[0]
            self.y += self.speed * self.direction[1]
            self.theta += self.omega
        if self.duration > 0:
            self._draw()
        else:
            self.kill()

        

        
        