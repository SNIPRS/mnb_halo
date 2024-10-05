import pygame
import numpy

# Globals

pygame.init()

DEGREE_TO_RAD = 0.01745329252
PI = 3.14159265359

BACKGROUND_COL = (0, 90, 10)

WIDTH, HEIGHT = 600, 1000
CHARACTERS = pygame.sprite.Group() # Group of Character objects
FIRING_EFFECTS = pygame.sprite.Group()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
EVENTS = pygame.event.get()