# candle.py
# From The Official Raspberry Pi Projects Book
# 2016-06-02	PV

import RPi.GPIO as GPIO
import time, random

LED = 18

def setup():
	global pwm

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED, GPIO.OUT)

	pwm = GPIO.PWM(LED, 200)
	pwm.start(100)

def set_brightness(nb):
	pwm.ChangeDutyCycle(nb)

def flicker():
	set_brightness(random.randrange(0,100))
	time.sleep(random.randrange(1,10)*0.01)

def loop():
	try:
		while True:
			flicker()
	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()



setup()
loop()

