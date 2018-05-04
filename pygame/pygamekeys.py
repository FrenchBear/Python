# pygamekeys.py
# event.key retourne des codes en supposant un clavier qwerty
# event.dict['unicode'] retourne le vrai caractère de la touche
# 2016-06-17    PV
# 2018-03-29    PV		Better version, display text in graphics mode and give a chance to escape!!!

import pygame
from pygame.locals import *
import sys

def terminate():
    pygame.quit()
    sys.exit()

def loop():
	global row
	running = True
	while running:
		for event in pygame.event.get(): # event handling loop
			if event.type == QUIT:		# Actually no idea how to generate a QUIT event when program is running in fullscreen mode...
				running = False
			if event.type == KEYDOWN:
				carac = event.dict['unicode']
				if carac=='q' or carac=='Q': running=False
				#print(event.key, carac)
				#print(event.dict)
				row += 1
				text(row, str(event.dict))

def text(row, s):
	levelSurf = BASICFONT.render(s, 1, BRIGHTBLUE)
	levelRect = levelSurf.get_rect()
	levelRect.bottomleft = (20, 40+22*row)
	window.blit(levelSurf, levelRect)
	pygame.display.update()

pygame.init()

res = (1920, 1080)
width, height = res
window = pygame.display.set_mode(res, pygame.FULLSCREEN)

BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
BRIGHTBLUE = pygame.Color(  0, 170, 255)

text(0, 'pygamekeys: press a key, q to exit')

row = 0
loop()
pygame.quit()

#while True:
#    loop()
