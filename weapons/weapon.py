import pygame 
import numpy as np
from typing import Tuple, Optional
from random import randint, random, uniform
from math import sin, cos, tan

import G
from utils import displacement
from sprite.firing_effect import BulletEffect, ProjectileEffect

class Weapon:
    def __init__(self):
        self.firing = False
        self.cooldown = [1, 1]

    def start_burst(self):
        pass

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        pass

class AssaultRifle(Weapon): # Placeholder MA5B
    def __init__(self):
        # Constants
        self.mag_cap = 60 # Maximum magazine capacity
        self.firerate = 20 # Rounds per second
        self.error = 3 # Error angle in degrees
        self.aim_time = 1 # Seconds, takes this long to aim before firing
        self.reload_time = (5, 7) # Seconds: min, max
        self.burst_range = (4, 16) # min, max
        self.subburst_probability = 0.05
        self.subburst_delay = (0.2, 2) # Seconds: min, max
        self.spread_heat = 1 # Spread increase per shot
        self.cooldown = [3*G.FPS, 6*G.FPS] # Time to wait after a burst
        self.shot_effect = BulletEffect

        self.fire_sound = pygame.mixer.Sound("./assets/sounds/ar_fire.wav")
        self.reload_sound = pygame.mixer.Sound("./assets/sounds/ar_reload.wav")

        # State variables
        self.spread = self.error
        self.mag = self.mag_cap
        self.firing_timer = self.aim_time*G.FPS
        self.reload_timer = 0
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))
        self.spread = self.error

    def start_burst(self):
        if not self.firing and self.mag > 0:
            self._reset_burst()
            self.firing = True

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        if self.firing:
            if self.firing_timer <= 0 and self.burst > 0 and start is not None and end is not None:
                target = self._target_point(start, end)
                self._shot(start, target)
                self.burst -= 1
                self.mag -= 1
                subburst = random() <= self.subburst_probability
                self.firing_timer = G.FPS//self.firerate + int(uniform(*self.subburst_delay)*G.FPS) if subburst \
                    else G.FPS//self.firerate
                self.spread = self.error if subburst else self.spread + self.spread_heat
            if self.mag <= 0:
                self.firing = False
                self.reload_timer = int(uniform(*self.reload_time)*G.FPS)
                return
            if self.burst <= 0:
                self.firing = False
                self._reset_burst()
                return
            else:
                self.firing_timer -= 1

        else:
            if self.mag <= 0:
                self.reload_timer = max(0, self.reload_timer-1)
                if self.reload_timer == 0:
                    self._reload()

    def _target_point(self, start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float]:
        dis, _, _ = displacement(start, end)
        # Not a uniform sampler!
        r = dis * tan(G.DEGREE_TO_RAD * self.error) * random()
        theta = random() * 2 * G.PI
        return end[0] + r*cos(theta), end[1] + r*sin(theta)

    def _shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        # Fires a single shot
        G.PLAY_SOUND(self.fire_sound)
        eff = self.shot_effect(start, end)
        G.FIRING_EFFECTS.add(eff)

    def _reload(self):
        if self.mag != self.mag_cap:
            G.PLAY_SOUND(self.reload_sound)
        self.mag = self.mag_cap

    def _reset_burst(self):
        self.firing_timer = self.aim_time*G.FPS
        self.burst = min(self.mag, randint(*self.burst_range))


class PlasmaRifle(AssaultRifle):
    def __init__(self):
        super().__init__()
        # Constants
        self.mag_cap = 100 # Maximum magazine capacity
        self.firerate = 8 # Rounds per second
        self.error = 3 # Error angle in degrees
        self.aim_time = 2 # Seconds, takes this long to aim before firing
        self.reload_time = (0, 1) # Seconds: min, max
        self.burst_range = (2, 8) # min, max
        self.subburst_probability = 0.25
        self.subburst_delay = (0.2, 2) # Seconds: min, max
        self.spread_heat = 1 # Spread increase per shot
        self.cooldown = [5*G.FPS, 10*G.FPS] # Time to wait after a burst
        self.shot_effect = ProjectileEffect

        self.fire_sound = pygame.mixer.Sound("./assets/sounds/ar_fire.wav")
        self.reload_sound = pygame.mixer.Sound("./assets/sounds/ar_reload.wav")

        # State variables
        self.spread = self.error
        self.mag = self.mag_cap
        self.firing_timer = self.aim_time*G.FPS
        self.reload_timer = 0
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))
        self.spread = self.error
