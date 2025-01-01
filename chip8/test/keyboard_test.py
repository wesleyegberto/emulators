import sys
import unittest
import pygame
from pygame.event import Event

sys.path.append('src')

from Keyboard import Keyboard, PYGAME_EVENT_MAPPING

class KeyboardTest(unittest.TestCase):
    def setUp(self):
        self.keyboard = Keyboard()

    def generate_keyboad_keypressed_events(self, pygame_key):
        event = Event(pygame.KEYDOWN, key=pygame_key)
        handled = self.keyboard.handle_pygame_event(event)
        self.assertTrue(handled)

        event = Event(pygame.KEYUP, key=pygame_key)
        handled = self.keyboard.handle_pygame_event(event)
        self.assertTrue(handled)


    def test_should_initialize_none(self):
        self.assertEqual(self.keyboard.read_key(), None)

        for _,v in PYGAME_EVENT_MAPPING.items():
            self.assertFalse(self.keyboard.is_key_pressing_down(v))

    def test_should_ignore_unwanted_pygame_event(self):
        event = Event(pygame.QUIT)
        handled = self.keyboard.handle_pygame_event(event)
        self.assertFalse(handled)

    def test_should_ignore_unmapped_key(self):
        event = Event(pygame.KEYDOWN, key=pygame.K_p)
        handled = self.keyboard.handle_pygame_event(event)
        self.assertFalse(handled)

    def test_should_wait_for_key_press(self):
        mocked_event = lambda: self.generate_keyboad_keypressed_events(pygame.K_c)

        key_pressed = self.keyboard.wait_key_press(mocked_event)
        self.assertEqual(key_pressed, 0xB)


    def test_should_set_last_pressed_key(self):
        self.generate_keyboad_keypressed_events(pygame.K_z)

        self.assertEqual(self.keyboard.read_key(), 0xA)

    def test_should_register_key_press_and_release(self):
        for k,v in PYGAME_EVENT_MAPPING.items():
            event = Event(pygame.KEYDOWN, key=k)
            handled = self.keyboard.handle_pygame_event(event)

            self.assertTrue(handled)
            self.assertTrue(self.keyboard.is_key_pressing_down(v))

            event = Event(pygame.KEYUP, key=k)
            handled = self.keyboard.handle_pygame_event(event)
            self.assertFalse(self.keyboard.is_key_pressing_down(v))
            self.assertEqual(self.keyboard.read_key(), v)

