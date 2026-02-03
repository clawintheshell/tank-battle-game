#!/bin/bash
# Tank Battle Game - Run Script with uv support

echo "========================================"
echo "   Tank Battle Game with Map Editor    "
echo "========================================"
echo ""
echo "Choose an option:"
echo "1. Run Game"
echo "2. Run Map Editor"
echo "3. Install Dependencies (using uv)"
echo "4. Test Game"
echo "5. Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "Starting Tank Battle Game..."
        echo "Controls: WASD/Arrows to move, Space to shoot, P to pause, ESC to quit"
        echo "Note: Running in headless mode (no audio available)"
        # Try uv run first, fall back to regular python
        if command -v uv &> /dev/null && [ -f "pyproject.toml" ]; then
            SDL_AUDIODRIVER=dummy uv run python game.py
        else
            SDL_AUDIODRIVER=dummy python3 game.py
        fi
        ;;
    2)
        echo "Starting Map Editor..."
        echo "Controls: Left-click to place tiles, Right-click to remove"
        echo "Number keys 0-5: Select terrain, P/E/U: Select spawn points"
        # Try uv run first, fall back to regular python
        if command -v uv &> /dev/null && [ -f "pyproject.toml" ]; then
            SDL_AUDIODRIVER=dummy uv run python map_editor.py
        else
            SDL_AUDIODRIVER=dummy python3 map_editor.py
        fi
        ;;
    3)
        echo "Installing dependencies..."
        # Check if uv is available
        if command -v uv &> /dev/null; then
            echo "Using uv for dependency management..."
            uv sync
            if [ $? -eq 0 ]; then
                echo "✅ Dependencies installed successfully with uv!"
                echo "Virtual environment created at: .venv/"
            else
                echo "❌ Failed to install dependencies with uv."
            fi
        else
            echo "uv not found. Installing with pip..."
            echo "Note: For best results, install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
            pip install pygame numpy
            if [ $? -eq 0 ]; then
                echo "Dependencies installed successfully with pip!"
            else
                echo "Failed to install dependencies. Trying alternative..."
                sudo apt-get install python3-pygame python3-numpy
            fi
        fi
        ;;
    4)
        echo "Running game test..."
        # Try uv run first, fall back to regular python
        if command -v uv &> /dev/null && [ -f "pyproject.toml" ]; then
            uv run python test_game.py
        else
            python3 test_game.py
        fi
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