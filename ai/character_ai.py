import pygame
import numpy as np
from random import randint

import G
from weapons.weapon import Weapon, AssaultRifle, PlasmaRifle
from weapons.weapon_manager import WeaponManager
from sprite.character import Character, Enemy
from utils import center_rect

class CharacterAI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.char = Character((100, 100, 100), 20, 20)
        G.CHARS_ALL.add(self.char)
        self.weapon = Weapon()
        self.weapon_manager = WeaponManager(self.char, self.weapon)

    def frame(self):
        self._update_desination()
        self.char.frame()
        if self.char.pinned() or self.char.health <= 0:
            return
        elif not self.weapon_manager.firing or self.char.shoot_while_move:
            self.char.move()
        self.weapon_manager.frame()

    def _update_desination(self):
        pass

    def can_kill(self):
        return False

    def kill(self):
        self.char.kill()
        super().kill()


class ControllableCharacterAI(CharacterAI):
    def __init__(self):
        super(CharacterAI, self).__init__()
        self.char = Character((100, 100, 100), 20, 20)
        self.char.x, self.char.y = 300, 800
        self.char.dstx, self.char.dsty = 300, 800
        G.CHARS_ALL.add(self.char)
        self.weapon = AssaultRifle()
        self.weapon_manager = WeaponManager(self.char, self.weapon)

    def _update_desination(self):
        for event in G.EVENTS:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.char.selected and self.char.rect.collidepoint(event.pos):
                    self.char.selected = True
                elif self.char.selected:
                    self.char.selected = False
                    self.char.dstx, self.char.dsty = center_rect(self.char.rect, event.pos[0], event.pos[1])

    def can_kill(self):
        return self.char.health < 0


class EnemyCharacterAI(CharacterAI):
    def __init__(self):
        super(CharacterAI, self).__init__()
        self.char = Enemy((200, 100, 100, 100), 20, 20)
        self.char.x, self.char.y = randint(0, G.WIDTH - self.char.rect.width), - self.char.rect.height - 10
        self.char.dstx = self.char.x
        self.char.dsty = G.HEIGHT + 100
        G.CHARS_ALL.add(self.char)
        self.weapon = PlasmaRifle()
        self.weapon_manager = WeaponManager(self.char, self.weapon)

    def _update_desination(self):
        pass

    def can_kill(self):
        return self.char.health <= 0 or self.char.y > G.HEIGHT + 10
