import pygame 
import numpy as np
from typing import Tuple, Optional
from random import randint, random, uniform
from math import sin, cos, tan

import G
from utils import displacement
from weapons.weapon_stats import *
from sprite.projectile import *
from sprite.decal import DecalBulletCasing

class Weapon:
    def __init__(self):
        self.firing = False
        self.cooldown = [1, 1]
        self.target_rect = None
        self.error = 0

    def start_burst(self):
        pass

    def stop_burst(self):
        pass

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        pass

    def _target_point(self, start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float]:
        dis, _, _ = displacement(start, end)
        # Not a uniform sampler!
        r = dis * tan(G.DEGREE_TO_RAD * self.error) * random()
        theta = random() * 2 * G.PI
        return end[0] + r*cos(theta), end[1] + r*sin(theta)

    def __bool__(self) -> bool:
        return True

class WeapAssaultRifle(Weapon): # Placeholder MA5B
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
        self.projectile = ProjectileBullet

        self.sound_fire = pygame.mixer.Sound("./assets/sounds/ar_fire.wav")
        self.sound_reload = pygame.mixer.Sound("./assets/sounds/ar_reload.wav")

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

        self.sound_fire = params['sound_fire']
        self.sound_reload = params['sound_reload']

        # State variables
        self.spread = self.error
        self.mag = self.mag_cap
        self.firing_timer = self.aim_time
        self.reload_timer = 0
        self.firing = False
        self.burst = min(self.mag, randint(*self.burst_range))
        self.spread = self.error

    def start_burst(self, target: pygame.Rect = None): # target for tracking weapons
        if not self.firing and self.mag > 0:
            self._reset_burst()
            self.firing = True
            self.target_rect = target

    def stop_burst(self):
        self.firing = False
        self.target_rect = None
        self._reset_burst()

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        if self.firing:
            if self.firing_timer <= 0 and self.burst > 0 and start is not None and end is not None:
                self._shot(start, end)
                self.burst -= 1
                self.mag -= 1
                subburst = random() < self.subburst_probability
                self.firing_timer = self.firerate + randint(*self.subburst_delay) if subburst \
                    else self.firerate
                self.spread = self.error if subburst else self.spread + self.spread_heat
            if self.mag <= 0:
                self.firing = False
                self.reload_timer = randint(*self.reload_time)
                G.PLAY_SOUND(self.sound_reload)
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
 
    def _shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        end = self._target_point(start, end)
        G.PLAY_SOUND(self.sound_fire)
        proj = self.projectile(start, end)
        _, dx, dy = displacement(start, end)
        casing = DecalBulletCasing(start, (dx, dy))
        G.FIRING_EFFECTS.add(proj)
        G.DECALS.add(casing)

    def _reload(self):
        self.mag = self.mag_cap

    def _reset_burst(self):
        self.firing_timer = self.aim_time
        self.target_rect = None
        self.burst = min(self.mag, randint(*self.burst_range))

class WeapBattleRifle(WeapAssaultRifle):
    def __init__(self, params: Optional[dict] = WEAPON_BATTLE_RIFLE):
        super().__init__(params)
        self.burst_size = params['burst_size']
        self.burst_rof = G.FPS // params['burst_rof']
        self.burst_heat = params['burst_heat']

    def _shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        G.PLAY_SOUND(self.sound_fire) # 3 rounds
        for i in range(self.burst_size):
            end = self._target_point(start, end)
            proj = self.projectile(start, end, initial_delay=i*self.burst_rof)
            _, dx, dy = displacement(start, end)
            casing = DecalBulletCasing(start, (dx, dy), initial_delay=i*self.burst_rof)
            G.FIRING_EFFECTS.add(proj)
            G.DECALS.add(casing)
            self.spread += self.burst_heat
        self.spread = self.error


class WeapShotgun(WeapAssaultRifle):
    def __init__(self, params: Optional[dict] = WEAPON_SHOTGUN):
        super().__init__(params)
        # Sound reload is actually the pumping sound
        self.sound_pump = params['sound_pump']
        self.sound_open = params['sound_open']
        self.sound_close = params['sound_close']
        self.sound_reload = params['sound_full_reload']
        self.pellets = params['pellets']

    def _shot(self, start, end):
        G.PLAY_SOUND(self.sound_fire)
        for _ in range(self.pellets):
            tend = self._target_point(start, end)
            proj = self.projectile(start, tend)
            _, dx, dy = displacement(start, tend)
            G.FIRING_EFFECTS.add(proj)
        casing = DecalShotgunCasing(start, (dx, dy))
        G.DECALS.add(casing)
        if self.mag > 0:
            G.PLAY_SOUND(self.sound_pump)

    def _reload(self):
        pass

class WeapPlasmaRifle(WeapAssaultRifle):
    def __init__(self):
        super().__init__(WEAPON_PLASMA_RIFLE)
        # HaloR Plasma Repeater
        self.firerate_decay = WEAPON_PLASMA_RIFLE['firerate_decay']
        self.firerate_orig = self.firerate

    def _reset_burst(self):
        super()._reset_burst()
        self.firerate = self.firerate_orig

    def _shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        end = self._target_point(start, end)
        G.PLAY_SOUND(self.sound_fire)
        proj = self.projectile(start, end)
        G.FIRING_EFFECTS.add(proj)
        self.firerate = int(min(self.firerate_orig * 2, self.firerate * self.firerate_decay))

class WeapNeedler(WeapAssaultRifle):
    def __init__(self):
        super().__init__(WEAPON_NEEDLER)

    def _shot(self, start: Tuple[float, float], end: Tuple[float, float]):
        end = self._target_point(start, end)
        G.PLAY_SOUND(self.sound_fire)
        proj = ProjectileNeedler(start, end, target=self.target_rect)
        G.FIRING_EFFECTS.add(proj)


class WeapFragGrenade(Weapon):
    def __init__(self):
        super().__init__()
        self.sound = G.SOUNDS['grenade_throw']
        self.error = 12
        self.safe_d = G.UNIT * 8

    def frame(self, start: Optional[Tuple[float, float]] = None, end: Optional[Tuple[float, float]] = None):
        # Give a start and end when you want to fire a grenade
        if start is not None and end is not None:
            target = self._target_point(start, end)
            G.PLAY_SOUND(self.sound)
            proj = ProjectileFragGrenade(start, target, initial_delay = randint(0, G.FPS))
            G.FIRING_EFFECTS.add(proj)
