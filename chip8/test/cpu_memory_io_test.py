import unittest
import sys
from pathlib import Path

sys.path.append('src')

from Cpu import Cpu

class CpuTestCase(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu()

    def test_allowed_memory_access_region(self):
        self.cpu.validate_memory_access_address(0x200)

    def test_reject_interpreter_reserved_area(self):
        with self.assertRaises(Exception):
            self.cpu.validate_memory_access_address(0x1FF)

    def test_reject_execution_reserved_area(self):
        with self.assertRaises(Exception):
            self.cpu.validate_memory_access_address(0xEA0)

    def test_reject_display_reserved_area(self):
        with self.assertRaises(Exception):
            self.cpu.validate_memory_access_address(0xF00)

    def test_data_registers_memory_address(self):
        v0_address = self.cpu.calculate_data_register_memory_address(0)
        self.assertEqual(0xEF0, v0_address)

        v1_address = self.cpu.calculate_data_register_memory_address(1)
        self.assertEqual(0xEF1, v1_address)

        vA_address = self.cpu.calculate_data_register_memory_address(0xA)
        self.assertEqual(0xEFA, vA_address)

        vF_address = self.cpu.calculate_data_register_memory_address(0xF)
        self.assertEqual(0xEFF, vF_address)

    def test_invalid_data_registers(self):
        with self.assertRaises(Exception):
            self.cpu.calculate_data_register_memory_address(0x10)

    def test_data_register_write(self):
        memory = self.cpu.memory

        self.cpu.write_V(0, 0x100)
        self.assertEqual(0x0, self.cpu.read_V(0))
        self.assertEqual(0x0, memory.read_8bit(0xEF0))

        self.cpu.write_V(0xA, 0x1F0)
        self.assertEqual(0xF0, self.cpu.read_V(0xA))
        self.assertEqual(0xF0, memory.read_8bit(0xEFA))

        self.cpu.write_V(0xF, 0x1FF)
        self.assertEqual(0xFF, self.cpu.read_V(0xF))
        self.assertEqual(0xFF, memory.read_8bit(0xEFF))

