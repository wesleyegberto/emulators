import unittest
import sys
from pathlib import Path

sys.path.append('src')

from Keyboard import Keyboard

class KeyboardTest(unittest.TestCase):
    def setUp(self):
        self.keyboard = Keyboard()

    def test_should_initialize_none(self):
        self.assertEqual(self.keyboard.read_key(), None)

    def test_should_store_key_pressed(self):
        self.keyboard.send_key(0x9)

        self.assertEqual(self.keyboard.read_key(), 0x9)

