import RPi.GPIO as GPIO

# GPIO pin definitions
fanPin = 26  # Pin to control Fan (PWM)
ledPin = 17  # Pin to control LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(fanPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

# Initialize PWM for the fan with a frequency of 1kHz
fan_pwm = GPIO.PWM(fanPin, 1000)
fan_pwm.start(0)  # Start with fan off

# PWM control parameters
PWM_START_SPEED = 30       # Starting speed for 1 detected person
PWM_STEP_SIZE = 20         # Increase in speed per additional person
TEMP_ADJUST_FACTOR = 1     # Increase fan speed per degree above threshold
MAX_PWM_DUTY_CYCLE = 100   # Maximum PWM duty cycle (100%)
TEMP_THRESHOLD = 25        # Temperature threshold to start adjusting fan speed

# Function to control fan and LED based on person count and temperature
def control_gpio(person_count, temperature):
    if person_count > 0 or temperature > TEMP_THRESHOLD:
        # Turn on LED
        GPIO.output(ledPin, GPIO.HIGH)

        # Calculate base fan speed from person count
        fan_speed = PWM_START_SPEED + (PWM_STEP_SIZE * (person_count - 1))
        
        # Increase fan speed based on temperature above the threshold
        if temperature > TEMP_THRESHOLD:
            temp_adjustment = (temperature - TEMP_THRESHOLD) * TEMP_ADJUST_FACTOR
            fan_speed += temp_adjustment
        
        # Ensure fan speed doesn't exceed the maximum duty cycle
        fan_speed = min(fan_speed, MAX_PWM_DUTY_CYCLE)
        
        # Set fan speed
        fan_pwm.ChangeDutyCycle(fan_speed)
        
        print(f"People detected: {person_count}, Temperature: {temperature}°C, Fan Speed: {fan_speed}%, LED ON")
    else:
        # Turn off LED and fan
        GPIO.output(ledPin, GPIO.LOW)
        fan_pwm.ChangeDutyCycle(0)
        
        print("No human detected, AC and LED OFF")

# Cleanup function to safely reset GPIO pins
def cleanup_gpio():
    fan_pwm.stop()
    GPIO.cleanup()

# use this for testing
# try:
#     while True:
#         person_count = int(input("Enter the number of people detected: "))  # For testing
#         temperature = float(input("Enter the current temperature (°C): "))   # For testing

#         # Control GPIO based on detected people and temperature
#         control_gpio(person_count, temperature)

# except KeyboardInterrupt:
#     print("Program interrupted by user")
# finally:
#     cleanup_gpio()
