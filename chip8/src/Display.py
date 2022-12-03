import pygame
from Memory import Memory

# each pixel is represented as 4
SCREEN_SIZE = (62*4, 32*4)

PIXEL_ON = (255, 255, 255)
PIXEL_OFF = (0, 0, 0)

class Display:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

    def update(self):
        self.screen.fill(PIXEL_OFF)


