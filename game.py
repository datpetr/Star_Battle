import pygame
import os
import sys
import background
import objects


pygame.init()
size = width, height = 600, 1000
screen = pygame.display.set_mode(size)
rect = screen.get_rect()  # создается Rect