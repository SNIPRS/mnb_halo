import numpy as np
import pygame
from PIL import Image, ImageFilter
import G

def generate_cloud_texture(width, height, scale=10, blur_radius=2):
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

def to_image(bk):
    return Image.fromarray((255 * bk).astype(np.uint8), mode='RGB')

def generate_background():
    img = 255 * generate_green_base().swapaxes(0, 1) # Need to transpose?
    img = pygame.surfarray.make_surface(img.astype(np.uint8))
    G.BACKGROUND_IMG = img