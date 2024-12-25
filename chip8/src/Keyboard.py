import pygame
from utils import quit_emulator

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

    def __init__(self, mocked = False):
        self.last_key_pressed = None
        self.mocked = mocked

    def read_key(self):
        return self.last_key_pressed

    def send_key(self, key_code):
        self.last_key_pressed = key_code & 0xF

    def wait_key_press(self):
        if self.last_key_pressed is None:
            waiting = True and not self.mocked
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Allow closing the window
                        quit_emulator()
                    if event.type == pygame.KEYDOWN:  # Key press detected
                        waiting = not self.handle_pygame_event(event)
        return self.read_key()

    def handle_pygame_event(self, event) -> bool:
        if event.type != pygame.KEYDOWN:
            return False
        # print(f"Key pressed: {pygame.key.name(event.key)}")

        if event.key not in PYGAME_EVENT_MAPPING:
            return False;

        key_value = PYGAME_EVENT_MAPPING.get(event.key)
        self.send_key(key_value)
        return True

