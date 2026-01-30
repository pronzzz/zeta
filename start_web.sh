#!/bin/bash
echo "Starting Zeta..."

# Start Backend in background
python3 zeta/server/api.py &
BACKEND_PID=$!

# Start Frontend
cd zeta/web_ui
npm run dev

# Cleanup
kill $BACKEND_PID
