import unittest
import sys

sys.path.append('src')

from Cpu import Cpu
from Display import Display
from Keyboard import Keyboard
from Memory import Memory
from Sound import Sound

class CpuRegistersTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()
        self.display = Display(self.memory)
        self.keyboard = Keyboard()
        self.sound = Sound(mocked=True)

        self.cpu = Cpu(self.memory, self.display, self.keyboard, self.sound)

    def test_data_registers_memory_address(self):
        v0_address = self.cpu.calculate_data_register_memory_address(0)
        self.assertEqual(0xEF0, v0_address)

        v1_address = self.cpu.calculate_data_register_memory_address(1)
        self.assertEqual(0xEF1, v1_address)

        vA_address = self.cpu.calculate_data_register_memory_address(0xA)
        self.assertEqual(0xEFA, vA_address)

        vF_address = self.cpu.calculate_data_register_memory_address(0xF)
        self.assertEqual(0xEFF, vF_address)

    def test_data_register_write(self):
        self.cpu.write_V(0, 0x100)
        self.assertEqual(0x0, self.cpu.read_V(0))
        self.assertEqual(0x0, self.memory.read_8bit(0xEF0))

        self.cpu.write_V(0xA, 0x1F0)
        self.assertEqual(0xF0, self.cpu.read_V(0xA))
        self.assertEqual(0xF0, self.memory.read_8bit(0xEFA))

        self.cpu.write_V(0xF, 0x1FF)
        self.assertEqual(0xFF, self.cpu.read_V(0xF))
        self.assertEqual(0xFF, self.memory.read_8bit(0xEFF))


    def test_pc_register_write(self):
        self.cpu.write_register_pc(0x200)

        self.assertEqual(self.memory.read_16bit(0xED0), 0x200)

    def test_sp_register_read_address(self):
        # Fake stack
        self.memory.write_16bit(0xEA0, 0x200)
        self.memory.write_16bit(0xEA2, 0x202)
        # Set initial SP
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0x2)

        popped_address = self.cpu.read_top_address_in_stack()

        self.assertEqual(popped_address, 0x202)
        self.assertEqual(self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS), 0x2)

    def test_pc_register_increment(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)

        self.cpu.step_pc()

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x202)

    def test_pc_register_increments(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)

        self.cpu.step_pc()
        self.cpu.step_pc()

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x204)

