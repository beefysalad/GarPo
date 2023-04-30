import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)

# Define the pins for each sensor
TRIGGER_PINS = [12, 16, 20]
ECHO_PINS = [1, 2, 3]

# Define the distance thresholds for each sensor
thresh = [
    [45, 33, 20, 10, 0],  # Thresholds for sensor 1
    [50, 38, 25, 15, 0],  # Thresholds for sensor 2
    [55, 43, 30, 20, 0]   # Thresholds for sensor 3
]

# Set up the GPIO pins for each sensor
for i in range(len(TRIGGER_PINS)):
    GPIO.setup(TRIGGER_PINS[i], GPIO.OUT)
    GPIO.setup(ECHO_PINS[i], GPIO.IN)

def distance(sensor):
    TRIGGER_PIN = TRIGGER_PINS[sensor]
    ECHO_PIN = ECHO_PINS[sensor]

    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    start = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = elapsed * 17150
    return distance

# REST API endpoint URL
endpoint_url = 'http://your-api-endpoint-url'

# Number of consecutive full detections required before sending a notification
full_detection_threshold = 10

# Counter for consecutive full detections
full_detection_counter = [0] * len(TRIGGER_PINS)

def send_email_notification(bin_number):
    # Data to send in the POST request
    data = {'bin_number': bin_number}

    try:
        response = requests.post(endpoint_url, data=data)
        response.raise_for_status()
        print('Email notification sent successfully.')
    except requests.exceptions.RequestException as e:
        print('Error sending email notification:', e)

try:
    while True:
        for i in range(len(TRIGGER_PINS)):
            dist = distance(i)
            print(f"Trash bin {i+1}: Distance: {dist:.1f} cm")

            if dist >= thresh[i][0]:
                print("Trash bin is empty.")
                full_detection_counter[i] = 0
            elif dist >= thresh[i][1]:
                print("Trash bin is 25% full.")
                full_detection_counter[i] = 0
            elif dist >= thresh[i][2]:
                print("Trash bin is 50% full.")
                full_detection_counter[i] = 0
            elif dist >= thresh[i][3]:
                print("Trash bin is 75% full.")
                full_detection_counter[i] = 0
            else:
                print("Trash bin is full.")
                full_detection_counter[i] += 1
                if full_detection_counter[i] >= full_detection_threshold:
                    send_email_notification(i+1)  # Send email notification for full bin
                    full_detection_counter[i] = 0

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
