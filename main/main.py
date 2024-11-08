import cv2
from yolo_detection import detect_people  # Import the people detection function
from gpio_control import control_gpio     # Import the GPIO control function
from image_upload import upload_to_server # Import the image upload function
import time

# Initialize variables
previous_person_count = 0  # Variable to track changes in detected person count
usb_camera_index = 0       # USB camera index

# Initialize camera
cap = cv2.VideoCapture(usb_camera_index)  # Set up capture from the USB camera

try:
    while True:
        # Capture a frame from the USB camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting.")
            break  # Exit if there's an issue with capturing

        # Detect people in the captured frame
        person_count, processed_frame = detect_people(frame)

        # Display the processed frame with detection results
        cv2.imshow("People Detection", processed_frame)

        # Check if the number of people detected has changed
        if person_count != previous_person_count:
            previous_person_count = person_count  # Update previous count
            # Upload the image and person count to the server
            upload_to_server(processed_frame, person_count)

        # Control fan and LED based on the detected person count
        control_gpio(person_count)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Add a delay between captures to avoid rapid polling
        time.sleep(1)  # Adjust delay as needed

finally:
    # Release the camera and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
