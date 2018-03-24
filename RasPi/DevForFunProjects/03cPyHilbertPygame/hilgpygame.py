# hilgpygame.py - Hilbert curve in graphics mode in Python with pygame
# Use a L-system for simple generation
#
# 2015-05-09    PV      Text version
# 2015-05-18    PV      Graphical version with tk
# 2016-06-01    PV      Graphical version with pygame on raspberry pi


import sys
import math
import pygame


# Simple recursive L-System generator for a Hilbert curve
# Recursively process building rules X and Y
def ls2(d, s):
	if d==0:
		dr(s)
	else:
		for c in s:
			if c=='X':
				ls2(d-1, '-YF+XFX+FY-')
			elif c=='Y':
				ls2(d-1, '+XF-YFY-FX+')
			else:
				dr(c)

# Drawing function, process drawing rules    
def dr(s):
	global a, cx, cy, mod, screen
	for c in s:
		if c=='-':          # Rotate 90° anti clockwise = increment a (modulo 4)
			a = (a+1)%4
		elif c=='+':        # Rotate 90° clockwise = decrement a (modulo 4)
			a = (a+3)%4
		elif c=='F':        # Forward drawing instruction
			# Compute next cell coordinates after drawing 1 unit in direction indicated by a
			nx, ny = {
				0: (cx+mod, cy),
				1: (cx, cy-mod),
				2: (cx-mod, cy),
				3: (cx, cy+mod)
				}[a]

			# draw 
			pygame.draw.line(screen, pygame.Color(255,128,0), [cx, cy], [nx, ny], 1)

			global iter
			iter += 1
			if iter % 500==0:
				pygame.display.update()

			cx, cy = nx, ny   # Move to next cell


def setup_pygame():
	global screen, res, width, height
	pygame.init()
	res = (1920, 1080)
	width, height = res
	screen = pygame.display.set_mode(res, pygame.FULLSCREEN)

	global myfont
	myfont = pygame.font.SysFont("Bitstream Vera Sans", 16)


level = 6                           # level 1 is the first drawing as an upside down U

if len(sys.argv)!=1 and len(sys.argv)!=2:
	print("Usage: python3 hilgpygame.py level")
	sys.exit()

if (len(sys.argv)==2):
	try:
		level = int(sys.argv[1])
	except:
		print("hilgpygame: level must be an integer")
		sys.exit()

	if level<1 or level>10:
		print("hilgpygame: level must be in the range 1..10")
		sys.exit()

# Get width and height
setup_pygame()

a = 0
side = int(math.pow(2, level))-1	# side of output square grid in units
mod = (height-20)//side					# size of a square in pixels
iter = 0							# Number of segments drawn to refresh during drawing

cx = (width-mod*side)//2            # initial coordinates
cy = height-(height-mod*side)//2


label = myfont.render("Level {0:d}".format(level), 1, pygame.Color(255,255,0))
screen.blit(label, (0, 0))

ls2(level, 'X')

pygame.display.update()

running = True
while running:
	for event in pygame.event.get():
		if event.type==pygame.KEYDOWN:
			running = False
			break
pygame.quit()

