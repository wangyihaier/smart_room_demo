#! /usr/bin/python

# Import the libraries we need
import RPi.GPIO as GPIO
import time

LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)


while (True):
    GPIO.output(LED, 1)
    print GPIO.input(LED)
    time.sleep(2)
    GPIO.output(LED, 0)
    print GPIO.input(LED)
    time.sleep(2)
