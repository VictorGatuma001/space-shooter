"""Game entity classes."""

import pygame
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_SHOOT_COOLDOWN,
    BULLET_SPEED, ENEMY_BASE_SPEED, POWERUP_DURATION,
)
from sprites import (
    create_player_sprite, create_drone_sprite, create_striker_sprite,
    create_tank_sprite, create_boss_sprite, create_bullet_sprite,
    create_powerup_sprite,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = create_player_sprite()
        self.rect = self.image.get_rect(center=(x, y))
        self.hp = 3
        self.max_hp = 3
        self.shoot_cooldown = 0
        self.score = 0
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.shield = False
        self.shield_timer = 0
        self.spread_shot = False
        self.spread_shot_timer = 0

    def update(self, keys):
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))

        # Cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
        else:
            self.rapid_fire = False
        if self.shield_timer > 0:
            self.shield_timer -= 1
        else:
            self.shield = False
        if self.spread_shot_timer > 0:
            self.spread_shot_timer -= 1
        else:
            self.spread_shot = False

    def shoot(self):
        """Return a list of bullet(s) if firing."""
        if self.shoot_cooldown > 0:
            return []

        cooldown = 5 if self.rapid_fire else PLAYER_SHOOT_COOLDOWN
        self.shoot_cooldown = cooldown

        bullets = []
        if self.spread_shot:
            # Three bullets at angles
            angles = [-15, 0, 15]
            for angle in angles:
                b = Bullet(
                    self.rect.centerx, self.rect.top,
                    angle_offset=angle,
                )
                bullets.append(b)
        else:
            bullets.append(Bullet(self.rect.centerx, self.rect.top))

        return bullets

    def take_damage(self):
        if not self.shield:
            self.hp -= 1
        else:
            self.shield = False
            self.shield_timer = 0

    def activate_powerup(self, powerup_type):
        if powerup_type == "rapid_fire":
            self.rapid_fire = True
            self.rapid_fire_timer = POWERUP_DURATION
        elif powerup_type == "shield":
            self.shield = True
            self.shield_timer = POWERUP_DURATION
        elif powerup_type == "spread_shot":
            self.spread_shot = True
            self.spread_shot_timer = POWERUP_DURATION


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle_offset=0):
        super().__init__()
        self.image = create_bullet_sprite()
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.angle_offset = angle_offset

    def update(self):
        # Simple angled movement for spread shot
        self.rect.y -= BULLET_SPEED
        if self.angle_offset != 0:
            self.rect.x += (self.angle_offset / 15) * BULLET_SPEED

        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type="drone", speed=1.0):
        super().__init__()
        self.enemy_type = enemy_type
        self.speed = speed * ENEMY_BASE_SPEED
        self.wave_x = x  # For wave formation
        self.wave_y = y
        self.time = 0

        if enemy_type == "drone":
            self.image = create_drone_sprite()
            self.max_hp = 1
            self.score_value = 100
        elif enemy_type == "striker":
            self.image = create_striker_sprite()
            self.max_hp = 1
            self.score_value = 150
            self.speed *= 1.5
        elif enemy_type == "tank":
            self.image = create_tank_sprite()
            self.max_hp = 3
            self.score_value = 300
            self.speed *= 0.5
        elif enemy_type == "boss":
            self.image = create_boss_sprite()
            self.max_hp = 50
            self.score_value = 1000
            self.speed *= 0.8

        self.hp = self.max_hp
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.time += 1

        # Gentle wave motion while moving down
        self.rect.x = self.wave_x + 15 * (self.time / 30)
        self.rect.y = self.wave_y + self.time * self.speed

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
            return True
        return False


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.powerup_type = powerup_type
        self.image = create_powerup_sprite(powerup_type)
        self.rect = self.image.get_rect(center=(x, y))
        self.time = 0

    def update(self):
        self.time += 1
        # Bob up and down
        self.rect.y += 1 if self.time % 20 < 10 else -1

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()