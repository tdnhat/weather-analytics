FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory and all parent directories if they don't exist
RUN mkdir -p /app/weather_data_ingestion

# Set full permissions (read/write/execute) for all users
RUN chmod 777 /app/weather_data_ingestion

# Switch to a non-root user
USER 1000:1000

# Copy the rest of the application
COPY . .

# Command to run the script
CMD ["python", "main.py"]