#!/usr/bin/env python

# Intermittent heating test with temperature measurement
# Run with: python3 -u merge1.py | tee out.txt
# to avoid output buffering

# 2021-06-12	PV

from tempir import *
from relay import *
from time import sleep


def relay_on():
	GPIO.output(LedPin, GPIO.HIGH)
	#print("Relay on")

def relay_off():
	GPIO.output(LedPin, GPIO.LOW)
	#print("Relay off")


def main_loop():
	cycle = 0

	heat_on = 1			# Heat duration = 1s
	heat_off = 20		# Rest duration = 20s
	relay_clock = 1		# Start with 1s
	relay_state = 1		# of heating
	relay_on()

	print("Clock\tHeat\tTemp")
	while True:
		print(f"{cycle}\t{relay_state}\t{sensor.get_obj_temp():.1f}")
		sleep(1)
		cycle += 1
		relay_clock -= 1
		if relay_clock==0:
			if relay_state==1:
				relay_state = 0
				relay_off()
				relay_clock = heat_off
			else:
				relay_state = 1
				relay_on()
				relay_clock = heat_on


if __name__ == '__main__':     # Program start from here
	relay_setup()
	sensor = MLX90614()

	try:
		main_loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		relay_destroy()

