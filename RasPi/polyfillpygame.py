# polyfillpygame.py
# Remplissage de polygone
# 2016-06-01	PV

import pygame
import math

def mapf(value, min_in, max_in, min_out, max_out):
	return float(value-min_in)/float(max_in-min_in)*(max_out-min_out)+min_out

def setup_pygame():
	global screen, res, width, height
	pygame.init()
	res = (1920, 1080)
	width, height = res
	screen = pygame.display.set_mode(res, pygame.FULLSCREEN)

	global myfont
	myfont = pygame.font.SysFont("Bitstream Vera Sans", 36)

def display():
	global screen, res, width, height
	screen.fill(pygame.Color(0,0,0))

	coords = [(100,100), (500,100), (500, 500)]
	pygame.draw.polygon(screen, pygame.Color(0,255,255), coords, 0)

	pygame.display.update()



if __name__=='__main__':
	setup_pygame()
	running = True
	display()
	while running:
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				running = False
				break
	pygame.quit()

