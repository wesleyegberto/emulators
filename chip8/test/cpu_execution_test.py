import unittest
import sys

sys.path.append('src')

from Cpu import Cpu
from Display import Display
from Keyboard import Keyboard
from Memory import Memory
from Sound import Sound

class CpuExecutionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = Memory()
        self.display = Display(self.memory)
        self.keyboard = Keyboard(mocked=True)
        self.sound = Sound(mocked=True)

        self.cpu = Cpu(self.memory, self.display, self.keyboard, self.sound)

    def assert_equal_hex(self, actual, expected):
        self.assertEqual(actual, expected, "Hex: {} != {}".format(hex(actual), hex(expected)))

    def test_decode_opcode_should_accept_valid_opcode(self):
        opcodes_tests = {
            0x00E0: 0x00E0,
            0x00EE: 0x00EE,
            # 0x0AFC: 0x0000,
            0x1AFC: 0x1000,
            0x2A8A: 0x2000,
            0x32FF: 0x3000,
            0x43FF: 0x4000,
            0x5AB0: 0x5000,
            0x63FF: 0x6000,
            0x73FF: 0x7000,
            0x8890: 0x8000,
            0x8791: 0x8001,
            0x8792: 0x8002,
            0x8793: 0x8003,
            0x8794: 0x8004,
            0x8795: 0x8005,
            0x8796: 0x8006,
            0x8797: 0x8007,
            0x879E: 0x800E,
            0x9790: 0x9000,
            0xA2FF: 0xA000,
            0xB2FF: 0xB000,
            0xC7FF: 0xC000,
            0xD334: 0xD000,
            0xE39E: 0xE09E,
            0xE3A1: 0xE0A1,
            0xF300: 0xF000,
            0xF307: 0xF007,
            0xF30A: 0xF00A,
            0xF315: 0xF015,
            0xF318: 0xF018,
            0xF31E: 0xF01E,
            0xF329: 0xF029,
            0xF333: 0xF033,
            0xF355: 0xF055,
            0xF365: 0xF065,
        }

        # mock the map to just return string instead of executing the opcode
        for opcode_test in opcodes_tests:
            opcode = opcodes_tests[opcode_test]
            self.cpu.opcodes_functions_map[opcode] = lambda _, opcode = opcode: hex(opcode)

        for opcode_test in opcodes_tests:
            opcode = opcodes_tests[opcode_test]

            opcode_function = self.cpu.decode_opcode(opcode_test)
            self.assertEqual(opcode_function(), hex(opcode))

    def test_decode_opcode_should_reject_invalid_opcode(self):
        invalid_opcodes = [0x01A0, 0x00E1, 0xF48C]

        for opcode in invalid_opcodes:
            with self.assertRaises(Exception):
                self.cpu.decode_opcode(opcode)

    def test_get_opcode_value_X_should_extract_value(self):
        self.assert_equal_hex(self.cpu.get_opcode_value_X(0x0A00), 0xA)
        self.assert_equal_hex(self.cpu.get_opcode_value_X(0x8A27), 0xA)
        self.assert_equal_hex(self.cpu.get_opcode_value_X(0x8F81), 0xF)

    def test_get_opcode_value_Y_should_extract_value(self):
        self.assert_equal_hex(self.cpu.get_opcode_value_Y(0x00B0), 0xB)
        self.assert_equal_hex(self.cpu.get_opcode_value_Y(0x8A27), 0x2)
        self.assert_equal_hex(self.cpu.get_opcode_value_Y(0x8F81), 0x8)

    def test_get_opcode_value_K_should_extract_value(self):
        self.assert_equal_hex(self.cpu.get_opcode_value_K(0x000C), 0xC)
        self.assert_equal_hex(self.cpu.get_opcode_value_K(0x8A27), 0x7)
        self.assert_equal_hex(self.cpu.get_opcode_value_K(0x8F81), 0x1)

    def test_get_opcode_value_KK_should_extract_value(self):
        self.assert_equal_hex(self.cpu.get_opcode_value_KK(0x00CD), 0xCD)
        self.assert_equal_hex(self.cpu.get_opcode_value_KK(0x8A27), 0x27)
        self.assert_equal_hex(self.cpu.get_opcode_value_KK(0x8F81), 0x81)

    def test_get_opcode_value_NNN_should_extract_value(self):
        self.assert_equal_hex(self.cpu.get_opcode_value_NNN(0x0ABC), 0xABC)
        self.assert_equal_hex(self.cpu.get_opcode_value_NNN(0x8A27), 0xA27)
        self.assert_equal_hex(self.cpu.get_opcode_value_NNN(0x8F81), 0xF81)

    def setup_opcode(self, opcode):
        self.memory.write_16bit(0x200, opcode)
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)

    def test_cpu_execution(self):
        self.setup_opcode(0x00E0)

        self.memory.write_8bit(0xF00, 0xF0)
        self.memory.write_8bit(0xF10, 0xF0)
        self.memory.write_8bit(0xFA0, 0xF0)
        self.memory.write_8bit(0xFFF, 0xF0)

        self.cpu.execute_cpu_cycle()

        for addr in range(0xF00, 0xFFF):
            self.assert_equal_hex(self.memory.read_8bit(addr), 0x0)
