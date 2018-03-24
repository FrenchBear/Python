# pygamestub.py
# Exemple de programme pygame
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
	screen.fill(pygame.Color(0,0,0))

	global width, height
	radius = height//2-200
	xc = width//2
	yc = height//2
	pygame.draw.circle(screen, pygame.Color(0,255,0), [xc, yc], radius, 0)

	a = 30.0/180.0*math.pi
	pygame.draw.line(screen, pygame.Color(255,128,0), [xc, yc], [int(xc+(radius-20)*math.cos(a)), int(yc-(radius-20)*math.sin(a))], 5)

	label = myfont.render("This is a text", 1, pygame.Color(255,255,0))
	screen.blit(label, (100, height-100))

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

