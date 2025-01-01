import pygame
from pygame import KEYUP, KEYDOWN

PYGAME_EVENT_MAPPING = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
}

class Keyboard:
    """ Class to handle keyboard events.

    Original COSMIC VIP keyboard layout:

    1 2 3 C
    4 5 6 D
    7 8 9 E
    A 0 B F

    Keyboard controller layout:

    1 2 3 4
    Q W E R
    A S D F
    Z X C V
    """

    last_key_pressed = None

    def __init__(self):
        self.keyboard = [KEYUP] * 0x10 # 0xF inclusive

    def press_key(self, key_value):
        self.keyboard[key_value] = KEYDOWN

    def release_key(self, key_value):
        self.keyboard[key_value] = KEYUP
        self.last_key_pressed = key_value

    def is_key_pressing_down(self, key_value):
        """
        This will take the given value and output it to the keyboard latch.
        This causes external flag 3 to be set if that key is currently held down or reset if not.
        """
        return self.keyboard[key_value] == KEYDOWN

    def send_key(self, key_value):
        self.press_key(key_value)
        self.release_key(key_value)

    def read_key(self):
        key = self.last_key_pressed
        self.last_key_pressed = None
        return key

    def wait_key_press(self, handle_pygame_event):
        self.last_key_pressed = None
        key_pressed = None

        while key_pressed is None:
            if handle_pygame_event != None:
                handle_pygame_event()
            key_pressed = self.read_key()

        return key_pressed

    def handle_pygame_event(self, event) -> bool:
        if event.type != KEYDOWN and event.type != KEYUP:
            return False
        if event.key not in PYGAME_EVENT_MAPPING:
            return False

        key_value = PYGAME_EVENT_MAPPING.get(event.key)

        if event.type == KEYDOWN:
            self.press_key(key_value)
        else:
            self.release_key(key_value)

        return True

