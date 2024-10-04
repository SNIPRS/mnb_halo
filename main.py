import pygame
import sys
import random
import numpy as np

pygame.init()
WIDTH, HEIGHT = 500, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('mnb_halo')


def center_rect(rect: pygame.Rect, x, y):
    return x - rect.width//2, y - rect.width//2

def displacement(x, y, xp, yp):
    mag = np.sqrt((x - xp)**2 + (y - yp)**2)
    return (xp - x)/mag, (yp - y)/mag, mag

class Character(pygame.sprite.Sprite):
    def __init__(self, colour, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.selected = False

        self.x, self.y = self.rect.x, self.rect.y
        self.dstx, self.dsty = self.rect.x, self.rect.y
        self.speed = 0.2

    def move(self):
        MOVE_THRESHOLD = 3
        dx, dy, dis = displacement(self.x, self.y, self.dstx, self.dsty)
        if dis <= MOVE_THRESHOLD:
            return
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self):
        global window
        self.rect.x, self.rect.y = int(self.x), int(self.y)
        window.blit(self.image,(self.rect.x, self.rect.y))

    def frame(self):
        global EVENTS
        for event in EVENTS:
            if (not self.selected and event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and self.rect.collidepoint(event.pos)):
                self.selected = True
            elif (self.selected and event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1):
                self.selected = False
                self.dstx, self.dsty = center_rect(self.rect, event.pos[0], event.pos[1])
        self.move()
        self.draw()


test = Character('red', 30, 30)
EVENTS = None

def main():
    looping = True
    
    while looping :
        # Get inputs
        global EVENTS
        EVENTS = pygame.event.get()
        for event in EVENTS:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('white')

        test.frame()

        
        pygame.display.update()
        clock.tick(60)

main()
