import cv2
from yolo_detection import detect_people
from gpio_control import control_gpio
from image_upload import upload_to_server
import time

# Initialize variables
previous_person_count = 0  # To track changes in person count
usb_camera_index = 0  # Index for the USB camera

# Initialize camera
cap = cv2.VideoCapture(usb_camera_index)

try:
    while True:
        # Capture frame-by-frame from the USB camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting.")
            break

        # Detect people in the frame
        person_count, processed_frame = detect_people(frame)

        # Check if the person count has changed since the last frame
        if person_count != previous_person_count:
            previous_person_count = person_count  # Update previous count

            # Calculate or define the temperature based on person count
            temperature = 20.0 + (0.5 * person_count)  # Example temperature logic
            
            # Upload the image and person count to the server
            upload_to_server(processed_frame, person_count)

            # Control fan and LED based on the current person count and temperature
            control_gpio(person_count, temperature)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Adjust delay as needed for frame rate
        time.sleep(1) 

finally:
    # Cleanup camera resources
    cap.release()
    cv2.destroyAllWindows()
