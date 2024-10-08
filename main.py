import sys
sys.dont_write_bytecode = True

import pygame
import random
import numpy as np


import G
from utils import center_rect, displacement
from misc.generate_background import generate_background
from ai.character_ai import EnemyCharacterAI, ControllableCharacterAI

pygame.display.set_caption('mnb_halo')
player = ControllableCharacterAI()
enemy = EnemyCharacterAI()

def main():
    generate_background()
    looping = True
    while looping:
        # update game state
        G.EVENTS = pygame.event.get()
        for event in G.EVENTS:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        G.WINDOW.blit(G.BACKGROUND_IMG,(0, 0))

        # update character state
        player.frame()
        enemy.frame()

        for eff in G.FIRING_EFFECTS:
            eff.frame()

        pygame.display.update()
        G.CLOCK.tick(G.FPS)

if __name__ == '__main__':
    main()
