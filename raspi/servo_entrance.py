import RPi.GPIO as GPIO
import time

# Set the GPIO mode and number
GPIO.setmode(GPIO.BCM)
servo_pin = 19

# Set up the GPIO pin for PWM
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)

# Define duty cycle ranges for 0-180 degrees
duty_cycle_0_deg = 7.5  # Duty cycle for 0 degrees
duty_cycle_minus_90_deg = 1.5  # Duty cycle for -90 degrees

# Loop 10 times
for _ in range(10):
    # Rotate to -90 degrees
    pwm.start(duty_cycle_0_deg)
    time.sleep(1)
    pwm.ChangeDutyCycle(duty_cycle_minus_90_deg)
    time.sleep(1)

    # Rotate back to 0 degrees
    pwm.ChangeDutyCycle(duty_cycle_0_deg)
    time.sleep(1)

# Cleanup
pwm.stop()
GPIO.cleanup()
