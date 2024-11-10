import RPi.GPIO as GPIO

# GPIO pin definitions
fanPin = 26  # Pin to control Fan (PWM)
ledPin = 17  # Pin to control LED (on/off)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(fanPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

# Initialize PWM for the fan with a frequency of 10kHz
fan_pwm = GPIO.PWM(fanPin, 10000)
fan_pwm.start(0)  # Start with fan off

# PWM control parameters
PWM_START_SPEED = 10       # Starting speed for 1 detected person (10%)
PWM_STEP_SIZE = 10         # Step size for each additional person (10%)
TEMP_ADJUST_FACTOR = 5     # Adjust fan speed based on temperature difference
MAX_PWM_DUTY_CYCLE = 100   # Maximum PWM duty cycle (100%)
TEMP_THRESHOLD = 25        # Temperature threshold to start adjusting fan speed
LED_ON_THRESHOLD = 1       # Minimum number of people to turn LED ON

# Function to control fan and LED based on person count and temperature
def control_gpio(person_count, temperature):
    # Temperature decreases with more people
    temperature = max(20, 30 - person_count * 2)  # Reduce temperature more with more people (min 20)
    
    if person_count > 0:
        # Turn LED on if there's at least one person detected, otherwise turn it off
        if person_count >= LED_ON_THRESHOLD:
            GPIO.output(ledPin, GPIO.HIGH)  # LED ON
        else:
            GPIO.output(ledPin, GPIO.LOW)  # LED OFF

        # Calculate base fan speed from person count, increase fan speed as more people are detected
        fan_speed = PWM_START_SPEED + (PWM_STEP_SIZE * (person_count - 1))

        # Adjust fan speed based on temperature
        if temperature > TEMP_THRESHOLD:
            # Reduce fan speed as temperature increases
            temp_adjustment = (temperature - TEMP_THRESHOLD) * TEMP_ADJUST_FACTOR
            fan_speed = max(0, fan_speed - temp_adjustment)  # Don't let fan speed go below 0
        else:
            # Increase fan speed as temperature decreases
            temp_adjustment = (TEMP_THRESHOLD - temperature) * TEMP_ADJUST_FACTOR
            fan_speed = min(fan_speed + temp_adjustment, MAX_PWM_DUTY_CYCLE)  # Ensure fan speed doesn't exceed max

        # Ensure fan speed doesn't exceed the maximum duty cycle
        fan_speed = min(fan_speed, MAX_PWM_DUTY_CYCLE)
        
        # Set fan speed
        fan_pwm.ChangeDutyCycle(fan_speed)
        
        print(f"People detected: {person_count}, Temperature: {temperature}°C, Fan Speed: {fan_speed}%, LED {'ON' if person_count >= LED_ON_THRESHOLD else 'OFF'}")
    else:
        # If no people detected, turn off LED and fan
        GPIO.output(ledPin, GPIO.LOW)  # LED OFF
        fan_pwm.ChangeDutyCycle(0)     # Fan OFF
        
        print("No human detected, Fan and LED OFF")

# Cleanup function to safely reset GPIO pins
def cleanup_gpio():
    fan_pwm.stop()
    GPIO.cleanup()
