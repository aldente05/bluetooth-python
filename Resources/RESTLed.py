import ConfigParser
import RPi.GPIO as GPIO
from flask import Flask, jsonify, url_for, abort, make_response, request

# Pull the configuration
config = ConfigParser.RawConfigParser()
config.read('Config.cfg')

# Allowed colors
allowed_colors = ['red', 'blue', 'green']

# Setup GPIO
GPIO.setmode(GPIO.BOARD)

for color in allowed_colors:
    GPIO.setup(config.getint(color, 'gpio_pin'), GPIO.OUT)

# Create the Flask Object
app = Flask(__name__)


# -= Get LED Status =-
@app.route('/led/<input_color>', methods=['GET'])
def led_get(input_color):
    color = input_color.lower()
    if (not _check_color(color)):
        abort(404)

    if (GPIO.input(config.getint(color, 'gpio_pin'))):
        return "On"
    else:
        return "Off"


# Turn LED On
@app.route('/led/<input_color>/on', methods=['PUT'])
def led_on(input_color):
    color = input_color.lower()
    if (not _check_color(color)):
        abort(404)

    # Turn on the led
    GPIO.output(config.getint(color, 'gpio_pin'), True)
    return "On"


# Turn LED Off
@app.route('/led/<input_color>/off', methods=['PUT'])
def led_off(input_color):
    color = input_color.lower()
    if (not _check_color(color)):
        abort(404)

    # Turn off the led
    GPIO.output(config.getint(color, 'gpio_pin'), False)
    return "Off"


# Toggle LED
@app.route('/led/<input_color>/toggle', methods=['PUT'])
def led_toggle(input_color):
    color = input_color.lower()
    if (not _check_color(color)):
        abort(404)

    # Toggle level
    GPIO.output(config.getint(color, 'gpio_pin'), not GPIO.input(config.getint(color, 'gpio_pin')))
    if (GPIO.input(config.getint(color, 'gpio_pin'))):
        return "On"
    else:
        return "Off"


# Private Functions
def _check_color(color):
    return color in allowed_colors


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
