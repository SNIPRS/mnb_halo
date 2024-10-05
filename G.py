import pygame
import numpy

# Globals

pygame.init()

BACKGROUND_COL = (0, 90, 10)

WIDTH, HEIGHT = 600, 1000
CHARACTERS = pygame.sprite.Group() # Group of Character objects
FIRING_EFFECTS = pygame.sprite.Group()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
EVENTS = pygame.event.get()