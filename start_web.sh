#!/bin/bash

# Get project root
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"

# Function to kill processes on exit
cleanup() {
    echo "Stopping Zeta..."
    kill $BACKEND_PID 2>/dev/null
    exit
}
trap cleanup SIGINT

echo "🚀 Starting Zeta Web UI..."

# 1. Start Backend
echo "Starting Backend (FastAPI)..."
cd "$PROJECT_DIR"
"$VENV_PYTHON" zeta/server/api.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# 2. Start Frontend
echo "Starting Frontend (Vite)..."
cd "$PROJECT_DIR/zeta/web_ui"

# Check if node_modules exists, if not install handling errors
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Run dev server
npm run dev

# Wait for backend process
wait $BACKEND_PID
