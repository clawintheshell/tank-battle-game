#!/usr/bin/env python3
"""
Tank Battle Game
A classic tank battle game with destructible environments.
"""

import pygame
import sys
import os
import random
from enum import Enum
import json

# Initialize pygame
pygame.init()
try:
    pygame.mixer.init()
    audio_available = True
except pygame.error as e:
    print(f"⚠️  Audio initialization failed: {e}")
    print("⚠️  Game will run without sound effects")
    audio_available = False

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40
GRID_WIDTH = 20
GRID_HEIGHT = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)
ICE_BLUE = (200, 230, 255)

# Tile types
class TileType(Enum):
    GRASS = 0
    BRICK = 1
    STEEL = 2
    WATER = 3
    FOREST = 4
    ICE = 5
    PLAYER_SPAWN = 6
    ENEMY_SPAWN = 7
    POWERUP_SPAWN = 8

# Direction vectors
class Direction:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)

class Tank:
    def __init__(self, x, y, color, direction=Direction.UP, is_player=False):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.speed = 2
        self.is_player = is_player
        self.health = 100
        self.max_health = 100
        self.bullet_cooldown = 0
        self.bullet_cooldown_time = 20  # frames
        self.size = TILE_SIZE - 4
        self.alive = True
        self.score = 0
        
    def move(self, dx, dy, game_map):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check map bounds
        if (0 <= new_x <= SCREEN_WIDTH - self.size and 
            0 <= new_y <= SCREEN_HEIGHT - self.size):
            
            # Check collision with walls (simple grid-based)
            grid_x = int(new_x // TILE_SIZE)
            grid_y = int(new_y // TILE_SIZE)
            
            # Check all four corners of the tank
            corners = [
                (grid_x, grid_y),
                (grid_x + 1, grid_y),
                (grid_x, grid_y + 1),
                (grid_x + 1, grid_y + 1)
            ]
            
            can_move = True
            for cx, cy in corners:
                if 0 <= cx < GRID_WIDTH and 0 <= cy < GRID_HEIGHT:
                    tile = game_map[cy][cx]
                    # Can't move through walls or water
                    if tile in [TileType.BRICK.value, TileType.STEEL.value, TileType.WATER.value]:
                        can_move = False
                        break
            
            if can_move:
                self.x = new_x
                self.y = new_y
                if dx != 0 or dy != 0:
                    self.direction = (dx, dy)
                return True
        return False
    
    def shoot(self):
        if self.bullet_cooldown <= 0:
            self.bullet_cooldown = self.bullet_cooldown_time
            # Create bullet in front of tank
            bullet_x = self.x + self.size // 2
            bullet_y = self.y + self.size // 2
            return Bullet(bullet_x, bullet_y, self.direction, self.color, self.is_player)
        return None
    
    def update(self):
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
    
    def draw(self, screen):
        if not self.alive:
            return
            
        # Draw tank body
        tank_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.color, tank_rect)
        pygame.draw.rect(screen, BLACK, tank_rect, 2)
        
        # Draw tank turret (direction indicator)
        turret_length = self.size // 2
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        end_x = center_x + self.direction[0] * turret_length
        end_y = center_y + self.direction[1] * turret_length
        pygame.draw.line(screen, YELLOW, (center_x, center_y), (end_x, end_y), 4)
        
        # Draw health bar
        health_width = self.size
        health_height = 4
        health_x = self.x
        health_y = self.y - 8
        health_ratio = self.health / self.max_health
        
        # Background (red)
        pygame.draw.rect(screen, RED, (health_x, health_y, health_width, health_height))
        # Foreground (green)
        pygame.draw.rect(screen, GREEN, (health_x, health_y, health_width * health_ratio, health_height))
        
        # Draw player indicator
        if self.is_player:
            pygame.draw.circle(screen, YELLOW, (center_x, self.y - 15), 5)

class Bullet:
    def __init__(self, x, y, direction, color, from_player=False):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = 5
        self.radius = 4
        self.from_player = from_player
        self.alive = True
        
    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # Check if bullet is out of bounds
        if (self.x < 0 or self.x > SCREEN_WIDTH or 
            self.y < 0 or self.y > SCREEN_HEIGHT):
            self.alive = False
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius - 1)

