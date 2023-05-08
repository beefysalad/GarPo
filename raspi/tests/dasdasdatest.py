import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set the GPIO mode to BCM numbering

# Set the GPIO pins for the servos
servo_pins = {
    'plastic': 12,
    'metal': 26,
    'paper': 19
}

# Set up the entrance pin
entrance_pin = servo_pins.get('paper')
if entrance_pin:
    GPIO.setup(entrance_pin, GPIO.OUT)  # set the entrance pin as an output
    entrance_pwm = GPIO.PWM(entrance_pin, 50)
    entrance_pwm.start(0)

# Set up the metal servo pin
metal_servo_pin = servo_pins.get('plastic')
if metal_servo_pin:
    GPIO.setup(metal_servo_pin, GPIO.OUT)  # set the metal servo pin as an output
    metal_pwm = GPIO.PWM(metal_servo_pin, 50)
    metal_pwm.start(0)

    # Rotate the metal servo to 60 degrees
    print("60 DEG")
    metal_pwm.ChangeDutyCycle(10)
    time.sleep(1)

    # Rotate back the metal servo to -60 degrees
    #print("-60 DEG")
    #metal_pwm.ChangeDutyCycle(7.5)
    #time.sleep(1)

    # Stop the metal servo
    #metal_pwm.stop()

# Open the entrance by rotating to 90 degrees
if entrance_pin:
    print("Open Entrance")
    entrance_pwm.ChangeDutyCycle(1.5)
    time.sleep(1)
    print("-60 DEG")
    entrance_pwm.ChangeDutyCycle(7.5)
    time.sleep(1)

    # Stop the entrance servo
    entrance_pwm.stop()

    # Wait for the entrance to close
    time.sleep(1)

    # Close the metal servo
    if metal_servo_pin:
        print("Close Metal Servo")
        metal_pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        metal_pwm.stop()
    else:
        print("Invalid metal servo pin configuration")

elif entrance_pin:
    # Open the entrance by rotating to 90 degrees for plastic
    print("Open Entrance")
    entrance_pwm.ChangeDutyCycle(7.5)
    time.sleep(1)
    print("-60 DEG")
    entrance_pwm.ChangeDutyCycle(2.5)
    time.sleep(1)

    # Stop the entrance servo
    entrance_pwm.stop()

else:
    print("Invalid entrance servo pin configuration")

GPIO.cleanup()
