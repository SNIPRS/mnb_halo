import pygame 
import numpy as np

import G

class DamageEffect:
    def __init__(self, dmg=0):
        self.dmg = 0

    def apply(self):
        return self.dmg
