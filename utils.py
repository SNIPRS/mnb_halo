import pygame
import sys
import random
import numpy as np
from typing import Tuple

def center_rect(rect: pygame.Rect, x: float, y: float) -> Tuple[float, float]:
    return x - rect.width//2, y - rect.width//2


def displacement(start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float, float]:
    mag = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    return mag, (end[0] - start[0])/mag, (end[1] - start[1])/mag