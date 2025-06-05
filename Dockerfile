FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Split into separate layers
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    psmisc \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama and download the model during build
RUN ollama serve & \
    sleep 15 && \
    ollama pull gemma3:12b-it-qat && \
    pkill ollama && \
    sleep 5

# Install Python packages
COPY requirements_runpod.txt /tmp/requirements_runpod.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements_runpod.txt && \
    rm /tmp/requirements_runpod.txt && \
    pip3 cache purge

# Create app directory
WORKDIR /app

# Copy files
COPY model/ src/
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Set entrypoint
CMD ["./start.sh"]