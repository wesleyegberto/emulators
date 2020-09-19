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
        self.assertEqual(self.memory.read_8bit(0x200), 0x7)

    def test_read_write_8bit_by_truncate(self):
        self.memory.write_8bit(0x200, 0x100)
        self.assertEqual(self.memory.read_8bit(0x200), 0x0)

        self.memory.write_8bit(0x200, 0x10A)
        self.assertEqual(self.memory.read_8bit(0x200), 0xA)

        self.memory.write_8bit(0x200, 0xAFF)
        self.assertEqual(self.memory.read_8bit(0x200), 0xFF)

    def test_read_write_16bit(self):
        self.memory.write_16bit(0x200, 0x7)
        self.assertEqual(self.memory.read_16bit(0x200), 0x7)

        self.memory.write_16bit(0x200, 0x0A)
        self.assertEqual(self.memory.read_16bit(0x200), 0x0A)

        self.memory.write_16bit(0x200, 0xFF)
        self.assertEqual(self.memory.read_16bit(0x200), 0xFF)

    def test_read_write_16bit_by_truncate(self):
        self.memory.write_16bit(0x200, 0xA0000)
        self.assertEqual(self.memory.read_16bit(0x200), 0x0)

        self.memory.write_16bit(0x200, 0xA00FF)
        self.assertEqual(self.memory.read_16bit(0x200), 0xFF)

        self.memory.write_16bit(0x200, 0xAFF00)
        self.assertEqual(self.memory.read_16bit(0x200), 0xFF00)

