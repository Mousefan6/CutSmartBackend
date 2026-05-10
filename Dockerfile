# Use python 3.14 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server directory contents to /app
COPY server/ ./server/

# Expose the necessary ports
EXPOSE 5000

# Start the server
CMD ["python", "-m", "server.run"]
