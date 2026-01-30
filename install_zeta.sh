#!/bin/bash

# Get the directory where this script is located (project root)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
MAIN_SCRIPT="$PROJECT_DIR/main.py"

echo " Installing Zeta..."
echo " Project Directory: $PROJECT_DIR"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found. Please run 'python3 -m venv .venv' first."
    exit 1
fi

# Define the alias command
ALIAS_CMD="alias zeta=\"'$VENV_PYTHON' '$MAIN_SCRIPT'\""

# Detect shell
SHELL_CONFIG=""
if [[ "$SHELL" == */zsh ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [[ "$SHELL" == */bash ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "⚠️ Unknown shell. You may need to add the alias manually."
fi

# Add alias if config file exists
if [ -n "$SHELL_CONFIG" ] && [ -f "$SHELL_CONFIG" ]; then
    if grep -q "alias zeta=" "$SHELL_CONFIG"; then
        echo "ℹ️  'zeta' alias already found in $SHELL_CONFIG"
    else
        echo "" >> "$SHELL_CONFIG"
        echo "# Zeta AI Agent" >> "$SHELL_CONFIG"
        echo "$ALIAS_CMD" >> "$SHELL_CONFIG"
        echo "✅ Added 'zeta' alias to $SHELL_CONFIG"
        echo "👉 Please run: source $SHELL_CONFIG"
    fi
else
    echo "ℹ️  Could not automatically edit run-com file."
    echo "👉 Please add this line to your shell config manually:"
    echo "   $ALIAS_CMD"
fi

echo " Installation Complete!"
echo "You can now run 'zeta start' from anywhere (after reloading shell)."
