import pygame
import numpy as np

import G
from utils import displacement, center_rect, rect_center
from sprite.firing_effect import FiringEffect
from weapons.weapon import Weapon

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
        self.weapon = Weapon()
        self.spotting_range = 600
        self.spotted_chance = 1
        self.faction = 0
        

    def frame(self):
        for event in G.EVENTS:
            if (not self.selected and event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(event.pos)):
                self.selected = True
            elif (self.selected and event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1):
                self.selected = False
                self.dstx, self.dsty = center_rect(self.rect, event.pos[0], event.pos[1])
        self.move()
        self.draw()
        self.weapon.frame(rect_center(self.rect), (G.WIDTH//2, G.HEIGHT//2))

    def hit(self, x: float, y: float, dmg: float, r: float=0):
        # Check if character has been hit
        mag, _, _,  = displacement((self.x, self.y), (x, y))
        if mag <= self.hitbox_radius:
            self.health -= dmg
            print(self.health)

    def move(self):
        # Moves a single step towards destination
        MOVE_THRESHOLD = 3
        dis, dx, dy = displacement((self.x, self.y), (self.dstx, self.dsty))
        if dis <= MOVE_THRESHOLD:
            return
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self):
        self.rect.x, self.rect.y = int(self.x), int(self.y)
        G.WINDOW.blit(self.image,(self.rect.x, self.rect.y))


class Enemy(Character):
    def __init__(self, colour, width: float, height: float):
        super().__init__(colour=colour, width=width, height=height)
        

class CharacterGroup(pygame.sprite.Group):
    def hit(self):
        for s in self.__iter__():
            pass
