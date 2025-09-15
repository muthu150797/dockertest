from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Load YOLO model ONCE at startup for speed
MODEL_PATH = "best.pt"  # replace with your trained model path
model = YOLO(MODEL_PATH)

@app.route('/')
def hello():
    return "Hello from Flask!"

@app.route("/predictGlass", methods=["POST"])
def predictGlass():
    try:
        print("Request received at /predictGlass")
        if "file" not in request.files:
            return jsonify({"message": "No file uploaded"}), 400

        file = request.files["file"]
        print("Uploaded filename:", file.filename)
        img_bytes = file.read()

        # Convert to OpenCV image
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            print("Failed to decode image")
            return jsonify({"message": "Failed to read image"}), 400

        # Run YOLO
        print("Running YOLO inference...")
        results = model(img, conf=0.7)

        glasses_worn = False
        detections = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                class_name = model.names[cls]
                confidence = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if class_name.lower() == "with class":
                    glasses_worn = True

                detections.append({
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })

        print("Detection complete",detections)
        return jsonify({
            "glasses_worn": glasses_worn,
            "detections": detections,
            "message": "Detection complete00"
        })

    except Exception as e:
        import traceback
        print("ERROR:", str(e))
        traceback.print_exc()
        return jsonify({"message": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
