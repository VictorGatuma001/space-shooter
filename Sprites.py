"""Procedurally generated pixel art sprites for all game entities."""

import pygame
from constants import COLOR_GREEN, COLOR_RED, COLOR_YELLOW, COLOR_CYAN, COLOR_WHITE


def create_player_sprite(size=40):
    """Create a simple triangular player ship sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Triangle pointing up (classic Galaga style)
    points = [
        (size // 2, 0),  # top point
        (0, size),  # bottom left
        (size, size),  # bottom right
    ]
    pygame.draw.polygon(surf, COLOR_GREEN, points)
    pygame.draw.polygon(surf, COLOR_WHITE, points, 2)
    return surf


def create_drone_sprite(size=30):
    """Create a simple square enemy sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(surf, COLOR_RED, (0, 0, size, size))
    pygame.draw.rect(surf, COLOR_YELLOW, (0, 0, size, size), 2)
    # Add eyes
    pygame.draw.circle(surf, COLOR_YELLOW, (size // 3, size // 3), 2)
    pygame.draw.circle(surf, COLOR_YELLOW, (2 * size // 3, size // 3), 2)
    return surf


def create_striker_sprite(size=30):
    """Create a faster, sleeker enemy sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Diamond shape
    points = [
        (size // 2, 0),
        (size, size // 2),
        (size // 2, size),
        (0, size // 2),
    ]
    pygame.draw.polygon(surf, COLOR_CYAN, points)
    pygame.draw.polygon(surf, COLOR_WHITE, points, 2)
    return surf


def create_tank_sprite(size=35):
    """Create a heavily armored, slow enemy."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Thick square with reinforcement
    pygame.draw.rect(surf, COLOR_RED, (0, 0, size, size))
    pygame.draw.rect(surf, COLOR_YELLOW, (0, 0, size, size), 3)
    # Armor plating (stripes)
    for i in range(2, size, 6):
        pygame.draw.line(surf, COLOR_YELLOW, (i, 0), (i, size), 1)
    return surf


def create_boss_sprite(size=50):
    """Create a large boss enemy sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    # Large octagon-ish shape
    pygame.draw.rect(surf, COLOR_RED, (5, 0, size - 10, size))
    pygame.draw.rect(surf, COLOR_YELLOW, (0, 10, size, size - 20))
    pygame.draw.rect(surf, COLOR_WHITE, (2, 2, size - 4, size - 4), 3)
    # Boss details
    pygame.draw.circle(surf, COLOR_YELLOW, (size // 3, size // 2), 4)
    pygame.draw.circle(surf, COLOR_YELLOW, (2 * size // 3, size // 2), 4)
    return surf


def create_bullet_sprite(size=4):
    """Create a simple bullet sprite."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(surf, COLOR_YELLOW, (size // 2, size // 2), size // 2)
    return surf


def create_powerup_sprite(powerup_type, size=20):
    """Create a powerup sprite based on type."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)

    if powerup_type == "rapid_fire":
        # Lightning bolt shape (simplified)
        pygame.draw.polygon(surf, COLOR_YELLOW, [
            (size // 2, 0), (size // 2 + 3, size // 2),
            (size // 2 + 2, size // 2), (size // 2, size),
            (size // 2 - 2, size // 2), (size // 2 - 3, size // 2),
        ])
    elif powerup_type == "shield":
        # Shield symbol
        pygame.draw.circle(surf, COLOR_CYAN, (size // 2, size // 2), size // 2)
        pygame.draw.circle(surf, COLOR_WHITE, (size // 2, size // 2), size // 2, 2)
    elif powerup_type == "spread_shot":
        # Three bullets
        pygame.draw.circle(surf, COLOR_GREEN, (size // 2, size // 3), 2)
        pygame.draw.circle(surf, COLOR_GREEN, (size // 2, size // 2), 2)
        pygame.draw.circle(surf, COLOR_GREEN, (size // 2, 2 * size // 3), 2)

    return surf