import pygame
import numpy as np
from utils import displacement, center_rect
import G

class Character(pygame.sprite.Sprite):
    def __init__(self, colour, width: float, height: float):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.selected = False

        self.x, self.y = self.rect.x, self.rect.y
        self.dstx, self.dsty = self.rect.x, self.rect.y
        self.speed = 1

        self.health = 100
        self.hitbox_radius = (self.rect.width + self.rect.height)/4

    def move(self):
        MOVE_THRESHOLD = 3
        dis, dx, dy = displacement(self.x, self.y, self.dstx, self.dsty)
        if dis <= MOVE_THRESHOLD:
            return
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self):
        self.rect.x, self.rect.y = int(self.x), int(self.y)
        G.WINDOW.blit(self.image,(self.rect.x, self.rect.y))

    def frame(self):
        global EVENTS
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

    def hit(self, x: float, y: float, dmg: float):
        mag, _, _,  = displacement(self.x, self.y, x, y)
        if mag <= self.hitbox_radius:
            self.health -= dmg
            print(self.health)

class CharacterGroup(pygame.sprite.Group):
    def hit(self):
        for s in self.__iter__():
            pass
