# aritmatics Q = pulses_measured * 60 / measuring_time / 7.5
# Import modules
import smbus
import time                             # Library to allow delay times
import datetime                         # Library to allow time and date recording
from array import array                 # Library to allow working with arrays
import os                               # Library to allow command line tasks
import unicodedata                      # Library to use unicode characters above value 127
import math                             # library with mathematical functions
import RPi.GPIO as GPIO                 # library with GPIO read- and write functions
import grovepi                          # library with the GrovePi functions
import struct

# for RPI version 1, use "bus = smbus.SMBus(0)"
rev = GPIO.RPI_REVISION

if rev == 2:
	bus = smbus.SMBus(1)
else:
	bus = smbus.SMBus(0)

# Define global variables

global WATER_FLOW_PIN
global LOGTIME
global PULSE_OUTPUT_FLOW_METER
global FLOW_SPEED
global VALUE
global FLOWTIME
global STARTTIME

# Set starting values variables

# This is the address of the Atmega328 on the GrovePi
address = 0x04

# Set starting values for global variables
WATER_FLOW_PIN = 5                                               FLOWTIME = 0.0
STARTTIME = 0.0
now = time.time()                                               # Set now to current time in seconds since Epoch
date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H:%M:%S")
								# Set date to current time in YYYY-mm-dd_hh:mm:ss format
STARTTIME = now                                                 # Set WORKTIME at current time in seconds since Epoch
FLOWTIME = now
PULSE_OUTPUT_FLOW_METER = 7.5                                   # This sets the output frequency conversion rate (depending on the  Water Flow Meter characteristics)
FLOW_SPEED = 0.0                                                # Set FLOW_SPEED start value at 0.0
LOGTIME = ["2014-04-21_19:00:00","2014-04-21_19:00:00","2014-04-21_19:00:00","2014-04-21_19:00:00","2014-04-21_19:00:00","2014-04-21_19:00:00","2014-04-21_19:00:00"]
VALUE = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]                     # Set array VALUE[0 to 6] with 7 readings, start value at 0.0

# Definition of functions

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

def read_flow_meter():                                          # Function to read Water Flow Meter
	global LOGTIME
	global VALUE
	global COUNT
	now = time.time()                                       # Set now to current time in seconds since Epoch
	STARTTIME = now                                         # Set worktime at current time in seconds since Epoch
	FLOWTIME = now                                          # Set flowtime at currect time in seconds since Epoch
	VALUE[6] = 0.0                                          # Set start value at 0.0
	falling = 0                                             # Set start value at 0
	rising = 0                                              # Set start value at 0
	lus_teller = 0                                          # Set start value at 0
	last_value = 'low'                                      # Set start value at 'low'
	pulse_value = 0
	duration = 0.0
	print( 'Reading Water Flow Meter for 1 second. Please wait ...' )
	while duration < 1.0:
		try:
			pulse_value = digitalRead( WATER_FLOW_PIN )       # Read value from Water Flow Meter
			print( 'lus_teller = ' + str( lus_teller ) + ', pulse_value = ' + str( pulse_value ) )
#			if lus_teller == 0 and pulse_value == 1:
#				last_value = 'high'
			if pulse_value == 0:
                                if last_value == 'high':
                			falling = falling + 1                   # Add 1 to variable low_tick to count the number of changes from high to low (falling pulses)
                                last_value = 'low'
			if pulse_value == 1:
                                if last_value == 'low':
                			rising = rising + 1                     # Add 1 to variable high_tick to count the number of changes from low to high (rising pulses)
				last_value = 'high'
			print( 'falling pulses = ' + str( falling ) + ', rising pulses = ' + str( rising ) +  ', last_value = ' + last_value )
			now = time.time()                               # Set now to current time in seconds since Epoch
			print( 'now = ' + str( now ) )
			date = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H:%M:%S")
									# Set date to current time in YYYY-mm-dd_hh:mm:ss format
			print( 'date = ' + date )
			FLOWTIME = now                                  # Set FLOWTIME at currect time in seconds since Epoch
			duration = FLOWTIME - STARTTIME                 # Calculate duration of measuring in seconds (float)
			print( 'duration = ' + str( duration ) )
		except TypeError:
			print( "Unable to read the Water Flow meter value" )
		lus_teller = lus_teller + 1                     # Add 1 to lus_teller to count the number of loops
	LOGTIME[6] = date                                       # Set LOGTIME[6] at current time in YYYY-mm-dd_hh:mm:ss format
	VALUE[6] = round( ( ( ( 60.0 / duration ) * falling ) / PULSE_OUTPUT_FLOW_METER ), 2 )
								# Calculate flow speed in l/min, rounded at 2 decimals (60.0 seconds / duration (measuring time in seconds) * number of rising pulses
	print( 'last_value = ' + last_value )
	print( 'falling pulses = ' + str( falling ) )
	print( 'rising pulses = ' + str( rising ) )
	print( 'lus_teller = ' + str( lus_teller ) + ' (number of times through loop).' )
	print( 'now = ' + str( now ) + ' time in seconds from Epoch at last measuring. ' )
	print( 'date = ' + date + ' (stringvalue of time at last measuring).' )
	print( 'duration = ' + str( duration ) + ' (time elapsed between start en ending measuring).' )
	print( 'LOGTIME[6] = ' + LOGTIME[6] + ' (saved time).' )
	print( 'VALUE[6] = ' + str( VALUE[6] ) + ' (saved value in l/min rounded at 2 decimals).' )
	print( CODE[6] + " (" + DESCRIPTION[6] + "). Flow meter readings during 1 second. Number of falling pulses = " + str( falling ) + ". Flow speed = " + str( VALUE[6] ) + " l/min. Logtime: " + LOGTIME[6] )
	falling = 0                                             # Reset start value at 0
	rising = 0                                              # Reset start value at 0
	lus_teller = 0                                          # Reset start value at 0
	duration = 0.0                                          # Reset start value at 0.0

main()                                                          # Call function main