import pygame
import numpy as np
from random import randint, random

import G
from weapons.weapon import *
from weapons.spotter import Spotter
from sprite.character import Character
from utils import rect_center, theta

class WeaponManager:
    # Handles firing weapons and spotting
    def __init__(self, attached: Character, weapon: Weapon, grenade: WeapFragGrenade = None):
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

        self.grenade = grenade
        self.grenade_prob = 0.2 / G.FPS # probability every second of throwing

    def frame(self):
        self.current_target = self.spotter.frame()
        if self.current_target:
            self.firing_pos = rect_center(self.current_target.rect)

            if self.grenade and random() <= self.grenade_prob and distance(self.firing_pos,
                (self.attached.x, self.attached.y)) > self.grenade.safe_d:
                self.grenade.frame((self.attached.x, self.attached.y), self.firing_pos)

            self.acquisition_timer -= 1
            if self.acquisition_timer <= 0 and self.cooldown_timer <= 0 and not self.weapon.firing:
                self.attached.set_theta(theta((self.attached.x, self.attached.y), self.firing_pos))
                self.weapon.start_burst(self.current_target.rect)
                self.cooldown_timer = randint(*self.cooldown_time)
        else:
            self.acquisition_timer = randint(*self.acquisition_time)

        self.weapon.frame(self.attached.get_firing_pos(), self.firing_pos)
        self.firing = self.weapon.firing
        if not self.firing:
            self.cooldown_timer -= 1

    def force_stop(self):
        self.weapon.stop_burst()
        self.firing = self.weapon.firing

class SuppresiveWeaponManager(WeaponManager):
    def __init__(self, attached: Character, weapon: Weapon, grenade: WeapFragGrenade = None):
        super().__init__(attached, weapon, grenade)
        self.sample_error = self.weapon.sample_error

    def frame(self):
        self.current_target = self.spotter.frame()
        if self.current_target:
            self.firing_pos = rect_center(self.current_target.rect)

            if self.grenade and random() <= self.grenade_prob and distance(self.firing_pos,
                (self.attached.x, self.attached.y)) > self.grenade.safe_d:
                self.grenade.frame((self.attached.x, self.attached.y), self.firing_pos)

            self.acquisition_timer -= 1
            if self.acquisition_timer <= 0 and self.cooldown_timer <= 0 and not self.weapon.firing:
                self.attached.set_theta(theta((self.attached.x, self.attached.y), self.firing_pos))
                self.weapon.start_burst(self.current_target.rect)
                self.cooldown_timer = randint(*self.cooldown_time)
        else:
            self.acquisition_timer = randint(*self.acquisition_time)

        self.weapon.frame(self.attached.get_firing_pos(), self.firing_pos)
        self.firing = self.weapon.firing
        if not self.firing:
            self.cooldown_timer -= 1
