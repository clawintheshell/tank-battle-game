"""
Map loader utility for Tank Battle game.
Handles loading and saving map files.
"""

import os
from enum import Enum

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

# Tile character mapping
TILE_CHARS = {
    '0': TileType.GRASS,
    '1': TileType.BRICK,
    '2': TileType.STEEL,
    '3': TileType.WATER,
    '4': TileType.FOREST,
    '5': TileType.ICE,
    'P': TileType.PLAYER_SPAWN,
    'E': TileType.ENEMY_SPAWN,
    'U': TileType.POWERUP_SPAWN,
}

# Reverse mapping
CHAR_TILES = {tile.value: char for char, tile in TILE_CHARS.items()}

def load_map(filename, width=20, height=15):
    """
    Load a map from a text file.
    
    Args:
        filename: Path to map file
        width: Expected map width
        height: Expected map height
        
    Returns:
        List of lists containing tile values, or None if error
    """
    if not os.path.exists(filename):
        print(f"Map file not found: {filename}")
        return None
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Filter out comment lines and empty lines
        map_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                map_lines.append(line)
        
        # Validate map size
        if len(map_lines) != height:
            print(f"Warning: Map height {len(map_lines)} doesn't match expected {height}")
            # Pad or truncate as needed
            while len(map_lines) < height:
                map_lines.append('0' * width)
            map_lines = map_lines[:height]
        
        # Parse map data
        map_data = []
        for y in range(height):
            if y < len(map_lines):
                line = map_lines[y]
                # Ensure line is correct width
                if len(line) < width:
                    line = line + '0' * (width - len(line))
                line = line[:width]
            else:
                line = '0' * width
            
            row = []
            for x in range(width):
                char = line[x] if x < len(line) else '0'
                tile_type = TILE_CHARS.get(char, TileType.GRASS)
                row.append(tile_type.value)
            
            map_data.append(row)
        
        print(f"Map loaded from {filename}")
        return map_data
        
    except Exception as e:
        print(f"Error loading map {filename}: {e}")
        return None

def save_map(filename, map_data, map_name="Untitled"):
    """
    Save a map to a text file.
    
    Args:
        filename: Path to save map file
        map_data: List of lists containing tile values
        map_name: Name of the map for header
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        height = len(map_data)
        width = len(map_data[0]) if height > 0 else 0
        
        with open(filename, 'w') as f:
            # Write header
            f.write(f"# Tank Battle Map: {map_name}\n")
            f.write(f"# Size: {width}x{height}\n")
            f.write("# Format: Each character represents a tile\n")
            f.write("# 0=Grass, 1=Brick, 2=Steel, 3=Water, 4=Forest, 5=Ice\n")
            f.write("# P=PlayerSpawn, E=EnemySpawn, U=PowerUpSpawn\n")
            f.write("#\n")
            
            # Write map data
            for y in range(height):
                row = ''
                for x in range(width):
                    tile_value = map_data[y][x]
                    char = CHAR_TILES.get(tile_value, '0')
                    row += char
                f.write(row + '\n')
        
        print(f"Map saved to {filename}")
        return True
        
    except Exception as e:
        print(f"Error saving map {filename}: {e}")
        return False

def create_empty_map(width=20, height=15):
    """Create an empty map filled with grass."""
    return [[TileType.GRASS.value for _ in range(width)] for _ in range(height)]

def print_map(map_data):
    """Print map to console for debugging."""
    if not map_data:
        print("Empty map data")
        return
    
    height = len(map_data)
    width = len(map_data[0]) if height > 0 else 0
    
    print(f"Map size: {width}x{height}")
    for y in range(height):
        row = ''
        for x in range(width):
            tile_value = map_data[y][x]
            char = CHAR_TILES.get(tile_value, '?')
            row += char
        print(row)

# Test function
if __name__ == "__main__":
    print("Testing map_loader module...")
    
    # Create test map
    test_map = create_empty_map(10, 8)
    test_map[4][4] = TileType.PLAYER_SPAWN.value
    test_map[2][2] = TileType.ENEMY_SPAWN.value
    test_map[6][6] = TileType.BRICK.value
    
    print("Test map:")
    print_map(test_map)
    
    # Save test map
    save_map("test_map.map", test_map, "Test Map")
    
    # Load test map
    loaded_map = load_map("test_map.map", 10, 8)
    
    if loaded_map:
        print("\nLoaded map:")
        print_map(loaded_map)
        
        # Clean up
        import os
        if os.path.exists("test_map.map"):
            os.remove("test_map.map")
            print("\nTest file cleaned up")