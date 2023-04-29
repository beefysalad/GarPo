import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIGGER_PIN = 12
ECHO_PIN = 1

GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def distance():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start = time.time()
    while GPIO.input(ECHO_PIN)==0:
        start = time.time()

    while GPIO.input(ECHO_PIN)==1:
        stop = time.time()

    elapsed = stop-start
    distance = elapsed * 17150
    return distance

thresh = [45, 33, 20, 10, 0]

try:
    while True:
        dist = distance()
        print ("Distance: %.1f cm" % dist)
        if dist >= thresh[0]:
            print("Trash bin is empty.")
        elif dist >= thresh[1]:
            print("Trash bin is 25% full.")
        elif dist >= thresh[2]:
            print("Trash bin is 50% full.")
        elif dist >= thresh[3]:
            print("Trash bin is 75% full.")
        else:
            print("Trash bin is full.")

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
