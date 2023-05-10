import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BCM)

# Define the pins for each sensor
#TRIGGER_PINS = [0,20,6]
#ECHO_PINS = [1,5,13]
TRIGGER_PINS = [20]
ECHO_PINS = [5]
email_sent = {}
# Define the distance thresholds for each sensor
#thresh = [
    #[47, 31, 18, 8, 0],  # Thresholds for sensor 1
    #[47, 31, 18, 8, 0],  # Thresholds for sensor 2
    #[47, 31, 18, 8, 0]   # Thresholds for sensor 3
#]
thresh = [
	[24,18,12,6,0]
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
endpoint_url = 'http://localhost:8080/bin-full'

# Number of consecutive full detections required before sending a notification
full_detection_threshold = 10

# Counter for consecutive full detections
full_detection_counter = [0] * len(TRIGGER_PINS)

# Flag to indicate if a bin is full
bin_full_flag = [False] * len(TRIGGER_PINS)

output_files = ["plastic_bin_levels.txt", "paper_bin_levels.txt", "metal_bin_levels.txt"]
def write_bin_level(bin_number,level):
    with open(output_files[bin_number-1], 'w') as f:
        f.write(level)
        
def send_email_notification(bin_number):
    # Data to send in the POST request
    if bin_number in email_sent:
        return
        
    data = {'bin_number': bin_number}

    try:
        response = requests.post(endpoint_url, data=data)
        #sresponse.raise_for_status()
        email_sent[bin_number] = True
        print('Email notification sent successfully.')
    except requests.exceptions.RequestException as e:
        print('Error sending email notification:', e)
try:
    while True:
        for i in range(len(TRIGGER_PINS)):
            dist = distance(i)
            levels = ''

            if dist >= thresh[i][0]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is empty.")
                full_detection_counter[i] = 0
                levels = 'empty'
                if i+1 in email_sent:
                    del email_sent[i+1]
            elif dist >= thresh[i][1]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is 25% full.")
                full_detection_counter[i] = 0
                levels = '25%'
            elif dist >= thresh[i][2]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is 50% full.")
                full_detection_counter[i] = 0
                levels = '50%'                
            elif dist >= thresh[i][3]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is 75% full.")
                full_detection_counter[i] = 0
                levels = '75%'
            else:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is full.")
                full_detection_counter[i] += 1
                levels = 'full'
            write_bin_level(i+1,levels)
            if full_detection_counter[i] >= full_detection_threshold:
                send_email_notification(i+1)  # Send email notification for full bin
                #full_detection_counter[i] = 0  # Reset the counter

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()

# Cleanup GPIO on program exit
GPIO.cleanup()
