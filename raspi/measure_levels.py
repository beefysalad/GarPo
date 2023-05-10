import RPi.GPIO as GPIO
import time

TRIGGER_PINS = [0,20,6]
ECHO_PINS = [1,5,13]

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)

for pin in TRIGGER_PINS:
    GPIO.setup(pin, GPIO.OUT)

for pin in ECHO_PINS:
    GPIO.setup(pin, GPIO.IN)

def measure_distance(trigger_pin, echo_pin):
    # Send a 10us pulse to trigger the sensor
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Wait for the echo pin to go high
    pulse_start = time.time()
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()

    # Wait for the echo pin to go low
    pulse_end = time.time()
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()

    # Calculate distance from the time it took for the pulse to return
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound is 343 meters per second
    distance = round(distance, 2)  # Round to two decimal places
    return distance

# Measure distance for each sensor
for i in range(len(TRIGGER_PINS)):
    distance = measure_distance(TRIGGER_PINS[i], ECHO_PINS[i])
    print(f"Distance to bin {i+1}: {distance} cm")

# Clean up GPIO pins
GPIO.cleanup()
