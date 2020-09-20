import unittest
import sys
from pathlib import Path

sys.path.append('src')

from Cpu import Cpu

class CpuTestCase(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu()
        self.memory = self.cpu.memory

    def test_opcode_0NNN(self):
        with self.assertRaises(Exception):
            self.cpu.opcode_0NNN()

    def test_opcode_00E0_should_clean_display(self):
        self.memory.write_8bit(0xF00, 0xF0)
        self.memory.write_8bit(0xF10, 0xF0)
        self.memory.write_8bit(0xFA0, 0xF0)
        self.memory.write_8bit(0xFFF, 0xF0)

        self.cpu.opcode_00E0()

        for addr in range(0xF00, 0xFFF):
            self.assertEqual(self.memory.read_8bit(addr), 0x0)

    def test_opcode_00EE_should_return_to_last_memory_address_before_subroutine(self):
        # Fake stack
        self.memory.write_16bit(0xEA0, 0x200)
        self.memory.write_16bit(0xEA2, 0x202)
        self.memory.write_16bit(0xEA4, 0xAAA)
        # Set initial SP and PC
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0x04)
        self.memory.write_8bit(Cpu.REGISTER_PC_ADDRESS, 0xBBB)

        self.cpu.opcode_00EE()

        self.assertEqual(self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS), 0x02)
        self.assertEqual(self.cpu.read_top_address_in_stack(), 0x202)
        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0xAAA)

    def test_opcode_00EE_should_throw_error_when_stack_is_empty(self):
        self.memory.write_16bit(0xEA0, 0x400)
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0x00)
        self.memory.write_8bit(Cpu.REGISTER_PC_ADDRESS, 0x400)

        with self.assertRaises(Exception):
            self.cpu.opcode_00EE()

    def test_opcode_1NNN_should_jump_to_allowed_memory(self):
        self.cpu.opcode_1NNN(0x8FF)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x8FF)

    def test_opcode_1NNN_should_reject_not_allowed_memory(self):
        with self.assertRaises(Exception):
            self.cpu.opcode_1NNN(0xEA0)

    def test_opcode_2NNN_should_be_correct_state_before_subroutine(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0x00)

        self.cpu.opcode_2NNN(0x400)

        self.assertEqual(self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS), 0x02)
        self.assertEqual(self.memory.read_16bit(0xEA2), 0x200)
        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x400)

    def test_opcode_2NNN_should_throw_stack_overflow(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0x00)

        with self.assertRaises(Exception):
            for i in range(0, 16):
                self.cpu.opcode_2NNN(0x400)

    def test_opcode_3XKK_should_skip_next_instruction(self):
        pass

    def test_opcode_3xKK_should_not_skip_next_instruction(self):
        pass

