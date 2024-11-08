import cv2
from ultralytics import YOLO
import os

# YOLO model path
model_path = os.path.join("..", "model", "best.pt")
yolo_human_detect = YOLO(model_path)

def detect_people(image):
    results = yolo_human_detect.predict(source=image, conf=0.25)
    person_count = 0

    # Count people and draw rectangles around detected humans
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0]
            cls = box.cls[0]
            if cls == 0:  # Check if the detected class is 'person'
                person_count += 1
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2, y2)), (0, 255, 0), 2)
                cv2.putText(image, f'Human {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return person_count, image
