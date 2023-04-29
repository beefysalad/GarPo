import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

while True:
    if not GPIO.input(16):
        print("Object detected")
    else:
        print("No object detected")
    time.sleep(0.1)
