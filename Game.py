"""Main game logic and state management."""

import pygame
import random
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, POWERUP_SPAWN_CHANCE,
    WAVES, BOSS, COLOR_BG, COLOR_WHITE, COLOR_RED, COLOR_GREEN,
)
from entities import Player, Enemy, Bullet, PowerUp


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)

        self.state = "menu"  # menu, playing, game_over, boss, won
        self.reset_game()

    def reset_game(self):
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.player_group.add(self.player)

        self.current_wave = 0
        self.enemies_spawned = 0
        self.enemies_to_spawn = 0
        self.spawn_timer = 0
        self.wave_complete = False
        self.boss_active = False

    def start_wave(self, wave_index):
        """Start a new wave or the boss."""
        if wave_index < len(WAVES):
            wave = WAVES[wave_index]
            self.enemies_to_spawn = wave["count"]
            self.enemies_spawned = 0
            self.spawn_timer = 0
            self.current_wave = wave_index
            self.wave_complete = False
            self.boss_active = False
        else:
            # Boss time
            self.enemies_to_spawn = 1
            self.enemies_spawned = 0
            self.spawn_timer = 0
            self.current_wave = wave_index
            self.wave_complete = False
            self.boss_active = True

    def spawn_enemy(self):
        """Spawn the next enemy in the current wave."""
        if self.enemies_spawned >= self.enemies_to_spawn:
            return

        self.spawn_timer += 1
        spawn_delay = 30

        if self.spawn_timer >= spawn_delay:
            self.spawn_timer = 0

            if self.boss_active:
                enemy = Enemy(SCREEN_WIDTH // 2, -50, **BOSS)
            else:
                wave = WAVES[self.current_wave]
                enemy = Enemy(
                    random.randint(50, SCREEN_WIDTH - 50),
                    -50,
                    enemy_type=wave["type"],
                    speed=wave["speed"],
                )

            self.enemy_group.add(enemy)
            self.enemies_spawned += 1

            if self.enemies_spawned >= self.enemies_to_spawn:
                self.wave_complete = True

    def handle_input(self):
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == "menu" and event.key == pygame.K_SPACE:
                    self.state = "playing"
                    self.reset_game()
                    self.start_wave(0)
                elif self.state == "game_over" and event.key == pygame.K_SPACE:
                    self.state = "menu"
                elif self.state == "won" and event.key == pygame.K_SPACE:
                    self.state = "menu"
                elif self.state == "playing" and event.key == pygame.K_SPACE:
                    bullets = self.player.shoot()
                    self.bullet_group.add(*bullets)

        if self.state == "playing":
            self.player.update(keys)

    def update(self):
        if self.state != "playing":
            return

        self.spawn_enemy()
        self.enemy_group.update()
        self.bullet_group.update()
        self.powerup_group.update()

        # Collision: bullets hit enemies
        for bullet in self.bullet_group:
            hits = pygame.sprite.spritecollide(bullet, self.enemy_group, False)
            for enemy in hits:
                bullet.kill()
                if enemy.take_damage(1):
                    self.player.score += enemy.score_value
                    if random.random() < POWERUP_SPAWN_CHANCE:
                        ptype = random.choice(["rapid_fire", "shield", "spread_shot"])
                        powerup = PowerUp(enemy.rect.centerx, enemy.rect.centery, ptype)
                        self.powerup_group.add(powerup)

        # Collision: enemies hit player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_group, False)
        for enemy in hits:
            self.player.take_damage()
            enemy.kill()
            if self.player.hp <= 0:
                self.state = "game_over"

        # Collision: player picks up power-ups
        hits = pygame.sprite.spritecollide(self.player, self.powerup_group, True)
        for powerup in hits:
            self.player.activate_powerup(powerup.powerup_type)

        # Wave complete check
        if (self.wave_complete and len(self.enemy_group) == 0):
            if self.boss_active:
                self.state = "won"
            else:
                self.start_wave(self.current_wave + 1)

    def draw(self):
        self.screen.fill(COLOR_BG)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_over":
            self.draw_game_over()
        elif self.state == "won":
            self.draw_won()

        pygame.display.flip()

    def draw_game(self):
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.powerup_group.draw(self.screen)

        # HUD
        score_text = self.font_small.render(f"Score: {self.player.score}", True, COLOR_GREEN)
        self.screen.blit(score_text, (10, 10))

        wave_text = self.font_small.render(
            f"Wave: {self.current_wave + 1 if not self.boss_active else 'BOSS'}",
            True,
            COLOR_WHITE,
        )
        self.screen.blit(wave_text, (SCREEN_WIDTH - 250, 10))

        # Health
        hp_text = self.font_small.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, COLOR_RED)
        self.screen.blit(hp_text, (10, 50))

        # Power-up status
        status_y = 90
        if self.player.rapid_fire:
            rapid_text = self.font_tiny.render("RAPID FIRE", True, COLOR_GREEN)
            self.screen.blit(rapid_text, (10, status_y))
            status_y += 25
        if self.player.shield:
            shield_text = self.font_tiny.render("SHIELD", True, COLOR_GREEN)
            self.screen.blit(shield_text, (10, status_y))
            status_y += 25
        if self.player.spread_shot:
            spread_text = self.font_tiny.render("SPREAD SHOT", True, COLOR_GREEN)
            self.screen.blit(spread_text, (10, status_y))

    def draw_menu(self):
        title = self.font_large.render("SPACE SHOOTER", True, COLOR_WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        instructions = [
            "LEFT/RIGHT or A/D to move",
            "SPACE to shoot",
            "Survive all waves and defeat the boss!",
            "",
            "Press SPACE to start",
        ]
        y = 250
        for line in instructions:
            text = self.font_small.render(line, True, COLOR_GREEN)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 50

    def draw_game_over(self):
        text = self.font_large.render("GAME OVER", True, COLOR_RED)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))

        score_text = self.font_small.render(f"Final Score: {self.player.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))

        restart = self.font_small.render("Press SPACE to return to menu", True, COLOR_GREEN)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 400))

    def draw_won(self):
        text = self.font_large.render("YOU WIN!", True, COLOR_GREEN)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200))

        score_text = self.font_small.render(f"Final Score: {self.player.score}", True, COLOR_WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))

        restart = self.font_small.render("Press SPACE to return to menu", True, COLOR_GREEN)
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 400))

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()