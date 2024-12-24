import sys
import unittest
import pygame
from pygame.event import Event

sys.path.append('src')

from Keyboard import Keyboard, PYGAME_EVENT_MAPPING

class KeyboardTest(unittest.TestCase):
    def setUp(self):
        self.keyboard = Keyboard()

    def test_should_initialize_none(self):
        self.assertEqual(self.keyboard.read_key(), None)

    def test_should_store_key_pressed(self):
        self.keyboard.send_key(0x9)

        self.assertEqual(self.keyboard.read_key(), 0x9)

    def test_should_ignore_unwanted_pygame_event(self):
        event = Event(pygame.QUIT)
        handled = self.keyboard.handle_pygame_event(event)
        self.assertFalse(handled)

    def test_should_ignore_unmapped_key(self):
        event = Event(pygame.KEYDOWN, key=pygame.K_p)
        handled = self.keyboard.handle_pygame_event(event)
        self.assertFalse(handled)

    def test_should_set_pressed_key(self):
        for k,v in PYGAME_EVENT_MAPPING.items():
            event = Event(pygame.KEYDOWN, key=k)
            handled = self.keyboard.handle_pygame_event(event)
            self.assertTrue(handled)
            self.assertEqual(self.keyboard.read_key(), v)
