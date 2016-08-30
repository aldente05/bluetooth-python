# Import the necessary libraries
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Setup pin 18 as an output
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


# This function turns the valve on and off in 10 sec. intervals.
def valve_OnOff(Pin):
    while True:
        GPIO.output(18, GPIO.HIGH)
        print("GPIO HIGH (on), valve should be off")
        time.sleep(10)  # waiting time in seconds
        GPIO.output(18, GPIO.LOW)
        print("GPIO LOW (off), valve should be on")
        time.sleep(10)

        valve_OnOff(18)

        GPIO.cleanup()

        # to start type "python3 main.py"
