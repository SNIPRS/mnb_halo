import numpy as np
from PIL import Image, ImageFilter

def generate_cloud_texture(width, height, scale=10, blur_radius=2):
    low_res_width = width // scale
    low_res_height = height // scale
    noise = np.random.rand(low_res_height, low_res_width)

    noise_image = Image.fromarray(noise.astype(np.uint8), mode='L')
    noise_image = noise_image.resize((width, height), Image.BILINEAR)

    blurred_image = noise_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    return blurred_image

image_width = 800
image_height = 600
scale = 10
blur_radius = 5

cloud_texture = generate_cloud_texture(image_width, image_height, scale, blur_radius)
cloud_texture.save("cloud_texture.png")
cloud_texture.show()