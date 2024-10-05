import pygame
import sys
import random
import numpy as np
from typing import Tuple

def center_rect(rect: pygame.Rect, x: float, y: float) -> Tuple[float, float]:
    return x - rect.width//2, y - rect.width//2

def rect_center(rect: pygame.Rect) -> Tuple[float, float]:
    return rect.x + rect.width//2, rect.y + rect.height//2

def displacement(start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float, float]:
    mag = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    return mag, (end[0] - start[0])/(mag+0.000001), (end[1] - start[1])/(mag+0.000001)