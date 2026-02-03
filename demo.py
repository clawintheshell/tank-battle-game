#!/usr/bin/env python3
"""
Tank Battle Game Demo
This script demonstrates the features of the Tank Battle game.
"""

import os
import sys

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def demo_features():
    """Demonstrate game features."""
    print_header("Tank Battle Game - Feature Demo")
    
    print("\n🎮 GAME FEATURES:")
    print("  • Player tank with full movement controls (WASD/Arrow keys)")
    print("  • Enemy tanks with AI pathfinding and shooting")
    print("  • Destructible brick walls and indestructible steel walls")
    print("  • Multiple terrain types: Grass, Water, Forest, Ice")
    print("  • Power-up system: Health, Speed, Shield")
    print("  • Score system with points for kills and level completion")
    print("  • Multiple lives and level progression")
    print("  • Pause menu and game state management")
    
    print("\n🗺️ MAP EDITOR FEATURES:")
    print("  • Tile-based map editing with 9 tile types")
    print("  • Brush size adjustment (1x1 to 5x5)")
    print("  • Save/Load functionality for custom maps")
    print("  • Grid toggle for precise editing")
    print("  • Intuitive UI with tool palette")
    print("  • Support for Player, Enemy, and Power-up spawn points")
    
    print("\n📁 PROJECT STRUCTURE:")
    for root, dirs, files in os.walk("."):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        level = root.count(os.sep) - 1
        indent = "  " * level
        if level == 0:
            print(f"{indent}📦 tank-battle-game/")
        else:
            print(f"{indent}📁 {os.path.basename(root)}/")
        
        subindent = "  " * (level + 1)
        for file in files:
            if not file.startswith('.') and file not in ['demo.py', 'test_game.py']:
                # Add icons based on file type
                if file.endswith('.py'):
                    icon = "🐍"
                elif file.endswith('.map'):
                    icon = "🗺️"
                elif file.endswith('.md'):
                    icon = "📝"
                elif file.endswith('.sh'):
                    icon = "⚡"
                else:
                    icon = "📄"
                print(f"{subindent}{icon} {file}")
    
    print("\n🚀 GETTING STARTED:")
    print("  1. Install dependencies: pip install pygame")
    print("  2. Run the game: python3 game.py")
    print("  3. Or use the run script: ./run.sh")
    print("  4. Create custom maps with: python3 map_editor.py")
    
    print("\n🎯 CONTROLS:")
    print("  Game Controls:")
    print("    • WASD or Arrow Keys: Move tank")
    print("    • Spacebar: Shoot")
    print("    • P: Pause/Resume game")
    print("    • ESC: Quit game")
    print("    • R: Restart (when game over)")
    
    print("\n  Map Editor Controls:")
    print("    • Left Click: Place selected tile")
    print("    • Right Click: Remove tile (set to grass)")
    print("    • Number Keys 0-5: Select terrain tiles")
    print("    • P, E, U: Select spawn tiles (Player, Enemy, Power-up)")
    print("    • N: New map, L: Load map, S: Save map")
    print("    • C: Clear map, G: Toggle grid")
    print("    • +/-: Change brush size, ESC: Exit editor")
    
    print("\n🏆 GAME RULES:")
    print("  • Objective: Destroy all enemy tanks")
    print("  • Score Points:")
    print("    - Destroy enemy tank: 100 points")
    print("    - Destroy brick wall: 10 points")
    print("    - Collect power-up: 50 points")
    print("    - Complete level: 500 points")
    print("  • Lives: Start with 3 lives")
    print("  • Power-ups provide temporary advantages")

def check_dependencies():
    """Check if required dependencies are installed."""
    print_header("Dependency Check")
    
    try:
        import pygame
        print(f"✅ Pygame {pygame.version.ver} is installed")
        return True
    except ImportError:
        print("❌ Pygame is not installed")
        print("   Install with: pip install pygame")
        return False

def main():
    """Main demo function."""
    print_header("Tank Battle Game with Map Editor")
    print("Created by MegaPonzuClaw AI buddy")
    print("GitHub: https://github.com/clawintheshell/tank-battle-game")
    
    # Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install dependencies before running the game.")
        return
    
    # Show features
    demo_features()
    
    # Show sample map
    print_header("Sample Map Preview")
    print("Level 1 Map (from maps/level1.map):")
    print("""
    11111111111111111111
    1P000000000000000001
    10001110001110000001
    10000000000000000001
    10000000000000000001
    10000033333000000001
    10000033333000000001
    10000033333000000001
    10000000000000000001
    10000000000000000001
    1000444444444400001
    1000000000000000E001
    10000000000000000001
    10000000000000000001
    11111111111111111111
    """)
    print("Legend: 1=Brick Wall, 0=Grass, 3=Water, 4=Forest")
    print("        P=Player Spawn, E=Enemy Spawn")
    
    print_header("Ready to Play!")
    print("Run './run.sh' to start the game or map editor.")
    print("Or run 'python3 game.py' to start the game directly.")
    
    # Ask if user wants to run a quick test
    response = input("\nRun quick test? (y/n): ")
    if response.lower() == 'y':
        os.system("python3 test_game.py")

if __name__ == "__main__":
    main()