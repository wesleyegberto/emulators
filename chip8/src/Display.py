import pygame
from Memory import Memory

# each pixel is represented as 4 pixels
PIXEL_SCALE = 8

SCREEN_SCALED_WIDTH = 64 * PIXEL_SCALE
SCREEN_SCALED_HEIGHT = 32 * PIXEL_SCALE
SCREEN_SIZE = (SCREEN_SCALED_WIDTH, SCREEN_SCALED_HEIGHT)

PIXEL_ON = (255, 255, 255)
PIXEL_OFF = (0, 0, 0)

PIXELS_PER_BYTE = 8
ROW_WIDTH_OFFSET = 64 // PIXELS_PER_BYTE # 8 bytes per row

""" Memory area reserved for screen bits (248 bytes) """
MEMORY_DISPLAY_AREA_START_ADDRESS = 0xF00
MEMORY_DISPLAY_AREA_END_ADDRESS = 0xFFF

class Display:
    WIDTH = 0x3F
    HEIGHT = 0x1F

    def __init__(self, memory: Memory):
        self.memory = memory

    def initialize(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(PIXEL_OFF)
        pygame.display.set_caption('Chip8 Emulator')

    def print_display(self):
        pass

    def render(self):
        # self.screen.blit(Surface, (0,0))

        py_x = 0
        py_y = 0

        for address in range(MEMORY_DISPLAY_AREA_START_ADDRESS, MEMORY_DISPLAY_AREA_END_ADDRESS + 1):
            byte_row = self.memory.read_8bit(address)

            # plots the sprite row pixels
            for i in range(8):
                pixel_color = PIXEL_OFF

                # check from higher to lower bit
                if byte_row > 0 and (byte_row & 1 << (7 - i)) > 0:
                    pixel_color = PIXEL_ON

                rect = pygame.Rect(py_x, py_y, PIXEL_SCALE, PIXEL_SCALE)
                pygame.draw.rect(self.screen, pixel_color, rect)

                # next col
                py_x = py_x + PIXEL_SCALE

            # next row
            if py_x >= SCREEN_SCALED_WIDTH:
                py_x = 0
                py_y = py_y + PIXEL_SCALE

        pygame.display.update()

def calculate_memory_address_offset(x, y):
    offset = y * ROW_WIDTH_OFFSET + (x // PIXELS_PER_BYTE)
    return MEMORY_DISPLAY_AREA_START_ADDRESS + offset

def calculate_y_from_memory_address(addr):
    if addr < MEMORY_DISPLAY_AREA_START_ADDRESS or addr > MEMORY_DISPLAY_AREA_END_ADDRESS:
        raise Exception('Invalid memory address');

    offset = addr - MEMORY_DISPLAY_AREA_START_ADDRESS

    return (offset // ROW_WIDTH_OFFSET) % (ROW_WIDTH_OFFSET - 1)

