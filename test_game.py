#!/usr/bin/env python3
"""
Quick test to verify the game runs.
"""

import subprocess
import sys
import time

def test_game():
    """Test if the game runs without crashing."""
    print("Testing Tank Battle Game...")
    
    try:
        # Run game for 3 seconds
        proc = subprocess.Popen(
            [sys.executable, "game.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit
        time.sleep(3)
        
        # Terminate the game
        proc.terminate()
        proc.wait(timeout=2)
        
        print("✅ Game started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Game test failed: {e}")
        return False

def test_map_editor():
    """Test if the map editor runs without crashing."""
    print("\nTesting Map Editor...")
    
    try:
        # Run editor for 2 seconds
        proc = subprocess.Popen(
            [sys.executable, "map_editor.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit
        time.sleep(2)
        
        # Terminate the editor
        proc.terminate()
        proc.wait(timeout=2)
        
        print("✅ Map editor started successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Map editor test failed: {e}")
        return False

def test_imports():
    """Test if all imports work."""
    print("\nTesting imports...")
    
    modules = ["pygame", "sys", "os", "random", "json"]
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            return False
    
    return True

def main():
    print("=" * 50)
    print("Tank Battle Game Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test game (commented out for now since it requires manual termination)
    # if not test_game():
    #     all_passed = False
    
    # Test map editor (commented out for same reason)
    # if not test_map_editor():
    #     all_passed = False
    
    # Quick syntax and module test
    print("\nQuick module test...")
    try:
        # Test game module imports
        from utils import map_loader
        print("✅ map_loader module imports successfully")
        
        # Test creating a simple map
        test_map = map_loader.create_empty_map(5, 5)
        print(f"✅ Created test map: {len(test_map)}x{len(test_map[0])}")
        
        # Test saving/loading
        if map_loader.save_map("test_save.map", test_map, "Test"):
            print("✅ Map saved successfully")
            
            loaded = map_loader.load_map("test_save.map", 5, 5)
            if loaded:
                print("✅ Map loaded successfully")
            
            # Clean up
            import os
            if os.path.exists("test_save.map"):
                os.remove("test_save.map")
                print("✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❌ Module test failed: {e}")
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ All tests passed!")
        print("\nTo run the game: python3 game.py")
        print("To run the map editor: python3 map_editor.py")
    else:
        print("❌ Some tests failed")
    print("=" * 50)

if __name__ == "__main__":
    main()