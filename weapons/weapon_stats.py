import pygame

from sprite.projectile import *



# Base weapon stats ======================================================
# for quickly changing values

WEAPON_ASSAULT_RIFLE = {
    'mag_cap': 60, # Magazine capacity
    'firerate': 10, # Rounds per second
    'error': 5, # Error angle in degrees
    'aim_time': 2, # Takes this long to aim before firing
    'reload_time': [5, 7], # Seconds: min, max
    'burst_range': [2, 10], # min, max
    'subburst_probability': 0.05, # Probability of each shot of stopping
    'subburst_delay': [0.5, 1.5], # Seconds: min, max
    'spread_heat': 1.5, # Spread increase per shot
    'cooldown': [4, 6], # Time to wait after a burst
    'projectile': ProjectileBullet, # Projectile

    'sound_fire': pygame.mixer.Sound("./assets/sounds/ar_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/ar_reload.wav")

}

WEAPON_SHOTGUN = {
    'mag_cap': 100,
    'firerate': 8,
    'error': 4,
    'aim_time': 2,
    'reload_time': [0, 0],
    'burst_range': [1, 4],
    'subburst_probability': 0.25,
    'subburst_delay': [0.5, 1.0],
    'spread_heat': 2.5,
    'cooldown': [5, 8],
    'projectile': ProjectileBolt,

    'sound_fire': pygame.mixer.Sound("./assets/sounds/ar_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/ar_reload.wav"),
}

WEAPON_PLASMA_RIFLE = {
    'mag_cap': 100,
    'firerate': 8,
    'error': 4,
    'aim_time': 2,
    'reload_time': [0, 0],
    'burst_range': [1, 4],
    'subburst_probability': 0.25,
    'subburst_delay': [0.5, 1.0],
    'spread_heat': 2.5,
    'cooldown': [5, 8],
    'projectile': ProjectileBolt,

    'sound_fire': pygame.mixer.Sound("./assets/sounds/ar_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/ar_reload.wav"),

    'firerate_decay': 1.1, # Multiplies the delay between shots
}

WEAPON_NEEDLER = {
    'mag_cap': 20,
    'firerate': 12,
    'error': 4,
    'aim_time': 1.5,
    'reload_time': [6, 10],
    'burst_range': [1, 6],
    'subburst_probability': 0.20,
    'subburst_delay': [0.6, 1.2],
    'spread_heat': 2,
    'cooldown': [10, 15],
    'projectile': ProjectileTracking,

    'sound_fire': pygame.mixer.Sound("./assets/sounds/ar_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/ar_reload.wav"),
}

