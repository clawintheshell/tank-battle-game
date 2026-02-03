# 🎮 Tank Battle Game with Map Editor

A classic Tank Battle game with an integrated map editor, built in Python using Pygame.

## 🚀 Features

### 🎯 Game Features
- **Player Tank**: Control a tank with keyboard (WASD/Arrow keys)
- **Enemy Tanks**: AI-controlled enemy tanks with basic pathfinding
- **Obstacles**: Destructible and indestructible walls
- **Power-ups**: Health packs, speed boosts, and weapon upgrades
- **Multiple Levels**: Progress through increasingly difficult levels
- **Score System**: Earn points for destroying enemies and completing levels

### 🗺️ Map Editor Features
- **Tile-based Editing**: Place different tile types (grass, walls, water, etc.)
- **Save/Load Maps**: Save custom maps and load them in the game
- **Multiple Layers**: Edit terrain, objects, and spawn points separately
- **Intuitive UI**: Simple mouse-based interface with tool palette

## 🛠️ Installation

This project uses [`uv`](https://github.com/astral-sh/uv) for fast, reliable dependency management.

### Prerequisites
- **Python 3.12 or higher** (automatically installed by `uv`)
- **`uv`** - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Quick Start with `uv`
```bash
# Clone the repository
git clone https://github.com/clawintheshell/tank-battle-game
cd tank-battle-game

# Install dependencies and create virtual environment
uv sync

# Run the game
python game.py

# Or run the map editor
python map_editor.py
```

### Manual Installation (without `uv`)
```bash
pip install pygame numpy
```

## 🔧 Development with `uv`

This project is configured with `uv` for reproducible development environments.

### Project Structure for `uv`
```
tank-battle-game/
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Locked dependency versions (crucial!)
├── .python-version   # Python version specification
├── .gitignore        # Excludes .venv/, .uv/, __pycache__/
└── .venv/            # Virtual environment (created by `uv sync`)
```

### Key `uv` Commands
```bash
# Install dependencies and create virtual environment
uv sync

# Update dependencies
uv sync --upgrade

# Add a new dependency
uv add package-name

# Run the game from the virtual environment
uv run python game.py

# Run tests
uv run pytest
```

### For Contributors
1. Clone the repository
2. Run `uv sync` to get the exact same environment
3. The `uv.lock` file ensures everyone uses the same dependency versions

Or on Ubuntu/Debian:
```bash
sudo apt-get install python3-pygame
```

### Run the Game
```bash
python3 game.py
```

### Run the Map Editor
```bash
python3 map_editor.py
```

## 🎮 How to Play

### Game Controls
- **Arrow Keys/WASD**: Move tank
- **Spacebar**: Shoot
- **P**: Pause game
- **M**: Toggle music
- **ESC**: Exit game
- **R**: Restart level

### Map Editor Controls
- **Left Click**: Place selected tile
- **Right Click**: Remove tile
- **Number Keys 1-9**: Select tile type
- **S**: Save map
- **L**: Load map
- **C**: Clear map
- **ESC**: Exit editor

## 📁 Project Structure

```
tank-battle-game/
├── game.py              # Main game logic
├── map_editor.py        # Map editor application
├── assets/              # Game assets (images, sounds)
│   ├── tanks/          # Tank sprites
│   ├── tiles/          # Tile images
│   ├── ui/             # UI elements
│   └── sounds/         # Sound effects and music
├── maps/               # Game maps
│   ├── level1.map     # Level 1 map
│   ├── level2.map     # Level 2 map
│   └── custom/        # User-created maps
├── utils/              # Utility modules
│   ├── tank.py        # Tank class
│   ├── enemy.py       # Enemy AI
│   ├── bullet.py      # Bullet physics
│   └── map_loader.py  # Map loading/saving
└── README.md          # This file
```

## 🎨 Tile Types

1. **Grass** (0): Passable terrain
2. **Brick Wall** (1): Destructible wall
3. **Steel Wall** (2): Indestructible wall
4. **Water** (3): Impassable (slows movement)
5. **Forest** (4): Provides cover (tanks hidden)
6. **Ice** (5): Slippery surface (reduced control)
7. **Player Spawn** (P): Player starting position
8. **Enemy Spawn** (E): Enemy starting positions
9. **Power-up Spawn** (U): Power-up locations

## 🎯 Game Rules

1. **Objective**: Destroy all enemy tanks while protecting your base
2. **Lives**: Player has 3 lives
3. **Score**: 
   - Destroy enemy tank: 100 points
   - Destroy brick wall: 10 points
   - Collect power-up: 50 points
   - Complete level: 500 points
4. **Power-ups**:
   - **Health**: Restore 50% health
   - **Speed**: Increase movement speed for 10 seconds
   - **Shield**: Temporary invincibility for 5 seconds
   - **Rapid Fire**: Faster shooting for 8 seconds

## 🗺️ Map Format

Maps are stored as text files with the following format:
- Each character represents a tile
- Numbers 0-9: Terrain tiles
- Letters: Special tiles (P=Player, E=Enemy, U=Power-up)
- Map size: 20x20 tiles (customizable)

Example map line: `11111111111111111111`

## 🚀 Development

### Adding New Features
1. **New Tile Types**: Add to `TILE_TYPES` in `map_editor.py`
2. **New Power-ups**: Extend `PowerUp` class in `game.py`
3. **New Enemy Types**: Create new class inheriting from `EnemyTank`

### Testing
```bash
# Run game tests
python3 -m pytest tests/

# Run specific test
python3 -m pytest tests/test_tank.py
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Credits

Created by **MegaPonzuClaw AI buddy**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Issues

Found a bug? Have a feature request? Please open an issue on GitHub.

## 🌟 Show Your Support

Give a ⭐️ if you like this project!

---

**Happy tank battling!** 🎮🚀