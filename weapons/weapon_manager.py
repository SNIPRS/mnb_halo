import pygame
import numpy as np
from random import randint

import G
from weapons.weapon import Weapon
from weapons.spotter import Spotter
from sprite.character import Character
from utils import rect_center

class WeaponManager:
    # Handles firing weapons and spotting
    def __init__(self, attached: Character, weapon: Weapon):
        self.attached = attached
        self.spotter = Spotter(attached)
        self.weapon = weapon
        self.acquisition_time = [0*G.FPS, 2*G.FPS] # Time to start firing on a new target
        self.cooldown_time = weapon.cooldown # Minimum time to wait after firing

        self.firing = False
        self.current_target = None
        self.acquisition_timer = randint(*self.acquisition_time)
        self.cooldown_timer = 0
        self.firing_pos = None

    def frame(self):
        self.current_target = self.spotter.frame()
        if self.current_target:
            self.firing_pos = rect_center(self.current_target.rect)
            self.acquisition_timer -= 1
            if self.acquisition_timer <= 0 and self.cooldown_timer <= 0 and not self.weapon.firing:
                self.weapon.start_burst()
                self.cooldown_timer = randint(*self.cooldown_time)
        else:
            self.acquisition_timer = randint(*self.acquisition_time)

        self.weapon.frame(rect_center(self.attached.rect), self.firing_pos)
        self.firing = self.weapon.firing
        if not self.firing:
            self.cooldown_timer -= 1