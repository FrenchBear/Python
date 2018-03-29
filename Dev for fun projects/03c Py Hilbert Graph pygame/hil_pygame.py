# hil_pygame.py - Hilbert curve in graphics mode in Python using pygame
# Use a L-system for simple generation
#
# 2015-05-09    PV      Text version
# 2015-05-18    PV      Graphical version with tk
# 2018-03-29    PV      Pygame version


import math
import pygame

# pygame init
def setup():
    global window, res, width, height
    pygame.init()
    res = (1920, 1080)
    width, height = res
    window = pygame.display.set_mode(res, pygame.FULLSCREEN)
    #pygame.draw.circle(window, pygame.Color(255,255,0), (width//2, height//2), 20, 1)


def text(row, s):
    global window
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BRIGHTBLUE = pygame.Color(  0, 170, 255)

    levelSurf = BASICFONT.render(s, 1, BRIGHTBLUE)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (50, 50+22*row)
    window.blit(levelSurf, levelRect)
    pygame.display.update()


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
    global window, a, cx, cy, mod
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
            pygame.draw.line(window, pygame.Color(255,128,0), [cx,cy], [nx,ny], 1)

            cx, cy = nx, ny   # Move to next cell


def display():
    global window, width, height, a, cx, cy, mod
    level = 6                           # level 1 is the first drawing as an upside down U
    side = int(math.pow(2, level))      # side of output square grid
    mod = min((width-100)//side, (height-100)//side)    # size in pixels of one cell
    a = 0                               # initial angle

    cx = width//2-(mod*side)//2         # initial coordinates
    cy = 50+int(mod*(side-1/2))

    ls2(level, 'X')
    pygame.display.update()

    text(0, "Hilbert curve in Python")
    text(1, "Generation using L-System")
    text(2, "Graphics using pygame")
    text(3, "Level = "+str(level))

setup()
display()
text(5, "Press any key...")

running = True
while running:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            running = False
            break
pygame.quit()

