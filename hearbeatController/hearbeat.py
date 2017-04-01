import RPi.GPIO as GPIO

# this input variable for hearbeat sensor
# Sensor and pins variables
pulsePin = 0
blinkPin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(pulsePin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(blinkPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

IBI = 600

# Main function
def main():
	global COUNT
	initialise()                                            # Call function initialise() to initalize port setting
	while True:                                             # Start infinitive loop
		COUNT = 0                                       # Set start value at 0
		read_flow_meter()                               # Call function read_flow_meter
		time.sleep(5)                                   # Pause 5 secs

def initialise():
	pinMode(WATER_FLOW_PIN,"INPUT")