import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)

# Set up PWM
pwm = GPIO.PWM(20, 50)
pwm.start(0)

# Function to set servo angle
# Function to set servo angle
# Function to set servo angle
def set_angle(angle):
    if angle >= 0:
        duty = angle / 18 + 2
    else:
        duty = (180 + angle) / 18 + 2
    GPIO.output(20, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(20,False)
    pwm.ChangeDutyCycle(0)

# Rotate servo to 45 degrees and back
set_angle(45)
time.sleep(1)
set_angle(-45)
time.sleep(1)
#set_angle(0)


# Clean up GPIO
pwm.stop()
GPIO.cleanup()
