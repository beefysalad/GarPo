#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from adafruit_servokit import ServoKit

nbServo = 3

MIN_PULSE_WIDTH = 600
MAX_PULSE_WIDTH = 2400
MIN_ANGLE = 0
MAX_ANGLE = 180

kit = ServoKit(channels=16)

def init():
    for i in range(nbServo):
        kit.servo[i].set_pulse_width_range(MIN_PULSE_WIDTH, MAX_PULSE_WIDTH)

def main():
    servoScenario()

def servoScenario():
    for i in range(nbServo):
        for angle in range(MIN_ANGLE, MAX_ANGLE + 1):
            print("Send angle {} to Servo {}".format(angle, i))
            kit.servo[i].angle = angle
            time.sleep(0.01)
        for angle in range(MAX_ANGLE, MIN_ANGLE - 1, -1):
            print("Send angle {} to Servo {}".format(angle, i))
            kit.servo[i].angle = angle
            time.sleep(0.01)
        kit.servo[i].angle = None
        time.sleep(0.5)

if __name__ == '__main__':
    init()
    main()
