FROM --platform=linux/amd64 ubuntu:22.04

WORKDIR /app

# Install dependencies and clean up in one layer
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  wget \
  unzip \
  python3 \
  python3-pip \
  python3-venv \
  ca-certificates \
  dos2unix && \
  rm -rf /var/lib/apt/lists/*

# NOTE: Copy and update CA certificates (uncomment if needed for corporate environments)
# See README for instructions on adding custom certificates
# COPY <certfile> /usr/local/share/ca-certificates/
# RUN update-ca-certificates

# Setup Python virtual environment
RUN python3 -m venv .venv

# Install Python dependencies (cached unless requirements.txt changes)
COPY requirements.txt .
RUN dos2unix requirements.txt && \
  .venv/bin/pip install --no-cache-dir -r requirements.txt

# Download and extract AzureHound in one layer
RUN wget -q https://github.com/SpecterOps/AzureHound/releases/download/v2.4.1/AzureHound_v2.4.1_linux_amd64.zip && \
  unzip -q AzureHound_v2.4.1_linux_amd64.zip && \
  rm AzureHound_v2.4.1_linux_amd64.zip

# Copy application files and fix line endings
COPY ingestdata.py update.sh ./
RUN dos2unix ingestdata.py update.sh

CMD ["bash", "update.sh"]
