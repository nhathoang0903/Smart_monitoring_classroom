import cv2
from ultralytics import YOLO
import requests
from datetime import datetime
import time

# Specify the path to the image directly in the code
image_path = 'image/test2.jpg'  

# Load the YOLO model for human detection
yolo_human_detect = YOLO('model/best.pt')  # Update this path to your model file

# Read the input image
img = cv2.imread(image_path)

# Check if the image is loaded properly
if img is None:
    print("Error: Unable to load the image. Check the path.")
    exit()

# Perform human detection
start_time = time.time()  # Start time for detection
results = yolo_human_detect.predict(source=img, conf=0.25)  # Adjust confidence as needed
end_time = time.time()  # End time for detection

# Initialize count of detected persons
person_count = 0

# Extract bounding boxes and labels from the detections
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()  # Get bounding box coordinates
        conf = box.conf[0]  # Get confidence score
        cls = box.cls[0]  # Get class ID
        if cls == 0:  # Check if the detected class is 'person' (usually class 0)
            person_count += 1  # Increment the person count
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Draw bounding box
            cv2.putText(img, f'Human {conf:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Save the processed image locally
output_image_path = 'output_detected_image.jpg'
cv2.imwrite(output_image_path, img)

# Display the output image (optional for headless systems)
# cv2.imshow('Human Detection', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Upload the image to Imgur
CLIENT_ID = '78c668ac8da2408'  # Your Imgur client ID
headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
with open(output_image_path, 'rb') as image_file:
    response = requests.post(
        'https://api.imgur.com/3/upload',
        headers=headers,
        files={'image': image_file}
    )

# Check if the upload was successful and get the image URL
if response.status_code == 200:
    image_url = response.json()['data']['link']
    print(f'Image uploaded successfully: {image_url}')
else:
    print(f'Failed to upload image. Status code: {response.status_code}')
    image_url = None  # Handle the case where the image wasn't uploaded

# Prepare data for API
timestamp = datetime.now().isoformat()  # Current timestamp
light_status = person_count > 0  # True if person_count > 0, False otherwise
ac_temperature = 20.0 + (0.5 * person_count)  # Adjust temperature based on people count

data = {
    "classroom_id": 2,  # Set to your classroom ID
    "classroom_name": "H108",  # Set to your classroom name
    "timestamp": timestamp,
    "people_count": person_count,
    "light_status": light_status,
    "ac_temperature": ac_temperature,
    "image_url": image_url  # URL of the processed image
}

# Send the data to the API
api_response = requests.post('http://172.26.24.142:3000/api/classroom_status/', json=data)

# Print the response status
if api_response.status_code == 200 or api_response.status_code == 201:
    print("Data successfully sent to the server.")
else:
    print(f"Failed to send data. Status code: {api_response.status_code}")
    print(api_response.text)