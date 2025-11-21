# Use an official Python image as the base
FROM python:3.12-slim

# Set environment variables to reduce Python bytecode and buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install OS dependencies and tools (including iproute2 for the 'ip' command)
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    git \
    jq \
    software-properties-common \
    apt-transport-https \
    bash-completion \
    vim \
    bash \
    iproute2 \
    libgconf-2-4 \
    libnss3 \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    ca-certificates \
    build-essential \    
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf aws awscliv2.zip

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && chmod +x kubectl \
    && mv kubectl /usr/local/bin/

# Install eksctl
RUN curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz" \
    | tar xz -C /tmp \
    && mv /tmp/eksctl /usr/local/bin/

# Add NodeSource repository and install Node.js & npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs && \
    npm install -g @testmo/testmo-cli

# Copy your Pytest framework into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Google Chrome and ChromeDriver
RUN curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | tee /etc/apt/trusted.gpg.d/google.asc && \
    echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/google.asc] http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable wget curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Expose a port for debugging (if needed)
EXPOSE 8080

# Start tests
RUN chmod 755 run_tests.sh

# Configure AWS CLI, eksctl, kubectl and run tests
# Setting the entrypoint to allow dynamic command args (test file name)
ENTRYPOINT ["./run_tests.sh"]

# Default command (if no arguments are passed)
CMD []
