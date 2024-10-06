import pygame
import numpy as numpy
from random import random
from typing import Union

import G
from sprite.character import Character
from utils import distance

class SpottingSystem:
    def __init__(self):
        pass

    def get_target(self, actor: Character) -> Union[None, Character]:
        # Closest
        dis = numpy.inf
        res = None
        for other in filter(lambda o: self._valid_target(actor, o), G.CHARS_ALL):
            d = distance((actor.x, actor.y), (other.x, other.y))
            if d < dis:
                dis = d
                res = other
        return res

    def _valid_target(self, actor: Character, other: Character) -> bool:
        return (actor.faction != other.faction and random() < other.spotted_chance and
            distance((actor.x, actor.y), (other.x, other.y)) <= actor.spotting_range)