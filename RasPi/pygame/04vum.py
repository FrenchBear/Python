# 04vum.py
# First drawing exercises in pygame, draws a vu-meter
# 2014-05-01	PV

import pygame
import math, random

def mapf(value, min_in, max_in, min_out, max_out):
	return float(value-min_in)/float(max_in-min_in)*(max_out-min_out)+min_out

def level(x):
	global xc, yc, radius
	global window, res, width, height
	a = mapf(x,0,255,math.pi/4,3*math.pi/4)
	pygame.draw.line(window, pygame.Color(255,128,0), [xc, yc], [int(xc-(radius-20)*math.cos(a)), int(yc-(radius-20)*math.sin(a))], 1)
	pygame.display.update()

def setup():
	global window, res, width, height
	pygame.init()
	res = (1920, 1080)
	width, height = res
	window = pygame.display.set_mode(res, pygame.FULLSCREEN)
	#window.fill(pygame.Color(255,255,255))

	global xc, yc, radius
	radius = height-200
	xc = int(width/2)
	yc = radius+10
	#pygame.draw.rect(window, pygame.Color(0,255,0), [width/2-radius,10,2*radius,2*radius], 3)
	pygame.draw.arc(window, pygame.Color(0,255,0), [width/2-radius,10,2*radius,2*radius], math.pi/4-0.015, 3*math.pi/4+0.03, 3)
	pygame.draw.circle(window, pygame.Color(0,255,0), [xc, yc], 6, 0)

	for i in range(0,101):
		a = mapf(i,0,100,math.pi/4,3*math.pi/4)
		pygame.draw.line(window, pygame.Color(0,255,30), [int(xc-(radius-7)*math.cos(a)), int(yc-(radius-7)*math.sin(a))], [int(xc-(radius-1)*math.cos(a)), int(yc-(radius-1)*math.sin(a))], 1)

	for i in range(0,11):
		a = mapf(i,0,10,math.pi/4,3*math.pi/4)
		pygame.draw.line(window, pygame.Color(0,255,0), [int(xc-(radius-15)*math.cos(a)), int(yc-(radius-15)*math.sin(a))], [int(xc-(radius-1)*math.cos(a)), int(yc-(radius-1)*math.sin(a))], 3)

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
	running = True
	while running:
		#loop()
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				running = False
				break
	pygame.quit()

