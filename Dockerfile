# Use lightweight Python base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for cv2 + Ultralytics)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy your application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir ultralytics opencv-python-headless flask

# Expose port (for Flask or FastAPI app)
EXPOSE 5000

# Run app
CMD ["python", "app.py"]
