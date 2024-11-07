import cv2
from ultralytics import YOLO
import time
import RPi.GPIO as GPIO

# GPIO pin definitions
fanPin = 26  # Pin to control Fan
ledPin = 17  # Pin to control LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(fanPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

# Human detection threshold to activate the fan and LED
person_count_threshold = 1  # Number of people required to activate fan and LED

# YOLO model path and image path
image_path = 'test5.jpg'  # Replace with your image path
yolo_human_detect = YOLO('best.pt')  # Update this path to your model file

# Function to control fan and LED based on person count
def control_gpio(person_count):
    if person_count >= person_count_threshold:
        GPIO.output(fanPin, GPIO.HIGH)
        GPIO.output(ledPin, GPIO.HIGH)
        print("Human detected, Fan and LED ON")
    else:
        GPIO.output(fanPin, GPIO.LOW)
        GPIO.output(ledPin, GPIO.LOW)
        print("No human detected, Fan and LED OFF")

try:
    while True:
        # Load and check the input image
        img = cv2.imread(image_path)
        if img is None:
            print("Error: Unable to load the image. Check the path.")
            break

        # Perform human detection
        results = yolo_human_detect.predict(source=img, conf=0.25)
        
        # Count the number of detected persons
        person_count = 0
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls = box.cls[0]
                if cls == 0:  # If the detected class is 'person'
                    person_count += 1
                    # Draw bounding boxes on detected persons (optional)
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(img, 'Human', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Control GPIO based on person count
        control_gpio(person_count)

        # Wait for the next detection cycle
        time.sleep(30)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
