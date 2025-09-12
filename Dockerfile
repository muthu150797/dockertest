FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install flask
RUN pip install ultralytics
CMD ["python", "app.py"]
