import RPi.GPIO as GPIO

# GPIO pin definitions
fanPin = 26  # Pin to control Fan
ledPin = 17  # Pin to control LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(fanPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

# Function to control fan and LED based on person count
def control_gpio(person_count):
    if person_count > 0:
        GPIO.output(fanPin, GPIO.HIGH)
        GPIO.output(ledPin, GPIO.HIGH)
        print("Human detected, Fan and LED ON")
    else:
        GPIO.output(fanPin, GPIO.LOW)
        GPIO.output(ledPin, GPIO.LOW)
        print("No human detected, Fan and LED OFF")

def cleanup_gpio():
    GPIO.cleanup()
