import pygame
import numpy as np
from typing import Optional, Tuple, Union

import G

class Animation:
    def __init__(self, pos: Tuple[float, float]):
        self.pos = pos

class CharacterAnimation:
    def __init__(self, pos: Tuple[float, float], theta: float):
        self.pos = pos
        self.theta = theta # Degrees
        self.state = 0
        self.anim_states = {
            'IDLE': 0,
            'MOVE': 1,
            'AIM': 2,
            'PIN': 3,
            'DEAD': 4,
            'MELEE': 5,
        }
        self.missing_txtr = pygame.Surface([G.SPRITE_SIZE, G.SPRITE_SIZE])
        self.missing_txtr.fill('purple')
        self.textures = {a : self.missing_txtr for a in range(len(self.anim_states))}
        self.txtr = self.textures[self.state]

    def frame(self, pos: Tuple[float, float] = None, theta: float = None, state: Union[str, int] = None):
        if pos is not None:
            self.pos = pos
        if theta is not None:
            self.txtr = pygame.transform.rotate(self.txtr, -self.theta + theta)
            self.theta = theta
        if state is not None:
            self.state = state if isinstance(state, int) else self.anim_states.get(state, 0)
            self.txtr = pygame.transform.rotate(self.textures[self.state], self.theta)

        G.WINDOW.blit(self.txtr, self.pos)

        





