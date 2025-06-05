FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    psmisc \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fSL https://ollama.com/install.sh | sh

# Start Ollama and download the model during build
RUN ollama serve & \
    sleep 10 && \
    ollama pull gemma3:12b-it-qat && \
    pkill ollama && \
    sleep 5

# Install Python packages
COPY requirements_runpod.txt /requirements_runpod.txt
RUN pip3 install --no-cache-dir -r /requirements_runpod.txt && \
    rm /requirements_runpod.txt

# Create app directory
WORKDIR /app

# Copy files
COPY model/ /app/src/
COPY start.sh /app/

# Make start script executable
RUN chmod +x /app/start.sh

# Set entrypoint
CMD ["/app/start.sh"]