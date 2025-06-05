#!/bin/bash

# Start Ollama in the background
echo "Starting Ollama server..."
ollama serve &

# Wait for Ollama to start
echo "Waiting for Ollama to start..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "  Ollama not ready yet, waiting 3 seconds..."
    sleep 3
done

echo "Ollama is ready!"

# Start the RunPod handler directly
echo "Starting RunPod handler..."
python3 /app/src/handler.py