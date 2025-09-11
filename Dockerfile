FROM python:3.10-slim

# Install minimal system dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip

# Install prebuilt dlib (latest version) + face_recognition + flask
RUN pip install dlib-bin==19.24.6
RUN pip install face_recognition flask

CMD ["python", "app.py"]
