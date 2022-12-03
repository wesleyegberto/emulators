
class Keyboard:
    """ Class to handle keyboard events.

    Original COSMIC VIP keyboard layout:

    1 2 3 C
    4 5 6 D
    7 8 9 E
    A 0 B F
    """
    def __init__(self):
        self.last_key_pressed = None

    def read_key(self):
        return self.last_key_pressed

    def send_key(self, key_code):
        self.last_key_pressed = key_code & 0xF

    def handle_pygame_event(self, event):
        pass
