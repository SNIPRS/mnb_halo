import sys
sys.dont_write_bytecode = True

import pygame
import random
import numpy as np

from utils import center_rect, displacement
import G
from sprite.character import Character

pygame.display.set_caption('mnb_halo')
test = Character('red', 30, 30)


def main():
    looping = True
    while looping :
        # update game state
        G.EVENTS = pygame.event.get()
        for event in G.EVENTS:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        G.WINDOW.fill('white')

        # update character state
        test.frame()

        pygame.display.update()
        G.CLOCK.tick(60)

if __name__ == '__main__':
    main()
