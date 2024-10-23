import pygame
import sys
from random import uniform
import numpy as np
from typing import Tuple

def center_rect(rect: pygame.Rect, x: float, y: float) -> Tuple[float, float]:
    return x - rect.width//2, y - rect.width//2

def rect_center(rect: pygame.Rect) -> Tuple[float, float]:
    return rect.x + rect.width//2, rect.y + rect.height//2

def displacement(start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float, float]:
    mag = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    return mag, (end[0] - start[0])/(mag+0.000001), (end[1] - start[1])/(mag+0.000001)

def displacement_theta(start: Tuple[float, float], end: Tuple[float, float]) -> Tuple[float, float, float, float]:
    mag = np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    dx, dy = (end[0] - start[0])/(mag+0.000001), (end[1] - start[1])/(mag+0.000001)
    return mag, dx, dy, np.arctan2(dy, dx)

def distance(start: Tuple[float, float], end: Tuple[float, float]) -> float:
    return np.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)

def theta(start: Tuple[float, float], end: Tuple[float, float]) -> float:
    return np.arctan2((start[1] - end[1]), (start[0] - end[0]))

def random_sample_circle(pos: Tuple[float, float], r: float) -> Tuple[float, float]:
    theta = uniform(0, 2 * np.pi)
    # Not a uniform sampler !
    d = r * uniform(0, 1)
    x = d * np.cos(theta) + pos[0]
    y = d * np.sin(theta) + pos[1]
    return (x, y)