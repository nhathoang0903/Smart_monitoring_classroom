import cv2
from ultralytics import YOLO
import requests
from datetime import datetime
import time
import os
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
image_path = 'test3.jpg'  # Replace with your image path
yolo_human_detect = YOLO('best.pt')  # Update this path to your model file

# Imgur API client ID
CLIENT_ID = '78c668ac8da2408'

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
        start_time = time.time()
        results = yolo_human_detect.predict(source=img, conf=0.25)
        end_time = time.time()
        
        # Count the number of detected persons
        person_count = 0
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                conf = box.conf[0]
                cls = box.cls[0]
                if cls == 0:  # If the detected class is 'person'
                    person_count += 1
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(img, f'Human {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save and optionally display the processed image
        output_image_path = 'output_detected_image.jpg'
        cv2.imwrite(output_image_path, img)

        # Upload image to Imgur
        headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
        with open(output_image_path, 'rb') as image_file:
            response = requests.post(
                'https://api.imgur.com/3/upload',
                headers=headers,
                files={'image': image_file}
            )

        # Get the image URL if uploaded successfully
        image_url = response.json()['data']['link'] if response.status_code == 200 else None
        if image_url:
            print(f'Image uploaded successfully: {image_url}')
        else:
            print(f"Failed to upload image. Status code: {response.status_code}")

        # Prepare data for the API
        timestamp = datetime.now().isoformat()
        light_status = person_count > 0
        ac_temperature = 20.0 + (0.5 * person_count)

        data = {
            "classroom_id": 2,
            "classroom_name": "H108",
            "timestamp": timestamp,
            "people_count": person_count,
            "light_status": light_status,
            "ac_temperature": ac_temperature,
            "image_url": image_url
        }

        # Send data to the server
        api_response = requests.post('http://172.26.24.142:3000/api/classroom_status/', json=data)
        if api_response.status_code in (200, 201):
            print("Data successfully sent to the server.")
        else:
            print(f"Failed to send data. Status code: {api_response.status_code}")
            print(api_response.text)

        # Control GPIO based on person count
        control_gpio(person_count)

        # Wait for the next detection cycle
        time.sleep(30)  # Adjust the delay as needed

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
