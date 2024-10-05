import pygame
import numpy

# Globals

pygame.init()

WIDTH, HEIGHT = 600, 1000
CHARACTERS = pygame.sprite.Group() # Group of Character objects

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
EVENTS = pygame.event.get()