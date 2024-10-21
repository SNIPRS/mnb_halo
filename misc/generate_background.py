import numpy as np
import pygame
from PIL import Image, ImageFilter
import G
import os
import random

SPRITE_FOLDERS = [
    'assets/terrain/layer0',
    'assets/terrain/layer1',
    'assets/terrain/layer2'
]

def generate_cloud_texture(width, height, scale=100, blur_radius=50):
    low_res_width = width // scale
    low_res_height = height // scale
    noise = np.random.rand(low_res_height, low_res_width) * 255

    noise_image = Image.fromarray(noise.astype(np.uint8), mode='L')
    noise_image = noise_image.resize((width, height), Image.BILINEAR)
    blurred_image = noise_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return np.asarray(blurred_image.convert('RGB'), dtype=np.float32) / 255

def generate_green_base(width = G.WIDTH, height = G.HEIGHT, scale = 2, blur_radius = 20, brightness = 0.7):
    msk = generate_cloud_texture(width, height, scale, blur_radius)
    green = np.zeros(msk.shape)
    green[:,:,0] = 0
    green[:,:,1] = brightness
    green[:,:,2] = brightness/2
    bk = green * msk
    return bk

def fill_sprites(bk: Image) -> Image:

    W, H = bk.size
    for f in SPRITE_FOLDERS:
        sprites = load_sprites(f)
        for sp in sprites:
            pass



def to_image(bk):
    return Image.fromarray((255 * bk).astype(np.uint8), mode='RGB')

def load_sprites(folder_path: str):
    sprites = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            sprite_path = os.path.join(folder_path, filename)
            sprite = Image.open(sprite_path).convert("RGBA")
            sprites.append(sprite)
    return sprites

def generate_background():
    img = generate_green_base().swapaxes(0, 1) * 255 # Need to transpose?
    img = pygame.surfarray.make_surface(img.astype(np.uint8))
    G.BACKGROUND_IMG = img