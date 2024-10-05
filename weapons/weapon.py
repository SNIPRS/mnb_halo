import pygame 
import numpy as np
from typing import Tuple, Optional
from random import randint, random, uniform

import G
from sprite.firing_effect import FiringEffect

class Weapon: # Placeholder MA5B
    def __init__(self):
        # Constants
        self.mag_cap = 60 # Maximum magazine capacity
        self.firerate = 20 # Rounds per second
        self.spread = 1 # Character radius units
        self.damage = 10 # Damage
        self.AP_multiplier = 0.2 # Damage vs. armour
        self.error = 1 # Error angle in degrees
        self.aim_time = 1 # Seconds, takes this long to aim before firing
        self.reload_time = (4, 5) # Seconds: min, max
        self.burst_range = (2, 15) # min, max
        self.subburst_probability = 0.1
        self.subburst_delay = (0.1, 1) # Seconds: min, max
        self.error_multiplier = 1.1 # Multiplier per sustained shot

        # State variables
        self.mag = self.mag_cap
        self.firing_timer = self.aim_time*G.FPS
        self.reload_timer = 0
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        if self.firing:
            if self.firing_timer <= 0 and self.burst > 0 and end is not None and start is not None:
                self._shot(start, end)
                self.burst -= 1
                self.mag -= 1
                self.firing_timer = G.FPS//self.firerate if random() >= self.subburst_probability \
                    else G.FPS//self.firerate + int(uniform(*self.subburst_delay)*G.FPS)
            if self.mag <= 0:
                self.firing = False
                self.reload_timer = int(uniform(*self.reload_time)*G.FPS)
                return
            else: # if self.burst <= 0:
                self.firing = False
                self._reset_burst()

        else:
            self.reload_timer = max(0, self.reload_timer-1)
            if self.reload_timer <= 0:
                self.mag = self.mag_cap

    def _shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        # Fires a single shot
        eff = FiringEffect(start, end)
        G.FIRING_EFFECTS.add(eff)

    def _reset_burst(self):
        self.firing_timer = self.aim_time*G.FPS
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))
