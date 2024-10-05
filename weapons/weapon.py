import pygame 
import numpy as np
from typing import Tuple

import G
from sprite.firing_effect import FiringEffect

class Weapon: # Placeholder MA5B
    def __init__(self):
        self.mag_cap = 60 # Maximum magazine capacity
        self.firerate = 20 # Rounds per second
        self.spread = 1 # Character radius units
        self.damage = 10 # Damage
        self.AP_multiplier = 0.2 # Damage vs. armour
        self.error = 1 # Error angle in degrees

    def shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        # Fires a single shot
        eff = FiringEffect(start, end)
        G.FIRING_EFFECTS.add(eff)