import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  ## GPIO 17 PIN number
GPIO.setup(27, GPIO.OUT)  ## GPIO 27 PIN number


def blink():
    print
    "START"
    iteration = 0
    while iteration < 30:  ## Repeated execution of a set of statements is called iteration.
        GPIO.output(17, True)  ## pin 17 on
        GPIO.output(27, False)  ## pin 27 off
        time.sleep(1)  ## delay
        GPIO.output(17, False)  ## pin 17 off
        GPIO.output(27, True)  ## pin 27 on
        time.sleep(1)  ## delayo
        iteration = iteration + 2  ## 
    print
    "END"
    GPIO.cleanup()  ## reset GPIO pin

    blink()  ## close function
