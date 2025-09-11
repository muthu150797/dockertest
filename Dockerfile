FROM ageitgey/face_recognition

WORKDIR /app
COPY . .

RUN pip install flask

CMD ["python", "app.py"]
