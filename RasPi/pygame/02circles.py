# 02circles.py
# First drawing exercises in pygame
# 2014-04-30	PV

import pygame
import random

def setup():
	global window, res, width, height
	pygame.init()
	res = (1920, 1080)
	width, height = res
	window = pygame.display.set_mode(res, pygame.FULLSCREEN)
	#window.fill(pygame.Color(255,255,255))		# White background

def display():
	global window, res, width, height
	radius = 10
	while radius<0.5*height:
		pygame.draw.circle(window, pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (width/2, height/2), radius, 1)
		radius += 10
	pygame.display.update()

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

