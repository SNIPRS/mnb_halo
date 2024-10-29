import pygame
import numpy
from random import choice
from typing import List, Union
from enum import Enum

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

def PLAY_SOUND(sound: Union[pygame.mixer.Sound, List[pygame.mixer.Sound]]):
    if isinstance(sound, list):
        sound = choice(list)
    for i in range(MIXER_CHANNELS):
        if not pygame.mixer.Channel(i).get_busy():
            pygame.mixer.Channel(i).play(sound)
            return

def QUEUE_SOUNDS(sounds: List[pygame.mixer.Sound]):
    for i in range(MIXER_CHANNELS):
        if not pygame.mixer.Channel(i).get_busy():
            for s in sounds:
                pygame.mixer.Channel(i).queue(s)
            return

class Sounds(Enum):
    NEEDLER_EX = pygame.mixer.Sound("./assets/sounds/needler_expl_3.wav"),
    GRENADE_EX = pygame.mixer.Sound("./assets/sounds/grenade_expl_0.wav"),
    GRENADE_THROW = pygame.mixer.Sound('./assets/sounds/grenade_throw.wav'),

class Images(Enum):
    BULLET_IMPACT_LARGE = pygame.transform.smoothscale(
        pygame.image.load('assets/decals/impact/small_bullet_impact.png').convert_alpha(), (10, 10))
    BULLET_IMPACT = pygame.transform.smoothscale(
        pygame.image.load('assets/decals/impact/small_bullet_impact.png').convert_alpha(), (7, 7))
    PLASMABURN_CENTER = pygame.image.load('assets/decals/burns/plasma_center0.png').convert_alpha()
    PLASMABURN_PR = pygame.transform.smoothscale(
        pygame.image.load('assets/decals/explosion/plasma_mark/blue.png').convert_alpha(), (24, 24))
    PLASMABURN_PP = pygame.transform.smoothscale(
        pygame.image.load('assets/decals/explosion/plasma_mark/green.png').convert_alpha(), (20, 20))
    PLASMABURN_PPOC = pygame.transform.smoothscale(
        pygame.image.load('assets/decals/explosion/plasma_mark/green.png').convert_alpha(), (60, 60))
    MICRO_SPARK = pygame.image.load('assets/decals/explosion/micro_spark/spark2.png').convert_alpha()
    SMALL_SPARK = pygame.image.load('assets/decals/explosion/small_spark/spark0.png').convert_alpha()

SOUNDS = {
    'needler_expl': pygame.mixer.Sound("./assets/sounds/needler_expl_3.wav"),
    'grenade_expl': pygame.mixer.Sound("./assets/sounds/grenade_expl_0.wav"),
    'grenade_throw': pygame.mixer.Sound('./assets/sounds/grenade_throw.wav'),
}