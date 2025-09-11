FROM python:3.10-slim

# Install system dependencies needed for dlib and face_recognition
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Upgrade pip first
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install flask face_recognition

CMD ["python", "app.py"]
