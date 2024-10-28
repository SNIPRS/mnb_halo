import pygame

from sprite.projectile import *



# Base weapon stats ======================================================
# for quickly changing values

WEAPON_ASSAULT_RIFLE = {
    'mag_cap': 60, # Magazine capacity
    'firerate': 10, # Rounds per second
    'error': 2, # Error angle in degrees
    'aim_time': 2, # Takes this long to aim before firing
    'reload_time': [5, 7], # Seconds: min, max
    'burst_range': [5, 20], # min, max
    'subburst_probability': 0.05, # Probability of each shot of stopping
    'subburst_delay': [0.5, 1.5], # Seconds: min, max
    'spread_heat': 1.5, # Spread increase per shot
    'cooldown': [4, 6], # Time to wait after a burst
    'projectile': ProjectileBullet, # Projectile

    'sound_fire': pygame.mixer.Sound("./assets/sounds/ar_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/ar_reload.wav")

}

WEAPON_BATTLE_RIFLE = {
    'mag_cap': 12, # Magazine capacity # 3 round bursts
    'firerate': 1.5, # Rounds per second
    'error': 1, # Error angle in degrees
    'aim_time': 1.5, # Takes this long to aim before firing
    'reload_time': [5, 7], # Seconds: min, max
    'burst_range': [2, 4], # min, max
    'subburst_probability': 0.3, # Probability of each shot of stopping
    'subburst_delay': [0.5, 1.5], # Seconds: min, max
    'spread_heat': 0, # Spread increase per shot
    'cooldown': [4, 6], # Time to wait after a burst
    'projectile': ProjectileBullet, # Projectile

    'sound_fire': pygame.mixer.Sound("./assets/sounds/br_fire.wav"), # need a sound for 3 round burst
    'sound_reload': pygame.mixer.Sound("./assets/sounds/br_reload.wav"),

    'burst_size': 3,
    'burst_rof': 20, # rounds per second
    'burst_heat': 1 # spread increase per shot
}

WEAPON_SHOTGUN = {
    'mag_cap': 8,
    'firerate': 1,
    'error': 7,
    'aim_time': 1.5,
    'reload_time': [6, 8],
    'burst_range': [1, 3],
    'subburst_probability': 1,
    'subburst_delay': [0.0, 1.0],
    'spread_heat': 2.5,
    'cooldown': [5, 8],
    'projectile': ProjectileShotgun,

    'sound_fire': pygame.mixer.Sound("./assets/sounds/shotgun_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/shotgun_reload.wav"),
    'sound_full_reload': pygame.mixer.Sound("./assets/sounds/shotgun_full_reload.wav"),

    'pellets': 8,
    'sound_pump': pygame.mixer.Sound("assets/sounds/shotgun_ready.wav"),
    'sound_open': pygame.mixer.Sound("assets/sounds/shotgun_open.wav"),
    'sound_close': pygame.mixer.Sound("assets/sounds/shotgun_close.wav"),
}

WEAPON_PLASMA_RIFLE = {
    'mag_cap': 100,
    'firerate': 8,
    'error': 2,
    'aim_time': 2,
    'reload_time': [0, 0],
    'burst_range': [3, 7],
    'subburst_probability': 0.25,
    'subburst_delay': [0.5, 1.0],
    'spread_heat': 2.5,
    'cooldown': [5, 8],
    'projectile': ProjectilePlasmaRifle,

    'sound_fire': pygame.mixer.Sound("./assets/sounds/pr_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/ar_reload.wav"),

    'firerate_decay': 1.1, # Multiplies the delay between shots
}

WEAPON_NEEDLER = {
    'mag_cap': 20,
    'firerate': 12,
    'error': 4,
    'aim_time': 1.5,
    'reload_time': [6, 10],
    'burst_range': [2, 8],
    'subburst_probability': 0.20,
    'subburst_delay': [0.6, 1.2],
    'spread_heat': 2,
    'cooldown': [10, 15],
    'projectile': ProjectileTracking,

    'sound_explode': pygame.mixer.Sound("./assets/sounds/needler_expl_3.wav"),
    'sound_fire': pygame.mixer.Sound("./assets/sounds/needler_fire.wav"),
    'sound_reload': pygame.mixer.Sound("./assets/sounds/needler_reload.wav"),
}

WEAPON_FRAG_GRENADE = {
    'sound': G.SOUNDS['grenade_throw'],
    'error': 12,
    'safe_d': G.UNIT * 8,

}