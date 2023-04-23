import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)

# Main loop
while True:
    if not GPIO.input(20) == GPIO.HIGH:
        print("motion detected")
    else:
        print("no motion detected")
    time.sleep(1)
