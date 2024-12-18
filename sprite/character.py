import pygame
import numpy as np
from typing import Optional, Tuple

import G
from utils import displacement, displacement_theta, center_rect, rect_center, distance

class Character(pygame.sprite.Sprite):
    def __init__(self, colour, width: float, height: float):
        super().__init__()

        # Body
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.x, self.rect.y
        self.dstx, self.dsty = self.rect.x, self.rect.y
        self.hitbox_radius = (self.rect.width + self.rect.height)/4
        self.selected = False
        self.theta = 0
        self.firing_dx, self.firing_dy = 0, 0

        # Usage
        self.speed = 1

        self.health = 100
        self.max_health = self.health

        self.morale = 100
        self.pin_health = self.morale / 100 * 0.5
        self.pin_health_regen = 10 / G.FPS
        self.max_pin_health = self.pin_health
        self.min_pin_health = -self.pin_health
        self.pinr_multiplier = 2
        self.pin_buffer = G.FPS * 2
        self.max_pin_buffer = self.pin_buffer

        self.supercombine_health = self.health // 2
        self.max_supercombine_health = self.supercombine_health
        self.supercombine_regen = 25 / G.FPS

        self.spotting_range = 800
        self.spotted_chance = 1
        self.faction = 0
        self.shoot_while_move = False

    def frame(self):
        if -1 <= self.pin_health < 0 and self.pin_buffer > 0:
            self.pin_buffer -= 1
            if self.pin_buffer == 0:
                self.pin_buffer = self.max_pin_buffer
                self.pin_health = 1
        else:
            self.pin_health = int(min(self.max_pin_health, self.pin_health + self.pin_health_regen))

        self.supercombine_health = min(self.max_supercombine_health, self.supercombine_health +
                                       self.supercombine_regen)
        self.draw()

    def hit(self, origin: Tuple[float, float], dmg: float, r: float=0):
        # Check if character has been hit
        mag, _, _,  = displacement((self.x, self.y), origin)
        if mag <= self.hitbox_radius:
            self.health -= dmg
            self.pin_health = max(min(self.pin_health - dmg, 0), self.min_pin_health)
            print(self.health)
        elif mag <= self.hitbox_radius * self.pinr_multiplier:
            self.pin_health = max(self.pin_health - dmg, self.min_pin_health)

    def move(self, move: Optional[bool]=True) -> bool:
        # Moves a single step towards destination
        dis, dx, dy, self.theta = displacement_theta((self.x, self.y), (self.dstx, self.dsty))
        if dis <= G.MOVE_THRESHOLD:
            return False
        if move:
            self.x += dx * self.speed
            self.y += dy * self.speed
            return True
        return False


    def draw(self):
        self.rect.x, self.rect.y = int(self.x), int(self.y)
        G.WINDOW.blit(self.image,(self.rect.x, self.rect.y))

    def pinned(self):
        return self.pin_health < 0

    def __bool__(self):
        return True

    def set_theta(self, theta: float):
        self.theta = theta

    def get_firing_pos(self) -> Tuple[int, int]:
        mid = rect_center(self.rect)
        return (int(mid[0] + self.firing_dx), int(mid[1] + self.firing_dy))


class Enemy(Character):
    def __init__(self, colour, width: float, height: float):
        super().__init__(colour=colour, width=width, height=height)
        self.faction = 1
        self.speed = 0.3
        self.spotted_chance = 1
        

class CharacterGroup(pygame.sprite.Group):
    def hit(self):
        for s in self.__iter__():
            pass
