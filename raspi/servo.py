import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set the GPIO mode to BCM numbering

servo_pin = 1  # set the GPIO pin for the servo

GPIO.setup(servo_pin, GPIO.OUT)  # set the servo pin as an output

# create a PWM object for the servo
servo_pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency

# start the PWM signal with 0 duty cycle
servo_pwm.start(0)

# define a function to open the door
def open_door():
    # move the servo to the open position (40 degrees)
    duty_cycle = (10 / 18) + 2.5  # calculate duty cycle for 40 degrees
    servo_pwm.ChangeDutyCycle(duty_cycle)  # set the duty cycle
    time.sleep(1)  # wait for the servo to move

    # move the servo back to the original position (0 degrees)
    duty_cycle = (0 / 18) + 2.5  # calculate duty cycle for 0 degrees
    servo_pwm.ChangeDutyCycle(duty_cycle)  # set the duty cycle
    time.sleep(1)  # wait for the servo to move

# open the door
open_door()

time.sleep(5)  # wait for 5 seconds

# stop the PWM signal and clean up the GPIO pins
servo_pwm.stop()
GPIO.cleanup()
