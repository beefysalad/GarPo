import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set the GPIO mode to BCM numbering

servo_21_pin = 21  # set the GPIO pin for servo 21
servo_20_pin = 20  # set the GPIO pin for servo 20

GPIO.setup(servo_21_pin, GPIO.OUT)  # set the servo 21 pin as an output
GPIO.setup(servo_20_pin, GPIO.OUT)  # set the servo 20 pin as an output

# create a PWM object for each servo
servo_21_pwm = GPIO.PWM(servo_21_pin, 50)  # 50 Hz frequency
servo_20_pwm = GPIO.PWM(servo_20_pin, 50)  # 50 Hz frequency

# start the PWM signals with 0 duty cycle
servo_21_pwm.start(0)
servo_20_pwm.start(0)

# define a function to set the angle of a servo
def set_servo_angle(pwm, angle):
    duty_cycle = (angle / 18) + 2.5  # calculate duty cycle from angle
    pwm.ChangeDutyCycle(duty_cycle)  # set the duty cycle

# move the servos to some angles
set_servo_angle(servo_21_pwm, 0)  # move servo 21 to 0 degrees
set_servo_angle(servo_20_pwm, 180)  # move servo 20 to 90 degrees

time.sleep(1)  # wait for 1 second

set_servo_angle(servo_21_pwm, 180)  # move servo 21 to 90 degrees
set_servo_angle(servo_20_pwm, 0)  # move servo 20 to 0 degrees

time.sleep(1)  # wait for 1 second

# stop the PWM signals and clean up the GPIO pins
servo_21_pwm.stop()
servo_20_pwm.stop()
GPIO.cleanup()
