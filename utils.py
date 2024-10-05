import pygame
import sys
import random
import numpy as np
from typing import Tuple

def center_rect(rect: pygame.Rect, x: float, y: float) -> Tuple[float, float]:
    return x - rect.width//2, y - rect.width//2


def displacement(x: float, y: float, xp: float, yp: float) -> Tuple[float, float, float]:
    mag = np.sqrt((x - xp)**2 + (y - yp)**2)
    return mag, (xp - x)/mag, (yp - y)/mag