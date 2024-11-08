import requests
from datetime import datetime
import cv2

# Imgur API client ID
CLIENT_ID = '78c668ac8da2408'
UPLOAD_URL = 'http://192.168.1.81:3000/api/classroom_status/'

def upload_to_server(image, person_count):
    # Save frame to file
    output_image_path = 'output_detected_image.jpg'
    cv2.imwrite(output_image_path, image)

    # Upload image to Imgur
    headers = {'Authorization': f'Client-ID {CLIENT_ID}'}
    with open(output_image_path, 'rb') as image_file:
        response = requests.post('https://api.imgur.com/3/upload', headers=headers, files={'image': image_file})

    # Prepare and send data to the server
    timestamp = datetime.now().isoformat()
    light_status = person_count > 0
    ac_temperature = 20.0 + (0.5 * person_count)
    image_url = response.json()['data']['link'] if response.status_code == 200 else None

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
    api_response = requests.post(UPLOAD_URL, json=data)
    if api_response.status_code in (200, 201):
        print("Data successfully sent to the server.")
    else:
        print(f"Failed to send data. Status code: {api_response.status_code}")
        print(api_response.text)
