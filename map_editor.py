#!/usr/bin/env python3
"""
Tank Battle Map Editor
Create and edit maps for the Tank Battle game.
"""

import pygame
import sys
import os
import json
from enum import Enum

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
UI_PANEL_WIDTH = 200

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
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Tile types (must match game.py)
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

# Tile information
TILE_INFO = [
    {"name": "Grass", "color": DARK_GREEN, "key": "0", "passable": True, "destructible": False},
    {"name": "Brick Wall", "color": BROWN, "key": "1", "passable": False, "destructible": True},
    {"name": "Steel Wall", "color": GRAY, "key": "2", "passable": False, "destructible": False},
    {"name": "Water", "color": BLUE, "key": "3", "passable": False, "destructible": False},
    {"name": "Forest", "color": (0, 80, 0), "key": "4", "passable": True, "destructible": False},
    {"name": "Ice", "color": ICE_BLUE, "key": "5", "passable": True, "destructible": False},
    {"name": "Player Spawn", "color": GREEN, "key": "P", "passable": True, "destructible": False},
    {"name": "Enemy Spawn", "color": RED, "key": "E", "passable": True, "destructible": False},
    {"name": "Power-up Spawn", "color": PURPLE, "key": "U", "passable": True, "destructible": False},
]

class MapEditor:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tank Battle Map Editor")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Map data
        self.map_data = []
        self.selected_tile = 0
        self.map_name = "untitled"
        self.dirty = False
        
        # Initialize empty map
        self.create_empty_map()
        
        # UI state
        self.show_grid = True
        self.show_tile_info = True
        self.brush_size = 1
        
        # Fonts
        self.font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 22)
        
        # Editor mode
        self.mode = "paint"  # "paint", "fill", "select"
        
        # Load default map if exists
        self.load_default_map()
    
    def create_empty_map(self):
        """Create an empty map filled with grass."""
        self.map_data = []
        for y in range(GRID_HEIGHT):
            row = []
            for x in range(GRID_WIDTH):
                row.append(TileType.GRASS.value)
            self.map_data.append(row)
        self.dirty = True
    
    def load_default_map(self):
        """Try to load a default map if it exists."""
        default_map_path = "maps/level1.map"
        if os.path.exists(default_map_path):
            try:
                self.load_map(default_map_path)
                print(f"Loaded default map: {default_map_path}")
            except:
                print("Could not load default map, using empty map")
    
    def draw_map(self):
        """Draw the map grid and tiles."""
        map_surface = pygame.Surface((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
        
        # Draw tiles
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                tile_value = self.map_data[y][x]
                tile_info = TILE_INFO[tile_value]
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                # Draw tile background
                pygame.draw.rect(map_surface, tile_info["color"], rect)
                
                # Draw tile border
                pygame.draw.rect(map_surface, BLACK, rect, 1)
                
                # Draw special indicators
                if tile_value == TileType.PLAYER_SPAWN.value:
                    # Draw "P" in center
                    text = self.small_font.render("P", True, WHITE)
                    text_rect = text.get_rect(center=(x * TILE_SIZE + TILE_SIZE//2, 
                                                     y * TILE_SIZE + TILE_SIZE//2))
                    map_surface.blit(text, text_rect)
                elif tile_value == TileType.ENEMY_SPAWN.value:
                    # Draw "E" in center
                    text = self.small_font.render("E", True, WHITE)
                    text_rect = text.get_rect(center=(x * TILE_SIZE + TILE_SIZE//2,
                                                     y * TILE_SIZE + TILE_SIZE//2))
                    map_surface.blit(text, text_rect)
                elif tile_value == TileType.POWERUP_SPAWN.value:
                    # Draw "U" in center
                    text = self.small_font.render("U", True, WHITE)
                    text_rect = text.get_rect(center=(x * TILE_SIZE + TILE_SIZE//2,
                                                     y * TILE_SIZE + TILE_SIZE//2))
                    map_surface.blit(text, text_rect)
        
        # Draw grid if enabled
        if self.show_grid:
            for x in range(0, GRID_WIDTH * TILE_SIZE, TILE_SIZE):
                pygame.draw.line(map_surface, (50, 50, 50), (x, 0), (x, GRID_HEIGHT * TILE_SIZE), 1)
            for y in range(0, GRID_HEIGHT * TILE_SIZE, TILE_SIZE):
                pygame.draw.line(map_surface, (50, 50, 50), (0, y), (GRID_WIDTH * TILE_SIZE, y), 1)
        
        # Draw cursor/selection
        mouse_pos = pygame.mouse.get_pos()
        map_x = (mouse_pos[0] - 20) // TILE_SIZE
        map_y = (mouse_pos[1] - 20) // TILE_SIZE
        
        if (0 <= map_x < GRID_WIDTH and 0 <= map_y < GRID_HEIGHT and
            mouse_pos[0] < SCREEN_WIDTH - UI_PANEL_WIDTH and mouse_pos[1] < GRID_HEIGHT * TILE_SIZE + 40):
            
            # Draw brush preview
            for dy in range(self.brush_size):
                for dx in range(self.brush_size):
                    px = map_x + dx - self.brush_size // 2
                    py = map_y + dy - self.brush_size // 2
                    if 0 <= px < GRID_WIDTH and 0 <= py < GRID_HEIGHT:
                        preview_rect = pygame.Rect(px * TILE_SIZE, py * TILE_SIZE, 
                                                  TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(map_surface, WHITE, preview_rect, 2)
            
            # Draw coordinates
            coord_text = self.small_font.render(f"({map_x}, {map_y})", True, YELLOW)
            map_surface.blit(coord_text, (10, 10))
        
        # Blit map to screen
        self.screen.blit(map_surface, (20, 40))
    
    def draw_ui_panel(self):
        """Draw the UI panel on the right side."""
        panel_x = SCREEN_WIDTH - UI_PANEL_WIDTH
        panel_rect = pygame.Rect(panel_x, 0, UI_PANEL_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, panel_rect)
        pygame.draw.rect(self.screen, LIGHT_GRAY, panel_rect, 2)
        
        # Draw title
        title_text = self.title_font.render("Map Editor", True, YELLOW)
        self.screen.blit(title_text, (panel_x + 20, 20))
        
        # Draw current map info
        map_info = self.font.render(f"Map: {self.map_name}", True, WHITE)
        self.screen.blit(map_info, (panel_x + 20, 60))
        
        dirty_text = self.small_font.render("*" if self.dirty else "", True, RED)
        self.screen.blit(dirty_text, (panel_x + 20 + map_info.get_width(), 60))
        
        size_text = self.small_font.render(f"Size: {GRID_WIDTH}x{GRID_HEIGHT}", True, WHITE)
        self.screen.blit(size_text, (panel_x + 20, 90))
        
        # Draw selected tile
        selected_text = self.font.render("Selected Tile:", True, WHITE)
        self.screen.blit(selected_text, (panel_x + 20, 130))
        
        tile_info = TILE_INFO[self.selected_tile]
        tile_rect = pygame.Rect(panel_x + 30, 160, TILE_SIZE * 2, TILE_SIZE * 2)
        pygame.draw.rect(self.screen, tile_info["color"], tile_rect)
        pygame.draw.rect(self.screen, WHITE, tile_rect, 2)
        
        tile_name = self.small_font.render(tile_info["name"], True, WHITE)
        self.screen.blit(tile_name, (panel_x + 30, 160 + TILE_SIZE * 2 + 10))
        
        # Draw tile palette
        palette_y = 250
        palette_text = self.font.render("Tile Palette:", True, WHITE)
        self.screen.blit(palette_text, (panel_x + 20, palette_y))
        
        palette_y += 40
        for i, tile in enumerate(TILE_INFO):
            tile_rect = pygame.Rect(panel_x + 20, palette_y, TILE_SIZE * 1.5, TILE_SIZE * 1.5)
            
            # Highlight selected tile
            if i == self.selected_tile:
                pygame.draw.rect(self.screen, YELLOW, tile_rect, 3)
            else:
                pygame.draw.rect(self.screen, LIGHT_GRAY, tile_rect, 1)
            
            pygame.draw.rect(self.screen, tile["color"], 
                           (tile_rect.x + 2, tile_rect.y + 2, 
                            tile_rect.width - 4, tile_rect.height - 4))
            
            # Draw tile key
            key_text = self.small_font.render(tile["key"], True, WHITE)
            key_rect = key_text.get_rect(center=(tile_rect.x + tile_rect.width//2,
                                                tile_rect.y + tile_rect.height//2))
            self.screen.blit(key_text, key_rect)
            
            # Draw tile name
            name_text = self.small_font.render(tile["name"], True, WHITE)
            self.screen.blit(name_text, (tile_rect.x + tile_rect.width + 10, tile_rect.y + 5))
            
            palette_y += TILE_SIZE * 1.5 + 10
            
            # Check if we need a new column
            if palette_y > SCREEN_HEIGHT - 200 and i < len(TILE_INFO) - 1:
                panel_x += 150
                palette_y = 250 + 40
    
    def draw_toolbar(self):
        """Draw the toolbar at the top."""
        toolbar_rect = pygame.Rect(0, 0, SCREEN_WIDTH - UI_PANEL_WIDTH, 40)
        pygame.draw.rect(self.screen, (60, 60, 80), toolbar_rect)
        pygame.draw.rect(self.screen, LIGHT_GRAY, toolbar_rect, 1)
        
        # Draw buttons
        buttons = [
            ("New (N)", 20),
            ("Load (L)", 100),
            ("Save (S)", 180),
            ("Clear (C)", 260),
            ("Grid: ON" if self.show_grid else "Grid: OFF", 340),
            (f"Brush: {self.brush_size}", 440),
        ]
        
        for text, x in buttons:
            button_rect = pygame.Rect(x, 5, 80, 30)
            pygame.draw.rect(self.screen, (80, 80, 100), button_rect)
            pygame.draw.rect(self.screen, LIGHT_GRAY, button_rect, 1)
            
            button_text = self.small_font.render(text, True, WHITE)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
        
        # Draw mode indicator
        mode_text = self.small_font.render(f"Mode: {self.mode}", True, YELLOW)
        self.screen.blit(mode_text, (550, 12))
    
    def draw_status_bar(self):
        """Draw the status bar at the bottom."""
        status_y = GRID_HEIGHT * TILE_SIZE + 40
        status_rect = pygame.Rect(0, status_y, SCREEN_WIDTH - UI_PANEL_WIDTH, 30)
        pygame.draw.rect(self.screen, (60, 60, 80), status_rect)
        pygame.draw.rect(self.screen, LIGHT_GRAY, status_rect, 1)
        
        # Instructions
        instructions = [
            "Left Click: Place tile",
            "Right Click: Remove tile",
            "Number Keys: Select tile",
            "Mouse Wheel: Change brush size",
            "ESC: Exit"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(inst_text, (20 + i * 180, status_y + 5))
    
    def draw_help(self):
        """Draw help information."""
        help_y = GRID_HEIGHT * TILE_SIZE + 80
        help_rect = pygame.Rect(0, help_y, SCREEN_WIDTH - UI_PANEL_WIDTH, 100)
        pygame.draw.rect(self.screen, (40, 40, 50), help_rect)
        
        help_lines = [
            "Tile Types:",
            "  0: Grass (passable)",
            "  1: Brick Wall (destructible)",
            "  2: Steel Wall (indestructible)",
            "  3: Water (impassable)",
            "  4: Forest (passable, provides cover)",
            "  5: Ice (passable, slippery)",
            "  P: Player Spawn",
            "  E: Enemy Spawn",
            "  U: Power-up Spawn"
        ]
        
        for i, line in enumerate(help_lines):
            line_text = self.small_font.render(line, True, WHITE)
            self.screen.blit(line_text, (20, help_y + 5 + i * 20))
    
    def place_tile(self, x, y, tile_type):
        """Place a tile at the specified grid coordinates."""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            # Apply brush size
            for dy in range(self.brush_size):
                for dx in range(self.brush_size):
                    px = x + dx - self.brush_size // 2
                    py = y + dy - self.brush_size // 2
                    if 0 <= px < GRID_WIDTH and 0 <= py < GRID_HEIGHT:
                        # Special handling for spawn points
                        if tile_type == TileType.PLAYER_SPAWN.value:
                            # Only one player spawn allowed - remove existing player spawn
                            for cy in range(GRID_HEIGHT):
                                for cx in range(GRID_WIDTH):
                                    if self.map_data[cy][cx] == TileType.PLAYER_SPAWN.value:
                                        self.map_data[cy][cx] = TileType.GRASS.value
                        # Multiple enemy and power-up spawns are allowed
                        
                        self.map_data[py][px] = tile_type
                        self.dirty = True
    
    def remove_tile(self, x, y):
        """Remove tile (set to grass) at the specified grid coordinates."""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            for dy in range(self.brush_size):
                for dx in range(self.brush_size):
                    px = x + dx - self.brush_size // 2
                    py = y + dy - self.brush_size // 2
                    if 0 <= px < GRID_WIDTH and 0 <= py < GRID_HEIGHT:
                        self.map_data[py][px] = TileType.GRASS.value
                        self.dirty = True
    
    def save_map(self, filename=None):
        """Save the current map to a file."""
        if filename is None:
            # Create maps directory if it doesn't exist
            os.makedirs("maps", exist_ok=True)
            
            # Generate filename
            base_name = self.map_name
            if not base_name.endswith(".map"):
                base_name += ".map"
            filename = os.path.join("maps", base_name)
        
        try:
            # Save as simple text format
            with open(filename, 'w') as f:
                # Write header
                f.write(f"# Tank Battle Map: {self.map_name}\n")
                f.write(f"# Size: {GRID_WIDTH}x{GRID_HEIGHT}\n")
                f.write("# Format: Each character represents a tile\n")
                f.write("# 0=Grass, 1=Brick, 2=Steel, 3=Water, 4=Forest, 5=Ice\n")
                f.write("# P=PlayerSpawn, E=EnemySpawn, U=PowerUpSpawn\n")
                f.write("#\n")
                
                # Write map data
                for y in range(GRID_HEIGHT):
                    row = ''
                    for x in range(GRID_WIDTH):
                        tile_value = self.map_data[y][x]
                        tile_info = TILE_INFO[tile_value]
                        row += tile_info["key"]
                    f.write(row + '\n')
            
            self.dirty = False
            print(f"Map saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving map: {e}")
            return False
    
    def load_map(self, filename):
        """Load a map from a file."""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            # Parse map data
            map_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    map_lines.append(line)
            
            # Check size
            if len(map_lines) != GRID_HEIGHT:
                print(f"Warning: Map height {len(map_lines)} doesn't match expected {GRID_HEIGHT}")
                # Truncate or pad as needed
                while len(map_lines) < GRID_HEIGHT:
                    map_lines.append('0' * GRID_WIDTH)
                map_lines = map_lines[:GRID_HEIGHT]
            
            # Parse each line
            new_map_data = []
            for y in range(GRID_HEIGHT):
                if y < len(map_lines):
                    line = map_lines[y]
                    # Ensure line is correct width
                    if len(line) < GRID_WIDTH:
                        line = line + '0' * (GRID_WIDTH - len(line))
                    line = line[:GRID_WIDTH]
                else:
                    line = '0' * GRID_WIDTH
                
                row = []
                for x in range(GRID_WIDTH):
                    char = line[x] if x < len(line) else '0'
                    
                    # Convert character to tile value
                    tile_value = TileType.GRASS.value
                    for i, tile in enumerate(TILE_INFO):
                        if tile["key"] == char:
                            tile_value = i
                            break
                    
                    row.append(tile_value)
                new_map_data.append(row)
            
            self.map_data = new_map_data
            self.map_name = os.path.splitext(os.path.basename(filename))[0]
            self.dirty = False
            print(f"Map loaded from {filename}")
            return True
            
        except Exception as e:
            print(f"Error loading map: {e}")
            return False
    
    def clear_map(self):
        """Clear the entire map (set all tiles to grass)."""
        self.create_empty_map()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Tile selection with number keys
                elif event.key == pygame.K_0:
                    self.selected_tile = 0  # Grass
                elif event.key == pygame.K_1:
                    self.selected_tile = 1  # Brick
                elif event.key == pygame.K_2:
                    self.selected_tile = 2  # Steel
                elif event.key == pygame.K_3:
                    self.selected_tile = 3  # Water
                elif event.key == pygame.K_4:
                    self.selected_tile = 4  # Forest
                elif event.key == pygame.K_5:
                    self.selected_tile = 5  # Ice
                elif event.key == pygame.K_p:
                    self.selected_tile = 6  # Player Spawn
                elif event.key == pygame.K_e:
                    self.selected_tile = 7  # Enemy Spawn
                elif event.key == pygame.K_u:
                    self.selected_tile = 8  # Power-up Spawn
                
                # Editor commands
                elif event.key == pygame.K_n:
                    self.create_empty_map()
                    self.map_name = "untitled"
                elif event.key == pygame.K_l:
                    # Simple load dialog (in real app would use file dialog)
                    filename = "maps/level1.map"
                    if os.path.exists(filename):
                        self.load_map(filename)
                    else:
                        print("Default map not found. Save a map first.")
                elif event.key == pygame.K_s:
                    self.save_map()
                elif event.key == pygame.K_c:
                    self.clear_map()
                elif event.key == pygame.K_g:
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.brush_size = min(5, self.brush_size + 1)
                elif event.key == pygame.K_MINUS:
                    self.brush_size = max(1, self.brush_size - 1)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if click is in map area
                if (mouse_pos[0] < SCREEN_WIDTH - UI_PANEL_WIDTH and 
                    mouse_pos[1] < GRID_HEIGHT * TILE_SIZE + 40):
                    
                    map_x = (mouse_pos[0] - 20) // TILE_SIZE
                    map_y = (mouse_pos[1] - 40) // TILE_SIZE
                    
                    if 0 <= map_x < GRID_WIDTH and 0 <= map_y < GRID_HEIGHT:
                        if event.button == 1:  # Left click - place tile
                            self.place_tile(map_x, map_y, self.selected_tile)
                        elif event.button == 3:  # Right click - remove tile
                            self.remove_tile(map_x, map_y)
                
                # Check toolbar clicks
                elif mouse_pos[1] < 40:
                    # Toolbar button handling (simplified)
                    pass
            
            elif event.type == pygame.MOUSEWHEEL:
                # Change brush size with mouse wheel
                if event.y > 0:
                    self.brush_size = min(5, self.brush_size + 1)
                else:
                    self.brush_size = max(1, self.brush_size - 1)
    
    def update(self):
        """Update editor state."""
        # Continuous painting while mouse button is held
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        if mouse_buttons[0]:  # Left mouse button
            if (mouse_pos[0] < SCREEN_WIDTH - UI_PANEL_WIDTH and 
                mouse_pos[1] < GRID_HEIGHT * TILE_SIZE + 40):
                
                map_x = (mouse_pos[0] - 20) // TILE_SIZE
                map_y = (mouse_pos[1] - 40) // TILE_SIZE
                
                if 0 <= map_x < GRID_WIDTH and 0 <= map_y < GRID_HEIGHT:
                    self.place_tile(map_x, map_y, self.selected_tile)
        
        elif mouse_buttons[2]:  # Right mouse button
            if (mouse_pos[0] < SCREEN_WIDTH - UI_PANEL_WIDTH and 
                mouse_pos[1] < GRID_HEIGHT * TILE_SIZE + 40):
                
                map_x = (mouse_pos[0] - 20) // TILE_SIZE
                map_y = (mouse_pos[1] - 40) // TILE_SIZE
                
                if 0 <= map_x < GRID_WIDTH and 0 <= map_y < GRID_HEIGHT:
                    self.remove_tile(map_x, map_y)
    
    def draw(self):
        """Draw everything."""
        self.screen.fill(BLACK)
        
        self.draw_map()
        self.draw_toolbar()
        self.draw_status_bar()
        self.draw_help()
        self.draw_ui_panel()
        
        pygame.display.flip()
    
    def run(self):
        """Main editor loop."""
        print("Starting Tank Battle Map Editor...")
        print("Instructions:")
        print("  Left Click: Place selected tile")
        print("  Right Click: Remove tile (set to grass)")
        print("  Number Keys 0-5: Select terrain tiles")
        print("  P, E, U: Select spawn tiles (Player, Enemy, Power-up)")
        print("  N: New map, L: Load map, S: Save map, C: Clear map")
        print("  G: Toggle grid, +/-: Change brush size")
        print("  ESC: Exit editor")
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        # Ask to save if map is dirty
        if self.dirty:
            print("\nMap has unsaved changes!")
            save = input("Save before exiting? (y/n): ")
            if save.lower() == 'y':
                self.save_map()
        
        pygame.quit()
        sys.exit()

def main():
    editor = MapEditor()
    editor.run()

if __name__ == "__main__":
    main()