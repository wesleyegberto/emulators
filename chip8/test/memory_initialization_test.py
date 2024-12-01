import unittest
import sys

sys.path.append('src')

from Memory import Memory

class MemoryInitializationTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_builtin_fonts_initialization(self):
        # font digit 0
        char_values = self.memory.read_range(0x0, 5)
        self.assertListEqual(char_values, [0xF0, 0x90, 0x90, 0x90, 0xF0])

        # font digit 1
        char_values = self.memory.read_range(0x5, 5)
        self.assertListEqual(char_values, [0x20, 0x60, 0x20, 0x20, 0x70])

        # font digit 2
        char_values = self.memory.read_range(0xA, 5)
        self.assertListEqual(char_values, [0xF0, 0x10, 0xF0, 0x80, 0xF0])

        # font digit 3
        char_values = self.memory.read_range(0xF, 5)
        self.assertListEqual(char_values, [0xF0, 0x10, 0xF0, 0x10, 0xF0])

        # font digit 4
        char_values = self.memory.read_range(0x14, 5)
        self.assertListEqual(char_values, [0x90, 0x90, 0xF0, 0x10, 0x10])

        # font digit 5
        char_values = self.memory.read_range(0x19, 5)
        self.assertListEqual(char_values, [0xF0, 0x80, 0xF0, 0x10, 0xF0])

        # font digit 6
        char_values = self.memory.read_range(0x1E, 5)
        self.assertListEqual(char_values, [0xF0, 0x80, 0xF0, 0x90, 0xF0])

        # font digit 7
        char_values = self.memory.read_range(0x23, 5)
        self.assertListEqual(char_values, [0xF0, 0x10, 0x20, 0x40, 0x40])

        # font digit 8
        char_values = self.memory.read_range(0x28, 5)
        self.assertListEqual(char_values, [0xF0, 0x90, 0xF0, 0x90, 0xF0])

        # font digit 9
        char_values = self.memory.read_range(0x2D, 5)
        self.assertListEqual(char_values, [0xF0, 0x90, 0xF0, 0x10, 0xF0])

        # font digit A
        char_values = self.memory.read_range(0x32, 5)
        self.assertListEqual(char_values, [0xF0, 0x90, 0xF0, 0x90, 0x90])

        # font digit B
        char_values = self.memory.read_range(0x37, 5)
        self.assertListEqual(char_values, [0xE0, 0x90, 0xE0, 0x90, 0xE0])

        # font digit C
        char_values = self.memory.read_range(0x3C, 5)
        self.assertListEqual(char_values, [0xF0, 0x80, 0x80, 0x80, 0xF0])

        # font digit D
        char_values = self.memory.read_range(0x41, 5)
        self.assertListEqual(char_values, [0xE0, 0x90, 0x90, 0x90, 0xE0])

        # font digit E
        char_values = self.memory.read_range(0x46, 5)
        self.assertListEqual(char_values, [0xF0, 0x80, 0xF0, 0x80, 0xF0])

        # font digit F
        char_values = self.memory.read_range(0x4B, 5)
        self.assertListEqual(char_values, [0xF0, 0x80, 0xF0, 0x80, 0x80])

