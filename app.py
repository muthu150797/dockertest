from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# Load YOLO model ONCE at startup for speed
MODEL_PATH = "best.pt"  # replace with your trained model path
model = YOLO(MODEL_PATH)

@app.route('/')
def hello():
    return "Hello from Flask!"

@app.route("/predictGlass", methods=["POST"])
def predictGlass():
    return jsonify({"message": "predictGlass api called "}), 400
    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    # Read uploaded file
    file = request.files["file"]
    img_bytes = file.read()

    # Convert to OpenCV image
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"message": "Failed to read image"}), 400

    # Run YOLO inference
    results = model(img, conf=0.7)

    glasses_worn = False
    detections = []

    # Draw boxes and store detection info
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            class_name = model.names[cls]
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Decide box color
            color = (0, 255, 0) if class_name.lower() == "with class" else (0, 0, 255)
            if class_name.lower() == "with class":
                glasses_worn = True

            # Draw rectangle and label
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, f"{class_name} {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # Save detection info
            detections.append({
                "class": class_name,
                "confidence": confidence,
                "bbox": [x1, y1, x2, y2]
            })

    # Optionally, encode image to return as base64 (for React to show)
    # _, buffer = cv2.imencode('.jpg', img)
    # img_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        "glasses_worn": glasses_worn,
        "detections": detections,
        "message":"detect glass api"
        # "image": img_base64  # uncomment if you want image in response
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
