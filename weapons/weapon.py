import pygame 
import numpy as np
from typing import Tuple, Optional
from random import randint, random, uniform
from math import sin, cos, tan

import G
from utils import displacement
from weapons.weapon_stats import *
from sprite.firing_effect import *


class Weapon:
    def __init__(self):
        self.firing = False
        self.cooldown = [1, 1]

    def start_burst(self):
        pass

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        pass

class AssaultRifle(Weapon): # Placeholder MA5B
    def __init__(self, params: Optional[dict] = None):
        if params is not None:
            self.init_params(params)
            return
        # Constants
        self.mag_cap = 60
        self.firerate = G.FPS // 20
        self.error = 5
        self.aim_time = 1 * G.FPS
        self.reload_time = [int(5*G.FPS), int(7*G.FPS)]
        self.burst_range = (4, 16)
        self.subburst_probability = 0.05
        self.subburst_delay = [int(0.2*G.FPS), int(0.5*G.FPS)]
        self.spread_heat = 1
        self.cooldown = [int(3*G.FPS), int(6*G.FPS)]
        self.projectile = BulletEffect

        self.fire_sound = pygame.mixer.Sound("./assets/sounds/ar_fire.wav")
        self.reload_sound = pygame.mixer.Sound("./assets/sounds/ar_reload.wav")

        # State variables
        self.spread = self.error
        self.mag = self.mag_cap
        self.firing_timer = self.aim_time
        self.reload_timer = 0
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))
        self.spread = self.error

    def init_params(self, params: dict): # Reinit after increasing skill
        self.mag_cap = params['mag_cap']
        self.firerate = G.FPS // params['firerate']
        self.error = params['error']
        self.aim_time = params['aim_time'] * G.FPS
        self.reload_time = [int(params['reload_time'][0]*G.FPS), int(params['reload_time'][1]*G.FPS)]
        self.burst_range = (params['burst_range'][0], params['burst_range'][1])
        self.subburst_probability = params['subburst_probability']
        self.subburst_delay = [int(params['subburst_delay'][0]*G.FPS), int(params['subburst_delay'][1]*G.FPS)]
        self.spread_heat = params['spread_heat']
        self.cooldown = [int(params['cooldown'][0]*G.FPS), int(params['cooldown'][1]*G.FPS)]
        self.projectile = params['projectile']

        self.fire_sound = params['sound_fire']
        self.reload_sound = params['sound_reload']

        # State variables
        self.spread = self.error
        self.mag = self.mag_cap
        self.firing_timer = self.aim_time
        self.reload_timer = 0
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))
        self.spread = self.error

    def start_burst(self):
        if not self.firing and self.mag > 0:
            self._reset_burst()
            self.firing = True

    def stop_burst(self):
        self.firing = False
        self._reset_burst()

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        if self.firing:
            if self.firing_timer <= 0 and self.burst > 0 and start is not None and end is not None:
                target = self._target_point(start, end)
                self._shot(start, target)
                self.burst -= 1
                self.mag -= 1
                subburst = random() <= self.subburst_probability
                self.firing_timer = self.firerate + randint(*self.subburst_delay) if subburst \
                    else self.firerate
                self.spread = self.error if subburst else self.spread + self.spread_heat
            if self.mag <= 0:
                self.firing = False
                self.reload_timer = randint(*self.reload_time)
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
        G.PLAY_SOUND(self.fire_sound)
        eff = self.projectile(start, end)
        G.FIRING_EFFECTS.add(eff)

    def _reload(self):
        if self.mag != self.mag_cap:
            G.PLAY_SOUND(self.reload_sound)
        self.mag = self.mag_cap

    def _reset_burst(self):
        self.firing_timer = self.aim_time
        self.burst = min(self.mag, randint(*self.burst_range))


class PlasmaRifle(AssaultRifle):
    def __init__(self):
        super().__init__()
        # Constants
