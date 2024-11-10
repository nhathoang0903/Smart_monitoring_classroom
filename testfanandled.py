import RPi.GPIO as GPIO
import time

# Thiết lập kiểu đánh số GPIO (BCM hoặc BOARD)
GPIO.setmode(GPIO.BCM)  # Sử dụng số GPIO theo chuẩn BCM (Broadcom)

# Định nghĩa các chân GPIO
LED_PIN = 17      # Chân GPIO cho đèn
FAN_PIN = 26      # Chân GPIO cho quạt

# Thiết lập các chân là ngõ ra (OUTPUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

# Hàm bật đèn
def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("Đèn đã bật")

# Hàm tắt đèn
def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    print("Đèn đã tắt")

# Hàm bật quạt
def turn_on_fan():
    GPIO.output(FAN_PIN, GPIO.HIGH)
    print("Quạt đã bật")

# Hàm tắt quạt
def turn_off_fan():
    GPIO.output(FAN_PIN, GPIO.LOW)
    print("Quạt đã tắt")

# Vòng lặp bật tắt đèn và quạt
try:
    while True:
        # Bật đèn và quạt trong 5 giây
        turn_on_led()
        turn_on_fan()
        time.sleep(5)

        # Tắt đèn và quạt trong 5 giây
        turn_off_led()
        turn_off_fan()
        time.sleep(5)

except KeyboardInterrupt:
    # Thoát khỏi vòng lặp khi nhấn Ctrl+C
    print("Kết thúc chương trình")

finally:
    # Reset các chân GPIO sau khi hoàn thành
    GPIO.cleanup()
