# 01list.py
# List screen resolution and fonts
# 2016-05-01	PV

import pygame

pygame.init()
pygame.display.set_mode((1920,1080), 0, 24)
lr = pygame.display.list_modes()
lf = pygame.font.get_fonts()
vi = pygame.display.Info()
pygame.display.quit()
print("pygame.display.list_modes():")
print(lr)
print()

print("pygame.font.get_fonts():")
print(lf)
print()

print("pygame.display.Info():")
print(vi)

