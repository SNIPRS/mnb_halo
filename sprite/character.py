import pygame
import numpy as np
from typing import Optional

import G
from utils import displacement, center_rect, rect_center

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

        # Usage
        self.speed = 1
        self.health = 100
        self.spotting_range = 600
        self.spotted_chance = 1
        self.faction = 0

    def frame(self):
        self.move()
        self.draw()

    def hit(self, x: float, y: float, dmg: float, r: float=0):
        # Check if character has been hit
        mag, _, _,  = displacement((self.x, self.y), (x, y))
        if mag <= self.hitbox_radius:
            self.health -= dmg
            print(self.health)

    def move(self, move: Optional[bool]=True):
        # Moves a single step towards destination
        MOVE_THRESHOLD = 3
        dis, dx, dy = displacement((self.x, self.y), (self.dstx, self.dsty))
        if dis <= MOVE_THRESHOLD:
            return
        if move:
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self):
        self.rect.x, self.rect.y = int(self.x), int(self.y)
        G.WINDOW.blit(self.image,(self.rect.x, self.rect.y))

    def __bool__(self):
        return True


class Enemy(Character):
    def __init__(self, colour, width: float, height: float):
        super().__init__(colour=colour, width=width, height=height)
        

class CharacterGroup(pygame.sprite.Group):
    def hit(self):
        for s in self.__iter__():
            pass
