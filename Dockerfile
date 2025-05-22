FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    psmisc \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama and download the model during build
RUN ollama serve & \
    sleep 10 && \
    ollama pull gemma-3-12b-it-q4_0 && \
    killall ollama

# Install Python packages
COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

# Create app directory
WORKDIR /app

# Copy files
COPY src/ /app/src/
COPY start.sh /app/

# Make start script executable
RUN chmod +x /app/start.sh

# Set entrypoint
CMD ["/app/start.sh"]