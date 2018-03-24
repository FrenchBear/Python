# sprites.py
# Rebond de balles en python avec pygame
# From A la decouverte du Raspberry Pi
#
# This implementation doesn't use pygame.sprite, but to implement collision detection, it probably should.
#
# 2016-05-16	PV

import pygame
import random

numballs = 10


# pygame environment initialisation
def setup_pygame():
	global screen, width, height, fps
	pygame.init()
	info = pygame.display.Info()	# Get screen native resolution
	width, height = (info.current_w, info.current_h)
	screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
	fps = pygame.time.Clock()		# To avoid flicker

# Initialization of n balls of ballradius radius
def setup_balls(n, ballradius):
	global r, balls
	global width, height
	r = ballradius
	balls = []
	for i in range(n):
		ball = Ball(random.randrange(r, width-r), random.randrange(r, height-r), random.randint(0,1)*2-1, random.randint(0, 1)*2-1, random.randint(3, r), random.randint(3, r))
		balls.append(ball)

class Ball():	#pygame.sprite.Sprite):
	def __init__(self, x, y, xdir, ydir, xspeed, yspeed):
		#pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([2*r, 2*r])
		self.image.fill(pygame.Color(0, 0, 0))
		pygame.draw.circle(self.image, pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255)), (r,r), r, 0)
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
		self.xdir, self.ydir = xdir, ydir
		self.xspeed, self.yspeed = xspeed, yspeed

	def update(self):
		# test nonlocal
		self.x += self.xdir*self.xspeed
		self.y += self.ydir*self.yspeed
		if self.x<r or self.x>width-r:
			self.xdir = -self.xdir
			self.x += self.xdir*self.xspeed
		if self.y<r or self.y>height-r:
			self.ydir = -self.ydir
			self.y += self.ydir*self.yspeed
		self.rect.center = (self.x, self.y)

# Move balls and refresh display
def display():
	global screen, balls, fps
	screen.fill(pygame.Color(0, 0, 0))
	for ball in balls:
		ball.update()
		screen.blit(ball.image, ball.rect)
	pygame.display.update()
	fps.tick(60)


if __name__=='__main__':
	setup_pygame()
	setup_balls(numballs, 25)
	running = True
	while running:
		display()
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				running = False
				break
	pygame.quit()

	#global width, height
	#print((width, height))

