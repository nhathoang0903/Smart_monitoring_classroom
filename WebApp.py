import requests
import random  # Chỉ để mô phỏng dữ liệu cảm biến. Thay thế bằng các hàm đọc dữ liệu từ cảm biến thực tế.
import time

# Hàm để đọc dữ liệu nhiệt độ từ cảm biến
def read_temperature():
    # Thay thế bằng mã để đọc từ cảm biến thực tế
    temperature = random.uniform(20.0, 30.0)  # Giả lập dữ liệu nhiệt độ
    return round(temperature, 2)

# Hàm để đọc số người trong phòng từ cảm biến
def read_people_count():
    # Thay thế bằng mã để đọc từ cảm biến thực tế
    people_count = random.randint(0, 10)  # Giả lập số người
    return people_count

# Hàm gửi dữ liệu đến Web API
def send_data_to_api(temperature, people_count):
    url = "http://172.26.24.142:3000/api/classroom_status/"  # Thay thế bằng URL của Web API thực tế
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY'  # Nếu API cần xác thực
    }
    payload = {
        "classroom_id": 2,
        "classroom_name": "H108",
        "timestamp": "2024-11-03T15:09:55.618338+07:00",
        "people_count": people_count,
        "light_status": "true",
        "ac_temperature": temperature,
        "image_url": "https://tinhdoan.caobang.gov.vn/uploads/news/2021_11/1_63.jpg"

    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("Dữ liệu đã được gửi thành công:", response.json())
    except requests.exceptions.RequestException as e:
        print("Lỗi khi gửi dữ liệu:", e)

# Chu trình chính để đọc và gửi dữ liệu định kỳ
if __name__ == "__main__":
    while True:
        temp = read_temperature()
        count = read_people_count()
        print(f"Nhiệt độ: {temp}°C, Số người: {count}")

        send_data_to_api(temp, count)
        
        # Gửi dữ liệu mỗi 5 phút (300 giây)
        time.sleep(300)
