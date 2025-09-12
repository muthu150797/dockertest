# Use lightweight Python base
FROM python:3.10-slim

WORKDIR /app

# Install system deps (needed for cv2 & ultralytics)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (so Docker caches deps if unchanged)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Now copy your app code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
