import pygame
import numpy
from typing import List

# Globals

pygame.init()

DEGREE_TO_RAD = 0.01745329252
PI = 3.14159265359
TAU = PI * 2

BACKGROUND_COL = (0, 90, 10)
BACKGROUND_IMG = None
WIDTH, HEIGHT = 600, 1000

PLAYER_FAC = 0

CHARS_ALL = pygame.sprite.Group() # Group of Character objects
CHAR_AI_ALL = pygame.sprite.Group()

SPRITE_SIZE = 15
UNIT = SPRITE_SIZE

FIRING_EFFECTS = pygame.sprite.Group()
DECALS = pygame.sprite.Group()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
EVENTS = pygame.event.get()

MIXER_CHANNELS = 25
pygame.mixer.set_num_channels(MIXER_CHANNELS)

def PLAY_SOUND(sound: pygame.mixer.Sound):
    for i in range(MIXER_CHANNELS):
        if not pygame.mixer.Channel(i).get_busy():
            pygame.mixer.Channel(i).play(sound)
            return

def QUEUE_SOUND(sounds: List[pygame.mixer.Sound]):
    for i in range(MIXER_CHANNELS):
        if not pygame.mixer.Channel(i).get_busy():
            for s in sounds:
                pygame.mixer.Channel(i).queue(s)
            return