class EnemyTank(Tank):
    def __init__(self, x, y):
        super().__init__(x, y, RED)
        self.is_player = False
        self.ai_timer = 0
        self.ai_direction = Direction.NONE
        self.shoot_chance = 0.02  # 2% chance per frame
        
    def update_ai(self, player_tank, game_map):
        self.ai_timer -= 1
        
        if self.ai_timer <= 0:
            # Choose new random direction
            directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            self.ai_direction = random.choice(directions)
            self.ai_timer = random.randint(30, 90)  # 0.5 to 1.5 seconds
        
        # Try to move in AI direction
        self.move(self.ai_direction[0], self.ai_direction[1], game_map)
        
        # Random shooting
        if random.random() < self.shoot_chance:
            return self.shoot()
        
        return None

class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # 'health', 'speed', 'shield'
        self.size = TILE_SIZE // 2
        self.alive = True
        self.colors = {
            'health': GREEN,
            'speed': YELLOW,
            'shield': BLUE
        }
        self.symbols = {
            'health': 'H',
            'speed': 'S',
            'shield': 'D'
        }
        
    def draw(self, screen):
        if not self.alive:
            return
            
        rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
        pygame.draw.rect(screen, self.colors[self.type], rect)
        pygame.draw.rect(screen, WHITE, rect, 2)
        
        # Draw symbol
        font = pygame.font.Font(None, 24)
        text = font.render(self.symbols[self.type], True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tank Battle Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "playing"  # "playing", "paused", "game_over", "level_complete"
        
        # Initialize game objects
        self.player = None
        self.enemies = []
        self.bullets = []
        self.powerups = []
        self.game_map = []
        self.level = 1
        self.score = 0
        self.lives = 3
        
        # Load default map
        self.load_default_map()
        
        # Spawn player
        self.spawn_player()
        
        # Spawn initial enemies
        self.spawn_enemies(2 + self.level)
        
        # UI font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def load_default_map(self):
        # Create a simple default map
        self.game_map = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                # Borders are walls
                if x == 0 or x == GRID_WIDTH - 1 or y == 0 or y == GRID_HEIGHT - 1:
                    row.append(TileType.BRICK.value)
                else:
                    # Random terrain
                    rand = random.random()
                    if rand < 0.7:
                        row.append(TileType.GRASS.value)
                    elif rand < 0.8:
                        row.append(TileType.BRICK.value)
                    elif rand < 0.85:
                        row.append(TileType.FOREST.value)
                    elif rand < 0.9:
                        row.append(TileType.WATER.value)
                    else:
                        row.append(TileType.ICE.value)
            self.game_map.append(row)
        
        # Clear center area for player
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if 0 <= center_x + dx < GRID_WIDTH and 0 <= center_y + dy < GRID_HEIGHT:
                    self.game_map[center_y + dy][center_x + dx] = TileType.GRASS.value
        
        # Set player spawn
        self.game_map[center_y][center_x] = TileType.PLAYER_SPAWN.value
        
        # Set some enemy spawns
        for _ in range(3):
            ex = random.randint(2, GRID_WIDTH - 3)
            ey = random.randint(2, GRID_HEIGHT - 3)
            if abs(ex - center_x) > 3 or abs(ey - center_y) > 3:  # Not too close to player
                self.game_map[ey][ex] = TileType.ENEMY_SPAWN.value
    
    def spawn_player(self):
        # Find player spawn position
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.game_map[y][x] == TileType.PLAYER_SPAWN.value:
                    player_x = x * TILE_SIZE + 2
                    player_y = y * TILE_SIZE + 2
                    self.player = Tank(player_x, player_y, BLUE, Direction.UP, True)
                    return
    
    def spawn_enemies(self, count):
        enemy_spawns = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.game_map[y][x] == TileType.ENEMY_SPAWN.value:
                    enemy_spawns.append((x, y))
        
        for _ in range(min(count, len(enemy_spawns))):
            if enemy_spawns:
                x, y = random.choice(enemy_spawns)
                enemy_spawns.remove((x, y))
                enemy_x = x * TILE_SIZE + 2
                enemy_y = y * TILE_SIZE + 2
                self.enemies.append(EnemyTank(enemy_x, enemy_y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.game_state = "paused" if self.game_state == "playing" else "playing"
                elif event.key == pygame.K_r and self.game_state in ["game_over", "level_complete"]:
                    self.__init__()  # Restart game
                elif event.key == pygame.K_SPACE and self.game_state == "playing":
                    # Player shooting
                    bullet = self.player.shoot()
                    if bullet:
                        self.bullets.append(bullet)
        
        if self.game_state == "playing":
            # Player movement
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            
            if dx != 0 or dy != 0:
                self.player.move(dx, dy, self.game_map)
    
    def update(self):
        if self.game_state != "playing":
            return
            
        # Update player
        self.player.update()
        
        # Update enemies and their AI
        for enemy in self.enemies[:]:
            enemy.update()
            bullet = enemy.update_ai(self.player, self.game_map)
            if bullet:
                self.bullets.append(bullet)
            
            # Remove dead enemies
            if not enemy.alive:
                self.enemies.remove(enemy)
                self.score += 100
                
                # Chance to drop powerup
                if random.random() < 0.3:
                    powerup_type = random.choice(['health', 'speed', 'shield'])
                    self.powerups.append(PowerUp(enemy.x, enemy.y, powerup_type))
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            
            # Check bullet collision with walls
            grid_x = int(bullet.x // TILE_SIZE)
            grid_y = int(bullet.y // TILE_SIZE)
            
            if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                tile = self.game_map[grid_y][grid_x]
                
                # Destroy brick walls
                if tile == TileType.BRICK.value:
                    self.game_map[grid_y][grid_x] = TileType.GRASS.value
                    bullet.alive = False
                    self.score += 10
                
                # Stop bullets at steel walls
                elif tile == TileType.STEEL.value:
                    bullet.alive = False
            
            # Check bullet collision with tanks
            if bullet.from_player:
                # Check collision with enemies
                for enemy in self.enemies[:]:
                    if (abs(bullet.x - (enemy.x + enemy.size//2)) < enemy.size//2 and
                        abs(bullet.y - (enemy.y + enemy.size//2)) < enemy.size//2):
                        enemy.health -= 25
                        bullet.alive = False
                        if enemy.health <= 0:
                            enemy.alive = False
            else:
                # Check collision with player
                if (self.player.alive and
                    abs(bullet.x - (self.player.x + self.player.size//2)) < self.player.size//2 and
                    abs(bullet.y - (self.player.y + self.player.size//2)) < self.player.size//2):
                    self.player.health -= 25
                    bullet.alive = False
                    if self.player.health <= 0:
                        self.player.alive = False
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_state = "game_over"
                        else:
                            # Respawn player
                            self.spawn_player()
            
            # Remove dead bullets
            if not bullet.alive:
                self.bullets.remove(bullet)
        
        # Update powerups
        for powerup in self.powerups[:]:
            # Check collision with player
            if (self.player.alive and
                abs(powerup.x - (self.player.x + self.player.size//2)) < self.player.size//2 and
                abs(powerup.y - (self.player.y + self.player.size//2)) < self.player.size//2):
                self.apply_powerup(powerup.type)
                powerup.alive = False
                self.score += 50
            
            if not powerup.alive:
                self.powerups.remove(powerup)
        
        # Check level completion
        if len(self.enemies) == 0:
            self.game_state = "level_complete"
            self.score += 500
    
    def apply_powerup(self, type):
        if type == 'health':
            self.player.health = min(self.player.max_health, self.player.health + 50)
        elif type == 'speed':
            self.player.speed = 4
            # Reset after delay (simplified - would need timer in real implementation)
        elif type == 'shield':
            # Simplified shield effect
            pass
    
    def draw_map(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile = self.game_map[y][x]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                # Draw tile based on type
                if tile == TileType.GRASS.value:
                    pygame.draw.rect(self.screen, DARK_GREEN, rect)
                    pygame.draw.rect(self.screen, (0, 80, 0), rect, 1)
                elif tile == TileType.BRICK.value:
                    pygame.draw.rect(self.screen, BROWN, rect)
                    # Draw brick pattern
                    for i in range(0, TILE_SIZE, 5):
                        pygame.draw.line(self.screen, (100, 50, 0), 
                                        (rect.x, rect.y + i), 
                                        (rect.x + TILE_SIZE, rect.y + i), 1)
                elif tile == TileType.STEEL.value:
                    pygame.draw.rect(self.screen, GRAY, rect)
                    pygame.draw.rect(self.screen, (60, 60, 60), rect, 2)
                elif tile == TileType.WATER.value:
                    pygame.draw.rect(self.screen, BLUE, rect)
                    # Water animation effect
                    for i in range(0, TILE_SIZE, 8):
                        pygame.draw.line(self.screen, LIGHT_BLUE, 
                                        (rect.x + i, rect.y), 
                                        (rect.x, rect.y + i), 1)
                elif tile == TileType.FOREST.value:
                    pygame.draw.rect(self.screen, (0, 80, 0), rect)
                    # Draw trees
                    pygame.draw.rect(self.screen, (100, 50, 0), 
                                    (rect.x + TILE_SIZE//2 - 2, rect.y + 5, 4, TILE_SIZE - 10))
                    pygame.draw.circle(self.screen, (0, 120, 0), 
                                    (rect.x + TILE_SIZE//2, rect.y + TILE_SIZE//3), 
                                    TILE_SIZE//3)
                elif tile == TileType.ICE.value:
                    pygame.draw.rect(self.screen, ICE_BLUE, rect)
                    pygame.draw.rect(self.screen, (150, 200, 255), rect, 1)
                elif tile == TileType.PLAYER_SPAWN.value:
                    pygame.draw.rect(self.screen, (0, 150, 0), rect)
                    pygame.draw.rect(self.screen, GREEN, rect, 2)
                elif tile == TileType.ENEMY_SPAWN.value:
                    pygame.draw.rect(self.screen, (150, 0, 0), rect)
                    pygame.draw.rect(self.screen, RED, rect, 2)
    
    def draw_ui(self):
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw level
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 50))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 90))
        
        # Draw player health
        if self.player and self.player.alive:
            health_text = self.small_font.render(f"Health: {self.player.health}", True, GREEN)
            self.screen.blit(health_text, (SCREEN_WIDTH - 120, 10))
        
        # Draw enemy count
        enemies_text = self.small_font.render(f"Enemies: {len(self.enemies)}", True, RED)
        self.screen.blit(enemies_text, (SCREEN_WIDTH - 120, 40))
        
        # Draw controls help
        controls = [
            "WASD/Arrows: Move",
            "Space: Shoot",
            "P: Pause",
            "ESC: Quit",
            "R: Restart (game over)"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, YELLOW)
            self.screen.blit(text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150 + i * 25))
        
        # Game state messages
        if self.game_state == "paused":
            pause_text = self.font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
            
            continue_text = self.small_font.render("Press P to continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(continue_text, continue_rect)
        
        elif self.game_state == "game_over":
            game_over_text = self.font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            self.screen.blit(game_over_text, text_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, YELLOW)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(score_text, score_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(restart_text, restart_rect)
        
        elif self.game_state == "level_complete":
            complete_text = self.font.render("LEVEL COMPLETE!", True, GREEN)
            text_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40))
            self.screen.blit(complete_text, text_rect)
            
            next_text = self.font.render(f"Score: +500", True, YELLOW)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(next_text, next_rect)
            
            continue_text = self.small_font.render("Press R for next level", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(continue_text, continue_rect)
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw game elements
        self.draw_map()
        
        # Draw powerups
        for powerup in self.powerups:
            powerup.draw(self.screen)
        
        # Draw player
        if self.player and self.player.alive:
            self.player.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    print("Starting Tank Battle Game...")
    print("Controls:")
    print("  WASD or Arrow Keys: Move tank")
    print("  Spacebar: Shoot")
    print("  P: Pause/Resume")
    print("  ESC: Quit game")
    print("  R: Restart (when game over)")
    print("\nGood luck, commander!")
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()