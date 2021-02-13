"""Soil Moisture Example"""

import time
import board
import displayio

from analogio import AnalogIn
from analogio import AnalogOut
from adafruit_clue import clue

last_moisure_value = 0

def get_moisture_value(pin):

    return (pin.value / 65536) * 1023

def is_dry():
    analog_in = AnalogIn(board.A3)
    global last_moisure_value
    last_moisure_value = get_moisture_value(analog_in)
    analog_in.deinit()
    return last_moisure_value <= 400

data = clue.simple_text_display(title="   Moisture Data", text_scale=2, colors=(clue.WHITE, clue.BLUE, clue.RED, clue.WHITE, clue.GREEN))

board.DISPLAY.brightness = 0.0

data[0].text = ""

clue._sensor.gesture_proximity_threshold = 255

while True:

    prox = clue.proximity
    
    if prox > 20 or clue.button_a:
        
        if is_dry():
            data[1].text = "Soil is dry!"
            data[2].text = "(" + str(last_moisure_value) + ")"
            data[3].text = ""
            data[4].text = "Need to water!!"
        else:
            data[1].text = "Soil is wet"
            data[2].text = "(" + str(last_moisure_value) + ")"
            data[3].text = ""
            data[4].text = "No need to water"

        data.show()
        board.DISPLAY.brightness = 1.0
        time.sleep(15)
        board.DISPLAY.brightness = 0.0
    