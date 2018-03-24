import math, random

def mapf(value, min_in, max_in, min_out, max_out):
	return float(value-min_in)/float(max_in-min_in)*(max_out-min_out)+min_out

def level(x):
	global xc, yc, radius
	global window, res, width, height
	a = mapf(x,0,255,math.pi/4,3*math.pi/4)
	print("{0:d}: {1:f}".format(x, a))

def setup():
	global res, width, height
	res = (1920, 1080)
	width, height = res

	global xc, yc, radius
	radius = height-200
	xc = int(width/2)
	yc = radius+10

def display():
	level(0)
	level(32)
	level(64)
	level(128)
	level(192)
	level(255)
	
if __name__=='__main__':
	setup()
	display()

