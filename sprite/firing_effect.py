import pygame 
import numpy as np
import G
from typing import Tuple

class FiringEffect(pygame.sprite.Sprite):
    def __init__(self, start: Tuple[float, float], end: Tuple[float, float], cnt_frame: int=0):
        super().__init__()
        self.start = start
        self.end = end
        self.cnt_frames = cnt_frame

        self.colour = (255, 234, 0)
        self.width = 1
        self.dmg = 1
        self.done = False

    def frame(self):
        if self.cnt_frames <= 0:
            self.apply()
        self.cnt_frames -= 1
        if self.cnt_frames <= -2:
            self.kill()

    def apply(self):
        pygame.draw.line(G.WINDOW, self.colour, self.start, self.end, self.width)
        self.damage()
        self.done = True

    def damage(self):
        for c in G.CHARACTERS:
            if 'hit' in c.__dict__:
                c.hit(self.end[0], self.end[1], self.dmg)
