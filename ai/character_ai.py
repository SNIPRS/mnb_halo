import pygame
import numpy as np

import G
from weapons.weapon import Weapon
from weapons.weapon_manager import WeaponManager
from sprite.character import Character
from utils import center_rect

class CharacterAI:
    def __init__(self):
        self.character = Character((100, 100, 100), 20, 20)
        self.weapon = Weapon()
        self.weapon_manager = WeaponManager(self.character, self.weapon)

    def frame(self):
        self.character.frame()
        self.weapon_manager.frame()

class ControllableCharacterAI(CharacterAI):
    def __init__(self):
        super.__init__()

    def update_pos(self):
        for event in G.EVENTS:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.character.selected and self.character.rect.collidepoint(event.pos):
                    self.character.selected = True
                elif self.character.selected:
                    self.character.selected = False
                    self.character.dstx, self.character.dsty = center_rect(self.rect, event.pos[0], event.pos[1])

    def frame(self):
        self.update_pos()
        self.character.frame()
        self.weapon_manager.frame()
