import math
import random
import pygame
from enemy import Enemy


class AdaptiveEnemyManager:
    """Tracks player movement bias and spawns enemies with patterns that react to it."""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Player movement observation
        self.move_right_count = 0
        self.move_left_count = 0
        self.pattern_timer = 0.0
        self.pattern_duration = 3.0  # seconds between pattern re-evaluation

        # Current pattern choice
        self.current_pattern = "straight"  # straight, arc_left, arc_right, zigzag

    def observe_player(self, keys, dt):
        if keys[pygame.K_LEFT]:
            self.move_left_count += 1
        if keys[pygame.K_RIGHT]:
            self.move_right_count += 1
        self.pattern_timer += dt

    def _compute_bias(self):
        total = self.move_left_count + self.move_right_count
        if total == 0:
            return 0.0
        return (self.move_right_count - self.move_left_count) / total

    def maybe_update_pattern(self):
        """Pick a pattern based on player dodge bias every pattern_duration seconds."""
        if self.pattern_timer < self.pattern_duration:
            return

        bias = self._compute_bias()  # >0 means tends right, <0 tends left
        if bias > 0.2:
            self.current_pattern = "arc_right"
        elif bias < -0.2:
            self.current_pattern = "arc_left"
        else:
            self.current_pattern = "zigzag"

        # Reset observation window
        self.move_left_count = 0
        self.move_right_count = 0
        self.pattern_timer = 0.0

    def spawn_enemy(self, speed):
        """Create a new enemy positioned above the screen with the current pattern."""
        e = Enemy(
            x=random.randint(0, self.screen_width - 50),
            y=random.randint(-300, -50),
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            speed=speed,
        )
        e.pattern = self.current_pattern
        e.time = 0.0
        e.zigzag_amp = 60
        e.zigzag_freq = 6
        e.curve_speed = 80
        return e


def update_enemy_pattern(enemy, dt):
    """Mutate enemy position based on its pattern."""
    enemy.time = getattr(enemy, "time", 0.0) + dt
    enemy.rect.y += enemy.speed * dt

    pattern = getattr(enemy, "pattern", "straight")
    if pattern == "arc_left":
        enemy.rect.x -= enemy.curve_speed * dt
    elif pattern == "arc_right":
        enemy.rect.x += enemy.curve_speed * dt
    elif pattern == "zigzag":
        enemy.rect.x += enemy.zigzag_amp * math.sin(enemy.time * enemy.zigzag_freq) * dt

    # Keep within screen bounds horizontally
    enemy.rect.x = max(0, min(enemy.rect.x, enemy.width - enemy.rect.width))

    # If off the bottom, recycle to top
    if enemy.rect.top > enemy.height:
        enemy.rect.x = random.randint(0, enemy.width - enemy.rect.width)
        enemy.rect.y = random.randint(-200, -50)
        enemy.time = 0.0
