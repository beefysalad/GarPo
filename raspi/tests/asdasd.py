import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # set the GPIO mode to BCM numbering

servo_pins = [12]  # set the GPIO pins for the servos

for servo_pin in servo_pins:
    GPIO.setup(servo_pin, GPIO.OUT)  # set each servo pin as an output

servos = []
for servo_pin in servo_pins:
    pwm = GPIO.PWM(servo_pin, 50)
    pwm.start(0)
    servos.append(pwm)

# loop 10 times
for _ in range(5):
    # move to 30 degrees
    print("30 DEG")
    for pwm in servos:
        #5 basta oposite (right)
        #10 basta left
        pwm.ChangeDutyCycle(10)
    time.sleep(1)

    # move back to 0 degrees
    print("0 DEG")
    for pwm in servos:
        pwm.ChangeDutyCycle(7.5)
    time.sleep(1)

# go back to the starting position
for pwm in servos:
    pwm.stop()

GPIO.cleanup()
