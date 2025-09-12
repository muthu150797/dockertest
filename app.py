from flask import Flask, request, jsonify
from ultralytics import YOLO
import os
import cv2

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask inside Docker on Render !"

@app.route('/getme')
def sayhi():
    return "HIIIII"

@app.route('/predictGlass')
def predictGlass():
    # Read query parameters
    image_path = request.args.get("image")
    model_path = request.args.get("model")
    output_image_path = request.args.get("output", "output.jpg")

    if not image_path or not model_path:
        return jsonify({"error": "Missing 'image' or 'model' query parameter"}), 400

    # Check if image exists
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    # Load YOLO model
    model = YOLO(model_path)

    # Run inference
    results = model(image_path, conf=0.7)
    img = cv2.imread(image_path)
    glasses_worn = False
    confi = 0.0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            class_name = model.names[cls]
            confi = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            if class_name.lower() == "with class":  # <-- replace with your trained class name
                glasses_worn = True
                color = (0, 255, 0)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f"{class_name} {confi:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            else:
                color = (0, 0, 255)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, f"{class_name} {confi:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Save output image
    #cv2.imwrite(output_image_path, img)

    # Return JSON response
    return jsonify({
        #"image": os.path.basename(image_path),
        "glasses_worn": glasses_worn,
        "confidence": confi,
        #"output_image": output_image_path
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
