#!/bin/bash
# Tank Battle Game - Run Script

echo "========================================"
echo "   Tank Battle Game with Map Editor    "
echo "========================================"
echo ""
echo "Choose an option:"
echo "1. Run Game"
echo "2. Run Map Editor"
echo "3. Install Dependencies"
echo "4. Test Game"
echo "5. Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "Starting Tank Battle Game..."
        echo "Controls: WASD/Arrows to move, Space to shoot, P to pause, ESC to quit"
        python3 game.py
        ;;
    2)
        echo "Starting Map Editor..."
        echo "Controls: Left-click to place tiles, Right-click to remove"
        echo "Number keys 0-5: Select terrain, P/E/U: Select spawn points"
        python3 map_editor.py
        ;;
    3)
        echo "Installing dependencies..."
        pip install pygame
        if [ $? -eq 0 ]; then
            echo "Dependencies installed successfully!"
        else
            echo "Failed to install dependencies. Trying alternative..."
            sudo apt-get install python3-pygame
        fi
        ;;
    4)
        echo "Running game test..."
        python3 test_game.py
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run again."
        exit 1
        ;;
esac