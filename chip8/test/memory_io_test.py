
import unittest
import sys
from pathlib import Path

sys.path.append('src')

from Memory import Memory

class MemoryIOTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()

    def test_read_write_8bit(self):
        self.memory.write_8bit(0x200, 0x7)
        self.assertEqual(self.memory.read(0x200), 0x7)

    def test_read_write_8bit_by_truncate(self):
        self.memory.write_8bit(0x200, 0x8)
        self.assertEqual(self.memory.read(0x200), 0x0)

        self.memory.write_8bit(0x200, 0xA)
        self.assertEqual(self.memory.read(0x200), 0x2)

        self.memory.write_8bit(0x200, 0xFF)
        self.assertEqual(self.memory.read(0x200), 0x7)

    def test_read_write_16bit(self):
        self.memory.write_16bit(0x200, 0x7)
        self.assertEqual(self.memory.read(0x200), 0x7)

        self.memory.write_16bit(0x200, 0x9)
        self.assertEqual(self.memory.read(0x200), 0x9)

        self.memory.write_16bit(0x200, 0xF)
        self.assertEqual(self.memory.read(0x200), 0xF)

    def test_read_write_16bit_by_truncate(self):
        self.memory.write_16bit(0x200, 0x10)
        self.assertEqual(self.memory.read(0x200), 0x0)

        self.memory.write_16bit(0x200, 0xFF)
        self.assertEqual(self.memory.read(0x200), 0xF)

        self.memory.write_16bit(0x200, 0x1A)
        self.assertEqual(self.memory.read(0x200), 0xA)
