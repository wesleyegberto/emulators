import unittest
import sys
from pathlib import Path

sys.path.append('src')

from Cpu import Cpu

class CpuTestCase(unittest.TestCase):
    def setUp(self):
        self.cpu = Cpu()
        self.memory = self.cpu.memory
        self.keyboard = self.cpu.keyboard

    def assert_data_register_value(self, x, expected_value):
        self.assertEqual(self.cpu.read_V(x), expected_value)
        memory_position = self.cpu.calculate_data_register_memory_address(x)
        self.assertEqual(self.memory.read_8bit(memory_position), expected_value)

    def assert_memory_address_16bit_value(self, addr, expected_value):
        self.assertEqual(self.memory.read_16bit(addr), expected_value)

    def assert_memory_address_8bit_value(self, addr, expected_value):
        self.assertEqual(self.memory.read_8bit(addr), expected_value)

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

    def test_opcode_3XKK_should_skip_next_instruction_if_VX_equals_KK(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(2, 0x0F)

        self.cpu.opcode_3XKK(2, 0x0F)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x202)
        self.assert_data_register_value(2, 0x0F)

    def test_opcode_3XKK_should_not_skip_next_instruction_if_VX_not_equal_KK(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(2, 0x0F)

        self.cpu.opcode_3XKK(2, 0xFF)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x200)
        self.assert_data_register_value(2, 0x0F)

    def test_opcode_4XKK_should_skip_next_instruction_if_VX_not_equals_KK(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(3, 0xAF)

        self.cpu.opcode_4XKK(3, 0xFF)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x202)
        self.assert_data_register_value(3, 0xAF)

    def test_opcode_4XKK_should_not_skip_next_instruction_if_VX_equals_KK(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(3, 0xAF)

        self.cpu.opcode_4XKK(3, 0xAF)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x200)
        self.assert_data_register_value(3, 0xAF)

    def test_opcode_5XY0_should_skip_next_instruction_if_VX_equals_VY(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(4, 0xDF)
        self.cpu.write_V(6, 0xDF)

        self.cpu.opcode_5XY0(4, 6)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x202)
        self.assert_data_register_value(4, 0xDF)
        self.assert_data_register_value(6, 0xDF)

    def test_opcode_5XY0_should_not_skip_next_instruction_if_VX_not_equals_VY(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(4, 0xEF)
        self.cpu.write_V(0xA, 0xFF)

        self.cpu.opcode_5XY0(4, 0xA)

        self.assertEqual(self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS), 0x200)
        self.assert_data_register_value(4, 0xEF)
        self.assert_data_register_value(0xA, 0xFF)

    def test_opcode_6XKK_should_set_register_to_given_value(self):
        self.cpu.write_V(0xB, 0xAA)

        self.cpu.opcode_6XKK(0xB, 0xFB)

        self.assert_data_register_value(0xB, 0xFB)

    def test_opcode_6XKK_should_set_register_to_last_given_value(self):
        self.cpu.write_V(0xB, 0xAA)

        self.cpu.opcode_6XKK(0xB, 0xFB)
        self.cpu.opcode_6XKK(0xB, 0xFC)
        self.cpu.opcode_6XKK(0xB, 0xFF)

        self.assert_data_register_value(0xB, 0xFF)

    def test_opcode_7XKK_should_add_the_given_value_to_register(self):
        self.cpu.write_V(0xC, 0xA1)
        self.cpu.write_V(0xF, 0xA)

        self.cpu.opcode_7XKK(0xC, 0xE)

        self.assert_data_register_value(0xC, 0xAF)
        self.assert_data_register_value(0xF, 0xA) # don't change flag

    def test_opcode_7XKK_should_add_more_value_to_register(self):
        self.cpu.write_V(0xC, 0x0)

        self.cpu.opcode_7XKK(0xC, 0x9)
        self.cpu.opcode_7XKK(0xC, 0x4)
        self.cpu.opcode_7XKK(0xC, 0x4)

        self.assert_data_register_value(0xC, 0x11)

    def test_opcode_8XY0_copy_the_register_value_to_another_register(self):
        self.cpu.write_V(0x4, 0x6)
        self.cpu.write_V(0xB, 0xA)

        self.cpu.opcode_8XY0(0x4, 0xB)

        self.assert_data_register_value(0x4, 0xA)
        self.assert_data_register_value(0xB, 0xA)

    def test_opcode_8XY1_should_apply_OR_on_two_register_storing_result_first_one(self):
        self.cpu.write_V(0x1, 0x3)
        self.cpu.write_V(0xD, 0x5)

        self.cpu.opcode_8XY1(0x1, 0xD)

        self.assert_data_register_value(0x1, 0x7)
        self.assert_data_register_value(0xD, 0x5)

        self.cpu.write_V(0x3, 0x2)
        self.cpu.write_V(0xE, 0x2)

        self.cpu.opcode_8XY1(0x3, 0xE)

        self.assert_data_register_value(0x3, 0x2)
        self.assert_data_register_value(0xE, 0x2)

    def test_opcode_8XY2_should_apply_AND_on_two_register_storing_result_first_one(self):
        self.cpu.write_V(0x0, 0x3)
        self.cpu.write_V(0x1, 0x5)

        self.cpu.opcode_8XY2(0x0, 0x1)

        self.assert_data_register_value(0x0, 0x1)
        self.assert_data_register_value(0x1, 0x5)

    def test_opcode_8XY3_should_apply_XOR_on_two_register_storing_result_first_on(self):
        self.cpu.write_V(0xA, 0x5)
        self.cpu.write_V(0xB, 0x3)

        self.cpu.opcode_8XY3(0xA, 0xB)

        self.assert_data_register_value(0xA, 0x6)
        self.assert_data_register_value(0xB, 0x3)

    def test_opcode_8XY4_should_add_two_registers_storing_result_first_one_and_not_set_carry_when_not_overflowing(self):
        self.cpu.write_V(0x4, 0x6)
        self.cpu.write_V(0xB, 0xA)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY4(0x4, 0xB)

        self.assert_data_register_value(0x4, 0x10)
        self.assert_data_register_value(0xB, 0xA)
        self.assert_data_register_value(0xF, 0x0)

    def test_opcode_8XY4_should_add_two_registers_storing_result_first_one_and_set_carry_when_overflowing(self):
        self.cpu.write_V(0x4, 0xFF)
        self.cpu.write_V(0xB, 0xF)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY4(0x4, 0xB)

        self.assert_data_register_value(0x4, 0xE)
        self.assert_data_register_value(0xB, 0xF)
        self.assert_data_register_value(0xF, 0x1)

    def test_opcode_8XY5_should_subtract_VY_from_VX_storing_result_VX_and_not_set_borrow_when_not_underflowing(self):
        self.cpu.write_V(0xA, 0xFF)
        self.cpu.write_V(0xB, 0xF)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY5(0xA, 0xB)

        self.assert_data_register_value(0xA, 0xF0)
        self.assert_data_register_value(0xB, 0xF)
        self.assert_data_register_value(0xF, 1)

    def test_opcode_8XY5_should_subtract_VY_from_VX_storing_result_VX_and_set_borrow_when_underflowing(self):
        self.cpu.write_V(0xA, 0xF)
        self.cpu.write_V(0xB, 0xFF)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY5(0xA, 0xB)

        self.assert_data_register_value(0xA, 0x10) # 16
        self.assert_data_register_value(0xB, 0xFF)
        self.assert_data_register_value(0xF, 0) # negative

    def test_opcode_8XY6_should_shift_right_VY_storing_result_VX_and_not_set_flag_when_least_significant_is_0(self):
        self.cpu.write_V(0xA, 0x0)
        self.cpu.write_V(0xB, 0xA)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY6(0xA, 0xB)

        self.assert_data_register_value(0xA, 0x5)
        self.assert_data_register_value(0xB, 0xA)
        self.assert_data_register_value(0xF, 0)

    def test_opcode_8XY6_should_shift_right_VY_storing_result_VX_and_set_flag_when_least_significant_is_1(self):
        self.cpu.write_V(0xA, 0x0)
        self.cpu.write_V(0xB, 0xB)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY6(0xA, 0xB)

        self.assert_data_register_value(0xA, 0x5)
        self.assert_data_register_value(0xB, 0xB)
        self.assert_data_register_value(0xF, 1)

    def test_opcode_8XY7_should_subtract_VX_from_VY_storing_result_VX_and_not_set_borrow_when_not_underflowing(self):
        self.cpu.write_V(0xA, 0xF)
        self.cpu.write_V(0xB, 0xFF)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY7(0xA, 0xB)

        self.assert_data_register_value(0xA, 0xF0)
        self.assert_data_register_value(0xB, 0xFF)
        self.assert_data_register_value(0xF, 1)

    def test_opcode_8XY7_should_subtract_VX_from_VY_storing_result_VX_and_set_borrow_when_overflowing(self):
        self.cpu.write_V(0xA, 0xFF)
        self.cpu.write_V(0xB, 0xF)
        self.cpu.write_V(0xF, 0)

        self.cpu.opcode_8XY7(0xA, 0xB)

        self.assert_data_register_value(0xA, 0x10)
        self.assert_data_register_value(0xB, 0xF)
        self.assert_data_register_value(0xF, 0)

    def test_opcode_8XYE_should_shift_left_VY_storing_result_VX_and_not_set_flag_when_most_significant_is_0(self):
        self.cpu.write_V(0xA, 0x0)
        self.cpu.write_V(0xC, 0x7A)
        self.cpu.write_flag(0)

        self.cpu.opcode_8XYE(0xA, 0xC)

        self.assert_data_register_value(0xA, 0xF4)
        self.assert_data_register_value(0xC, 0x7A)
        self.assert_data_register_value(0xF, 0)

    def test_opcode_8XYE_should_shift_left_VY_storing_result_VX_and_set_flag_when_most_significant_is_1(self):
        self.cpu.write_V(0xA, 0x0)
        self.cpu.write_V(0xC, 0xAA)
        self.cpu.write_flag(0)

        self.cpu.opcode_8XYE(0xA, 0xC)

        self.assert_data_register_value(0xA, 0x54)
        self.assert_data_register_value(0xC, 0xAA)
        self.assert_data_register_value(0xF, 1)

    def test_opcode_9XY0_should_skip_next_instruction_if_VX_not_equals_VY(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0x1, 0xF)
        self.cpu.write_V(0x2, 0xA)

        self.cpu.opcode_9XY0(0x1, 0x2)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x202)
        self.assert_data_register_value(0x1, 0xF)
        self.assert_data_register_value(0x2, 0xA)

    def test_opcode_9XY0_should_skip_next_instruction_if_VX_not_equals_VY(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0x1, 0xF)
        self.cpu.write_V(0x2, 0xF)

        self.cpu.opcode_9XY0(0x1, 0x2)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.assert_data_register_value(0x1, 0xF)
        self.assert_data_register_value(0x2, 0xF)


    def test_opcode_ANNN_should_set_register_I(self):
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, 0x2FF)

        self.cpu.opcode_ANNN(0x230)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_I_ADDRESS, 0x230)

    def test_opcode_ANNN_should_not_set_not_allowed_address_register_I(self):
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, 0x2FF)

        with self.assertRaises(Exception):
            self.cpu.opcode_ANNN(0xF30)

    def test_opcode_BNNN_should_jump_to_address_plus_data_register_V0(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0x0, 0x2)

        self.cpu.opcode_BNNN(0x400)

        self.assert_data_register_value(0x0, 0x2)
        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x404)

    def test_opcode_BNNN_should_not_jump_to_address_not_allowed(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0x0, 0xA)

        with self.assertRaises(Exception):
            self.cpu.opcode_BNNN(0xE99)

    def test_opcode_CXKK_should_set_data_register_X_to_random_byte_AND_0(self):
        self.cpu.write_V(0x9, 0xF)

        self.cpu.opcode_CXKK(0x9, 0x0)

        self.assert_data_register_value(0x9, 0x0)

    def test_opcode_CXKK_should_set_data_register_X_to_random_byte_less_then_0x6(self):
        self.cpu.write_V(0x9, 0xF)

        self.cpu.opcode_CXKK(0x9, 0x5)

        v9_value = self.cpu.read_V(0x9)
        self.assertTrue(v9_value < 0x6)
        self.assert_memory_address_8bit_value(Cpu.REGISTER_RANDOM_NUMBER, v9_value)

    def test_opcode_EX9E_should_skip_next_instruction_if_given_key_was_pressed(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0xA, 0x5)

        self.keyboard.send_key(0x5)
        self.cpu.opcode_EX9E(0xA)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x202)
        self.assert_data_register_value(0xA, 0x5)

    def test_opcode_EX9E_should_not_skip_next_instruction_if_given_key_was_not_pressed(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0xA, 0x6)

        self.keyboard.send_key(0x5)
        self.cpu.opcode_EX9E(0xA)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.assert_data_register_value(0xA, 0x6)

    def test_opcode_EXA1_should_skip_next_instruction_if_given_key_was_not_pressed(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0xA, 0x2)

        self.keyboard.send_key(0xA)
        self.cpu.opcode_EXA1(0xA)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x202)
        self.assert_data_register_value(0xA, 0x2)

    def test_opcode_EXA1_should_not_skip_next_instruction_if_given_key_was_pressed(self):
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.cpu.write_V(0xA, 0xF)

        self.keyboard.send_key(0xF)
        self.cpu.opcode_EXA1(0xA)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_PC_ADDRESS, 0x200)
        self.assert_data_register_value(0xA, 0xF)

    def test_opcode_FX07_should_set_register_to_delay_timer_value(self):
        self.memory.write_8bit(Cpu.REGISTER_DT_ADDRESS, 0xD)
        self.cpu.write_V(0xD, 0x1)

        self.cpu.opcode_FX07(0xD)

        self.assert_data_register_value(0xD, 0xD)

    def test_opcode_FX0A_should_store_key_pressed_in_register(self):
        self.cpu.write_V(0xA, 0x1)

        self.keyboard.send_key(0xF)
        self.cpu.opcode_FX0A(0xA)

        self.assert_data_register_value(0xA, 0xF)

    def test_opcode_FX15_should_set_delay_timer_using_register_value(self):
        self.cpu.write_V(0x9, 0xA)

        self.cpu.opcode_FX15(0x9)

        self.assert_memory_address_8bit_value(Cpu.REGISTER_DT_ADDRESS, 0xA)


    def test_opcode_FX18_should_set_sound_timer_using_register_value(self):
        self.cpu.write_V(0x9, 0x3)

        self.cpu.opcode_FX18(0x9)

        self.assert_memory_address_8bit_value(Cpu.REGISTER_ST_ADDRESS, 0x3)

    def test_opcode_FX1E_should_add_register_value_to_register_I(self):
        self.cpu.write_V(0x5, 0x4)
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, 0x300)

        self.cpu.opcode_FX1E(0x5)

        self.assert_memory_address_16bit_value(Cpu.REGISTER_I_ADDRESS, 0x304)

    def test_opcode_FX29_should_set_register_I_to_font_sprite_defined_in_register(self):
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, 0x200)

        self.cpu.write_V(0xA, 0x1)
        self.cpu.opcode_FX29(0xA)
        self.assert_memory_address_16bit_value(Cpu.REGISTER_I_ADDRESS, 0x5)

        self.cpu.write_V(0xA, 0x7)
        self.cpu.opcode_FX29(0xA)
        self.assert_memory_address_16bit_value(Cpu.REGISTER_I_ADDRESS, 0x23)

        self.cpu.write_V(0xA, 0xA)
        self.cpu.opcode_FX29(0xA)
        self.assert_memory_address_16bit_value(Cpu.REGISTER_I_ADDRESS, 0x32)

        self.cpu.write_V(0xA, 0xF)
        self.cpu.opcode_FX29(0xA)
        self.assert_memory_address_16bit_value(Cpu.REGISTER_I_ADDRESS, 0x4B)

    def test_opcode_FX33_store_BCD(self):
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, 0x500)
        self.cpu.write_V(0xD, 0xF2) # 242

        self.cpu.opcode_FX33(0xD)

        self.assert_memory_address_8bit_value(Cpu.REGISTER_I_ADDRESS, 0x2)
        self.assert_memory_address_8bit_value(Cpu.REGISTER_I_ADDRESS + 1, 0x4)
        self.assert_memory_address_8bit_value(Cpu.REGISTER_I_ADDRESS + 2, 0x2)
        # COSMAC VIP doesn't change I
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, 0x500)

