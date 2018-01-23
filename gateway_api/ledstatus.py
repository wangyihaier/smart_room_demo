#! /usr/bin/python

# Import the libraries we need
import RPi.GPIO as GPIO
import time

LED = 26
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.IN)

state = GPIO.input(LED)


while (True):
    print state
    time.sleep(2)
    
