Edge AI Smart Monitoring Classroom Project

Overview: This project aims to implement a Smart Classroom Monitoring System using Edge AI, focusing on detecting people in the classroom, controlling environmental factors (fan and light), and uploading real-time data to a server.

By using computer vision techniques, specifically YOLOv8 for person detection, and hardware control through GPIO, the system provides autonomous and efficient classroom monitoring. This project is an Edge AI solution developed by a student in class 20ES at Danang University of Science and Technology (DUT).

Features:

Real-Time Person Detection: Uses YOLOv8 for detecting people in a classroom setting.

Environmental Control: Adjusts fan speed and LED status based on the number of detected people and temperature requirements.

Server Communication: Uploads detection images and classroom status to a specified server.

Camera Input: Utilizes a USB camera to continuously capture frames and process detections.

Project Structure

├── main/

│   ├── main.py                   # Main script to initialize detection, GPIO, and server upload

├── model/

│   ├── best.pt                   # YOLO model weights for person detection

├── yolo_detection.py             # YOLO-based detection script

├── gpio_control.py               # Controls GPIO (fan, LED) based on detection

├── image_upload.py               # Handles image upload and data submission to server

└── README.md                     # Project documentation


