import cv2
from ultralytics import YOLO
import os

# Define the path to the YOLO model file (best.pt) located in the "model" folder one level up
model_path = os.path.join("..", "model", "best.pt")
# Load the YOLO model for human detection
yolo_human_detect = YOLO(model_path)

# Function to detect people in an image
def detect_people(image):
    # Run YOLO model prediction on the input image with a confidence threshold of 0.25
    results = yolo_human_detect.predict(source=image, conf=0.25)
    person_count = 0  # Initialize count of detected persons

    # Loop through the prediction results to process detected boxes
    for result in results:
        for box in result.boxes:
            # Get coordinates of the bounding box (top-left and bottom-right corners)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            # Extract the confidence score and class of the detected object
            conf = box.conf[0]
            cls = box.cls[0]

            # Check if the detected class is 'person' (typically class index 0 in human detection models)
            if cls == 0:
                person_count += 1  # Increment person count
                # Draw a rectangle around the detected person
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (200, 200, 155), 2)
                # Annotate the bounding box with the confidence level
                cv2.putText(image, f'Human {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 155), 2)
    
    # Return the number of detected people and the annotated image
    return person_count, image
