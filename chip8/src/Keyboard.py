import pygame

PYGAME_EVENT_MAPPING = {
    pygame.K_4: 0x1, pygame.K_5: 0x2, pygame.K_6: 0x3, pygame.K_7: 0xC,
    pygame.K_r: 0x4, pygame.K_t: 0x5, pygame.K_y: 0x6, pygame.K_u: 0xD,
    pygame.K_f: 0x7, pygame.K_g: 0x8, pygame.K_h: 0x9, pygame.K_j: 0xE,
    pygame.K_v: 0xA, pygame.K_b: 0x0, pygame.K_n: 0xB, pygame.K_m: 0xF
}

class Keyboard:
    """ Class to handle keyboard events.

    Original COSMIC VIP keyboard layout:

    1 2 3 C
    4 5 6 D
    7 8 9 E
    A 0 B F

    Keyboard controller layout:

    4 5 6 7
    R T Y U
    F G H J
    V B N M
    """
    def __init__(self):
        self.last_key_pressed = None

    def read_key(self):
        return self.last_key_pressed

    def send_key(self, key_code):
        self.last_key_pressed = key_code & 0xF

    def handle_pygame_event(self, event) -> bool:
        if event.type != pygame.KEYDOWN:
            return False

        if event.key not in PYGAME_EVENT_MAPPING:
            return False;

        key_value = PYGAME_EVENT_MAPPING.get(event.key)
        self.send_key(key_value)
        return True

