import pygame 
import numpy as np
import G

class FiringEffect:
    def __init__(self, x, y, xp, yp):
        self.x = x
        self.y = y
        self.xp = xp
        self.yp = yp

class DamageEffect:
    def __init__(self, x, y, dmg):
        self.x = x
        self.y = y
        self.dmg = dmg

    def apply(self):
        for c in G.CHARACTERS:
            if 'hit' in c.__dict__:
                c.hit(self.x, self.y, self.dmg)