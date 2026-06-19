"""Game configuration and constants."""

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
COLOR_BG = (10, 10, 20)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 50, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_CYAN = (0, 255, 255)

# Player
PLAYER_SPEED = 5
PLAYER_SHOOT_COOLDOWN = 10
PLAYER_MAX_HP = 3

# Bullets
BULLET_SPEED = 7
BULLET_DAMAGE = 1

# Enemies
ENEMY_SPAWN_RATE = 30  # frames between spawns in wave
ENEMY_BASE_SPEED = 2

# Power-ups
POWERUP_SPAWN_CHANCE = 0.15  # 15% chance when enemy dies
POWERUP_DURATION = 300  # frames (5 seconds at 60 FPS)

# Waves
WAVES = [
    {"type": "drone", "count": 5, "speed": 1.5},
    {"type": "drone", "count": 8, "speed": 1.5},
    {"type": "striker", "count": 4, "speed": 2.5},
    {"type": "drone", "count": 6, "speed": 1.5},
    {"type": "striker", "count": 6, "speed": 2.5},
    {"type": "tank", "count": 3, "speed": 1.0},
]

BOSS = {"type": "boss", "speed": 1.0, "hp": 50}

