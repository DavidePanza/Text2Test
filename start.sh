#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start
echo "Waiting for Ollama to start..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 3
done

# Start FastAPI in the background
echo "Starting FastAPI server..."
cd /app
uvicorn src.app:app --host 0.0.0.0 --port 8000 &

# Wait for FastAPI to start
echo "Waiting for FastAPI to start..."
while ! curl -s http://localhost:8000/health > /dev/null; do
    sleep 3
done

# Start the handler
echo "Starting RunPod handler..."
python3 /app/src/handler.py