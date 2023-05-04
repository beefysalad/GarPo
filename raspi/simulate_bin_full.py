import time
import requests

# Define the distance thresholds for each sensor
thresh = [
    [45, 33, 20, 10, 0],  # Thresholds for sensor 1
    [45, 33, 20, 10, 0],  # Thresholds for sensor 2
    [45, 33, 20, 10, 0]   # Thresholds for sensor 3
]

# REST API endpoint URL
endpoint_url = 'http://localhost:8080/bin-full'

# Number of consecutive full detections required before sending a notification
full_detection_threshold = 10

# Counter for consecutive full detections
full_detection_counter = [0] * len(thresh)

# Flag to indicate if a bin is full
bin_full_flag = [False] * len(thresh)

def send_email_notification(bin_number):
    # Data to send in the POST request
    data = {'bin_number': bin_number}

    try:
        response = requests.post(endpoint_url, data=data)
        print(response)
        # response.raise_for_status()
        print('Email notification sent successfully.')
    except requests.exceptions.RequestException as e:
        print('Error sending email notification:', e)

def simulate_distance(sensor):
    # Simulate distance based on the bin being full or empty
    if bin_full_flag[sensor]:
        return 5  # Simulate a distance of 5 cm when the bin is full
    else:
        return 50  # Simulate a distance of 50 cm when the bin is empty

try:
    while True:
        for i in range(len(thresh)):
            dist = simulate_distance(i)
            if i == 0:  # Simulate the first bin reaching maximum capacity
                full_detection_counter[i] = full_detection_threshold
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is full.")
                if not bin_full_flag[i]:
                    bin_full_flag[i] = True  # Set the bin flag to indicate it is full
                    send_email_notification(i+1)
            if dist >= thresh[i][0]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is empty.")
                full_detection_counter[i] = 0
            elif dist >= thresh[i][1]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is 25% full.")
                full_detection_counter[i] = 0
            elif dist >= thresh[i][2]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is 50% full.")
                full_detection_counter[i] = 0
            elif dist >= thresh[i][3]:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is 75% full.")
                full_detection_counter[i] = 0
            else:
                print(f"Trash bin {i+1}: Distance: {dist:.1f} cm - Trash bin is full.")
                full_detection_counter[i] += 1

            if full_detection_counter[i] >= full_detection_threshold:
                bin_full_flag[i] = True  # Set the bin flag to indicate it is full
                send_email_notification(i+1)  # Send email notification for full bin

        time.sleep(1)

except KeyboardInterrupt:
    print("Simulation stopped by the user.")

