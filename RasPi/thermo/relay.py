#!/usr/bin/env python

# Intermittent heating test, controp of a 220V relay using GPIO
# 2021-06-12	PV
# On a 1400W waffle iron, with a cycle 1s on/5s off, it's burning after 67s, that is 12 heating cycles of 1s
#
# Cabling:
# GND		pin 6 or 9
# VCC/+5V	pin 2 or 4
# GPIO 0	pin 11

import RPi.GPIO as GPIO
import time
from time import perf_counter

LedPin = 11    # pin11	= GPIO 0 (17)
tstart = perf_counter()

def relay_setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to on led

def test_loop():
	cycle = 0
	while True:
		cycle += 1
		print(f"{cycle:3}  {perf_counter()-tstart:6.2f}  Power on")
		GPIO.output(LedPin, GPIO.HIGH)
		time.sleep(1)
		print(f"{cycle:3}  {perf_counter()-tstart:6.2f}  Power off")
		GPIO.output(LedPin, GPIO.LOW)
		time.sleep(5)

def relay_destroy():
	GPIO.output(LedPin, GPIO.LOW)     # Power off
	GPIO.cleanup()                    # Release resources

if __name__ == '__main__':     # Program start from here
	relay_setup()
	try:
		test_loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		relay_destroy()

