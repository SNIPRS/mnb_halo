import pygame
import numpy as np
from random import randint, choice

import G
from weapons.weapon import *
from weapons.weapon_manager import WeaponManager
from sprite.character import Character, Enemy
from utils import center_rect, distance, rect_center

class CharacterAI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.char = Character((100, 100, 100), G.SPRITE_SIZE, G.SPRITE_SIZE)
        G.CHARS_ALL.add(self.char)
        self.weapon = Weapon()
        self.grenade = None
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
        self.char = Character((100, 100, 100), G.SPRITE_SIZE, G.SPRITE_SIZE)
        self.char.x, self.char.y = 300, 800
        self.char.dstx, self.char.dsty = 300, 800
        G.CHARS_ALL.add(self.char)
        self.weapon = WeapMagnum() # WeapAssaultRifle()
        self.grenade = WeapFragGrenade()
        self.weapon_manager = WeaponManager(self.char, self.weapon, self.grenade)

    def _update_desination(self):
        for event in G.EVENTS:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self.char.selected and self.char.rect.collidepoint(event.pos):
                    # closest selected character
                    d = distance(event.pos, rect_center(self.char.rect))
                    for c in filter(lambda c: c.faction == G.PLAYER_FAC, G.CHARS_ALL):
                        if distance(event.pos, rect_center(c.rect)) < d:
                            return
                    self.char.selected = True
                elif self.char.selected:
                    self.char.selected = False
                    self.char.dstx, self.char.dsty = center_rect(self.char.rect, event.pos[0], event.pos[1])

    def can_kill(self):
        return self.char.health < 0


class EnemyCharacterAI(CharacterAI):
    def __init__(self):
        super(CharacterAI, self).__init__()
        self.char = Enemy((200, 100, 100, 100), G.SPRITE_SIZE, G.SPRITE_SIZE)
        self.char.x, self.char.y = randint(0, G.WIDTH - self.char.rect.width), - self.char.rect.height - 10
        self.char.dstx = self.char.x
        self.char.dsty = G.HEIGHT + 100
        G.CHARS_ALL.add(self.char)
        self.weapon = choice((WeapNeedler(), WeapPlasmaRifle(), WeapPlasmaPistol()))
        self.weapon_manager = WeaponManager(self.char, self.weapon)

    def _update_desination(self):
        pass

    def can_kill(self):
        return self.char.health <= 0 or self.char.y > G.HEIGHT + 10

class GruntHeavyCharacterAI(CharacterAI):
    def __init__(self):
        super(CharacterAI, self).__init__()
        self.char = Enemy((100, 255, 100), G.SPRITE_SIZE, G.SPRITE_SIZE)
        self.char.x, self.char.y = randint(0, G.WIDTH - self.char.rect.width), - self.char.rect.height - 10
        self.char.dstx = self.char.x
        self.char.dsty = randint(50, 200)
        self.dy = randint(100, 200)
        self.stay_time = (40 * G.FPS, 60 * G.FPS)
        self.stay_timer = randint(*self.stay_time)
        G.CHARS_ALL.add(self.char)
        self.weapon = WeapPlasmaCannon()
        self.weapon_manager = WeaponManager(self.char, self.weapon)

        self.defend_time = 15 * G.FPS


    def frame(self):
        self._update_desination()
        self.char.frame()
        if self.char.pinned() or self.char.health <= 0:
            return
        if not self.char.move():
            if self.stay_timer <= 0:
                self.char.dsty += randint(*self.dy)
                self.stay_timer = randint(*self.stay_time)
                self.weapon.stop_burst()
                return
            self.stay_timer -= 1
            self.weapon_manager.frame()

    def can_kill(self):
        return self.char.health <= 0 or self.char.y > G.HEIGHT + 10
