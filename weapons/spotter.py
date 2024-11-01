import pygame
import numpy as numpy
from random import random, randint
from typing import Union, Optional

import G
from sprite.character import Character
from utils import distance

class Spotter:
    def __init__(self, attached: Character):
        self.spotting_updates = [3*G.FPS, 5*G.FPS] # Updates every so often
        self.spotting_timer = randint(*self.spotting_updates) # Countdown
        self.current_target = None
        self.attached = attached

    def frame(self, spot: bool = False) -> Union[None, Character]:
        self.spotting_timer -= 1
        if spot:
            self.spotting_timer = 0
        if self.spotting_timer <= 0:
            self.current_target = self._get_target()
            self.spotting_timer = randint(*self.spotting_updates)
        else:
            if not self.valid_target(self.attached, self.current_target):
                self.current_target = None
        return self.current_target

    def _get_target(self, random_p: float = 0.5) -> Union[None, Character]:
        # Closest prob 1/2 random probability 1/2
        dis = numpy.inf
        res = None
        rand = None
        N = 1
        for other in filter(lambda o: self.valid_target(self.attached, o), G.CHARS_ALL):
            d = distance((self.attached.x, self.attached.y), (other.x, other.y))
            if d < dis:
                dis = d
                res = other
            if random() < 1/N:
                rand = other
            N += 1

        return res if random() <= random_p or rand is None else rand

    def valid_target(self, actor: Union[None, Character], other: Union[None, Character]) -> bool:
        if actor is None or other is None or other.health < 0:
            return False
        return (actor.faction != other.faction and random() < other.spotted_chance and
            distance((actor.x, actor.y), (other.x, other.y)) <= actor.spotting_range)