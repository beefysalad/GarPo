import pigpio
import time

# Connect to the pigpio daemon
pi = pigpio.pi()

# Define the GPIO pins to test
pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Loop through each GPIO pin
for pin in pins:
    # Set the GPIO pin to the output mode
    pi.set_mode(pin, pigpio.OUTPUT)

    # Toggle the state of the GPIO pin 5 times
    for i in range(5):
        pi.write(pin, 1)
        time.sleep(0.5)
        pi.write(pin, 0)
        time.sleep(0.5)

    # Get the state of the GPIO pin and output it to the console
    state = pi.read(pin)
    if state == 0:
        print("Pin {} OK".format(pin))
    else:
        print("Pin {} not working".format(pin))

# Disconnect from the pigpio daemon
pi.stop()
