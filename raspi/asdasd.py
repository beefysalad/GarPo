import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set the GPIO mode to BCM numbering

servo_pin = 20 # set the GPIO pin for the servo

GPIO.setup(servo_pin, GPIO.OUT)  # set the servo pin as an output

pwm=GPIO.PWM(servo_pin, 50)

pwm.start(0)

# move to 45 degrees
print("45 DEG")
pwm.ChangeDutyCycle(7.5)
time.sleep(1)

# move back to -45 degrees
print("-45 DEG")
pwm.ChangeDutyCycle(2.5)
time.sleep(1)

# go back to the starting position

pwm.stop()

GPIO.cleanup()
