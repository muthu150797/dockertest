FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install face_recognition

CMD ["python", "app.py"]
