import pygame 
import numpy as np

class Weapon: # Placeholder MA5B
    def __init__(self):
        self.mag_cap = 60 # Maximum magazine capacity
        self.firerate = 20 # Rounds per second
        self.spread = 1 # Character radius units
        self.damage = 10 # Damage
        self.AP_multiplier = 0.2 # Damage vs. armour
