import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)  # set the GPIO mode to BCM numbering

# Set the GPIO pins for the servos
servo_pins = {
    'plastic': 12,
    'metal': 26,
    'paper': 19
}

# Get the classified trash from  the command line argument
classified_trash = sys.argv[1]

# Set up the entrance pin
entrance_pin = servo_pins.get('paper')
if entrance_pin:
    GPIO.setup(entrance_pin, GPIO.OUT)  # set the entrance pin as an output
    entrance_pwm = GPIO.PWM(entrance_pin, 50)
    entrance_pwm.start(0)

# Set up the specific servo pin based on the classified trash
specific_servo_pin = servo_pins.get(classified_trash.lower())

if classified_trash.lower() in ['metal', 'plastic']:
    if specific_servo_pin:
        GPIO.setup(specific_servo_pin, GPIO.OUT)  # set the specific servo pin as an output
        specific_pwm = GPIO.PWM(specific_servo_pin, 50)
        specific_pwm.start(0)
        if(classified_trash == 'metal'):
            print("METAL")
            specific_pwm.ChangeDutyCycle(5)
            time.sleep(1)
        elif (classified_trash =='plastic'):
            print("PLASTIC")
            specific_pwm.ChangeDutyCycle(10)
            time.sleep(1)
        # Rotate the specific servo to 60 degrees
        #print("60 DEG")
        #specific_pwm.ChangeDutyCycle(7.5)
        #time.sleep(1)

        # Rotate back the specific servo to -60 degrees
        #print("-60 DEG")
        #specific_pwm.ChangeDutyCycle(2.5)
        #time.sleep(1)

        # Stop the specific servo
        #specific_pwm.stop()

        # Open the entrance by rotating to 90 degrees
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

        # Close the specific servo for metal or paper
        print("Close Specific Servo")
        #specific_pwm.ChangeDutyCycle(7.5)
        #time.sleep(1)
        specific_pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        specific_pwm.stop()

    else:
        print("Invalid specific servo pin configuration")

elif classified_trash.lower() == 'paper':
    if entrance_pin:
        # Open the entrance by rotating to 90 degrees
        print("Open Entrance")
        entrance_pwm.ChangeDutyCycle(1.5)
        time.sleep(1)
        print("-60 DEG")
        entrance_pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        # Stop the entrance servo
        entrance_pwm.stop()

else:
    print("Invalid classified trash")

GPIO.cleanup()
