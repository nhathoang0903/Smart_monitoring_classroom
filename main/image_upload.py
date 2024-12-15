import requests
from datetime import datetime
import cv2

# Imgur API client ID for authorization
CLIENT_ID = '...'
# URL of the server endpoint to upload classroom status data
UPLOAD_URL = '...'

# Function to upload data to the server
def upload_to_server(image, person_count):
    # Save the current frame (image) to a file
    output_image_path = 'output_detected_image.jpg'
    cv2.imwrite(output_image_path, image)

    # Upload image to Imgur
    headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
    with open(output_image_path, 'rb') as image_file:
        # Make a POST request to Imgur API with the saved image
        response = requests.post('https://api.imgur.com/3/upload', headers=headers, files={'image': image_file})

    # Prepare data to be sent to the server
    timestamp = datetime.now().isoformat()  # Get current time in ISO format
    light_status = person_count > 0         # Set light status based on person count
    ac_temperature = 20.0 + (0.5 * person_count)  # Adjust AC temperature based on number of people
    image_url = response.json()['data']['link'] if response.status_code == 200 else None  # Get image URL if upload succeeded

    # Data payload to send to the server
    data = {
        "classroom_id": 2,
        "classroom_name": "H108",
        "timestamp": timestamp,
        "people_count": person_count,
        "light_status": light_status,
        "ac_temperature": ac_temperature,
        "image_url": image_url
    }

    # Send the data payload to the server API
    api_response = requests.post(UPLOAD_URL, json=data)
    # Check if the request was successful
    if api_response.status_code in (200, 201):
        print("Data successfully sent to the server.")
    else:
        # Print error information if the request failed
        print(f"Failed to send data. Status code: {api_response.status_code}")
        print(api_response.text)
