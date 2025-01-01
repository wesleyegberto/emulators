import pygame
import random
import time
import sys

from Display import *
from Memory import Memory
from Keyboard import Keyboard
from Sound import Sound

class Cpu:
    """ CPU with registers and cycles """

    TIMERS_CLOCK_SPEED = 60 #hz
    CLOCK_SPEED = 120 #hz

    """ Instruction length: 2 bytes """
    OPCODE_LENGTH = 0x2

    """ Memory area reserved for builtin fonts """
    MEMORY_FONT_AREA_START_ADDRESS = 0x000
    MEMORY_FONT_AREA_END_ADDRESS = 0x050

    """ Memory area reserved for program opcodes of 2 bytes long """
    MEMORY_PROGRAM_CODE_AREA_START_ADDRESS = 0x200
    MEMORY_PROGRAM_CODE_AREA_END_ADDRESS = 0xE9F

    MEMORY_INTERPRETER_AREA_START_ADDRESS = 0xEA0

    """ Memory area reserved for stack (size of 12 x 2-byte) """
    MEMORY_STACK_START_ADDRESS = 0xEA0 # Addr 0xEA0 + REGISTER_SP_ADDRESS
    MEMORY_STACK_END_ADDRESS = 0xEBF # 16 levels of nested subroutines

    # internal registers (implemented using the memory)
    REGISTER_PC_ADDRESS = 0xED0 # 16-bit program counter
    REGISTER_I_ADDRESS = 0xED2 # 16-bit
    REGISTER_SP_ADDRESS = 0xED4 # 8-bit stack pointer

    REGISTER_DT_ADDRESS = 0xED5 # 8-bit delay timer (decremented at a rate of 60Hz)
    REGISTER_ST_ADDRESS = 0xED6 # 8-bit sound timer (decremented at a rate of 60Hz)

    REGISTER_RANDOM_NUMBER_ADDRESS = 0xED9 # 8-bit

    # data registers start memory position: 0xEF0 + V (where V is a variable from V0 to VF)
    MEMORY_REGISTERS_DATA_START_ADDRESS = 0xEF0
    # reserved data register VF
    REGISTER_DATA_VF_ADDRESS = 0xEFF

    """ Memory area reserved for screen bits (248 bytes) """
    MEMORY_DISPLAY_AREA_START_ADDRESS = 0xF00
    MEMORY_DISPLAY_AREA_END_ADDRESS = 0xFFF

    # number of cycles to execute by the CPU
    # NUMBER_CYCLES_BY_EXECUTION = 23;

    def __init__(self, memory: Memory, display: Display, keyboard: Keyboard, sound: Sound):
        self.memory = memory
        self.keyboard = keyboard
        self.display = display
        self.sound = sound

        self.clock = pygame.time.Clock()

        self.last_time = time.time()

        self.opcodes_masks = [
            { 'mask': 0xFFFF, 'opcode': 0x00E0 },
            { 'mask': 0xFFFF, 'opcode': 0x00EE },
            # { 'mask': 0xF000, 'opcode': 0x0000 },
            { 'mask': 0xF000, 'opcode': 0x1000 },
            { 'mask': 0xF000, 'opcode': 0x2000 },
            { 'mask': 0xF000, 'opcode': 0x3000 },
            { 'mask': 0xF000, 'opcode': 0x4000 },
            { 'mask': 0xF00F, 'opcode': 0x5000 },
            { 'mask': 0xF000, 'opcode': 0x6000 },
            { 'mask': 0xF000, 'opcode': 0x7000 },
            { 'mask': 0xF00F, 'opcode': 0x8000 },
            { 'mask': 0xF00F, 'opcode': 0x8001 },
            { 'mask': 0xF00F, 'opcode': 0x8002 },
            { 'mask': 0xF00F, 'opcode': 0x8003 },
            { 'mask': 0xF00F, 'opcode': 0x8004 },
            { 'mask': 0xF00F, 'opcode': 0x8005 },
            { 'mask': 0xF00F, 'opcode': 0x8006 },
            { 'mask': 0xF00F, 'opcode': 0x8007 },
            { 'mask': 0xF00F, 'opcode': 0x800E },
            { 'mask': 0xF00F, 'opcode': 0x9000 },
            { 'mask': 0xF000, 'opcode': 0xA000 },
            { 'mask': 0xF000, 'opcode': 0xB000 },
            { 'mask': 0xF000, 'opcode': 0xC000 },
            { 'mask': 0xF000, 'opcode': 0xD000 },
            { 'mask': 0xF0FF, 'opcode': 0xE09E },
            { 'mask': 0xF0FF, 'opcode': 0xE0A1 },
            { 'mask': 0xF0FF, 'opcode': 0xF000 },
            { 'mask': 0xF0FF, 'opcode': 0xF007 },
            { 'mask': 0xF0FF, 'opcode': 0xF00A },
            { 'mask': 0xF0FF, 'opcode': 0xF015 },
            { 'mask': 0xF0FF, 'opcode': 0xF018 },
            { 'mask': 0xF0FF, 'opcode': 0xF01E },
            { 'mask': 0xF0FF, 'opcode': 0xF029 },
            { 'mask': 0xF0FF, 'opcode': 0xF033 },
            { 'mask': 0xF0FF, 'opcode': 0xF055 },
            { 'mask': 0xF0FF, 'opcode': 0xF065 },
        ]

        self.opcodes_functions_map = {
            0x00E0: lambda _: self.opcode_00E0(),
            0x00EE: lambda _: self.opcode_00EE(),
            # 0x0000: lambda opcode: self.opcode_0NNN(self.get_opcode_value_NNN(opcode)),
            0x1000: lambda opcode: self.opcode_1NNN(self.get_opcode_value_NNN(opcode)),
            0x2000: lambda opcode: self.opcode_2NNN(self.get_opcode_value_NNN(opcode)),
            0x3000: lambda opcode: self.opcode_3XKK(self.get_opcode_value_X(opcode), self.get_opcode_value_KK(opcode)),
            0x4000: lambda opcode: self.opcode_4XKK(self.get_opcode_value_X(opcode), self.get_opcode_value_KK(opcode)),
            0x5000: lambda opcode: self.opcode_5XY0(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x6000: lambda opcode: self.opcode_6XKK(self.get_opcode_value_X(opcode), self.get_opcode_value_KK(opcode)),
            0x7000: lambda opcode: self.opcode_7XKK(self.get_opcode_value_X(opcode), self.get_opcode_value_KK(opcode)),
            0x8000: lambda opcode: self.opcode_8XY0(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8001: lambda opcode: self.opcode_8XY1(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8002: lambda opcode: self.opcode_8XY2(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8003: lambda opcode: self.opcode_8XY3(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8004: lambda opcode: self.opcode_8XY4(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8005: lambda opcode: self.opcode_8XY5(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8006: lambda opcode: self.opcode_8XY6(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x8007: lambda opcode: self.opcode_8XY7(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x800E: lambda opcode: self.opcode_8XYE(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0x9000: lambda opcode: self.opcode_9XY0(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode)),
            0xA000: lambda opcode: self.opcode_ANNN(self.get_opcode_value_NNN(opcode)),
            0xB000: lambda opcode: self.opcode_BNNN(self.get_opcode_value_NNN(opcode)),
            0xC000: lambda opcode: self.opcode_CXKK(self.get_opcode_value_X(opcode), self.get_opcode_value_KK(opcode)),
            0xD000: lambda opcode: self.opcode_DXYK(self.get_opcode_value_X(opcode), self.get_opcode_value_Y(opcode), self.get_opcode_value_K(opcode)),
            0xE09E: lambda opcode: self.opcode_EX9E(self.get_opcode_value_X(opcode)),
            0xE0A1: lambda opcode: self.opcode_EXA1(self.get_opcode_value_X(opcode)),
            0xF000: lambda opcode: self.opcode_FX00(self.get_opcode_value_X(opcode)),
            0xF007: lambda opcode: self.opcode_FX07(self.get_opcode_value_X(opcode)),
            0xF00A: lambda opcode: self.opcode_FX0A(self.get_opcode_value_X(opcode)),
            0xF015: lambda opcode: self.opcode_FX15(self.get_opcode_value_X(opcode)),
            0xF018: lambda opcode: self.opcode_FX18(self.get_opcode_value_X(opcode)),
            0xF01E: lambda opcode: self.opcode_FX1E(self.get_opcode_value_X(opcode)),
            0xF029: lambda opcode: self.opcode_FX29(self.get_opcode_value_X(opcode)),
            0xF033: lambda opcode: self.opcode_FX33(self.get_opcode_value_X(opcode)),
            0xF055: lambda opcode: self.opcode_FX55(self.get_opcode_value_X(opcode)),
            0xF065: lambda opcode: self.opcode_FX65(self.get_opcode_value_X(opcode)),
        }

        self.initialize()

    def initialize(self):
        """ Initialize the registers.

        - `PC`: program counter of 16-bit
        - `SP`: stack pointer of 8-bit
        - `I`: address pointer of 16-bit
        - `DT`: delay timer of 8-bit
        - `ST`: sound timer of 8-bit
        """

        # program start at memory address 0x200
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, Cpu.MEMORY_PROGRAM_CODE_AREA_START_ADDRESS)

        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, Cpu.MEMORY_PROGRAM_CODE_AREA_START_ADDRESS)

        # stack points start at reserved memory address
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0)

        # registers for delay and sound timers
        self.memory.write_8bit(Cpu.REGISTER_DT_ADDRESS, 0x00)
        self.memory.write_8bit(Cpu.REGISTER_ST_ADDRESS, 0x00)

        # clear the screen
        self.opcode_00E0()

    def start(self, on_quit):
        """ Start the CPU processing. """
        # Steps:
        # 1 - advance clock
        #   - generate interrupts
        #   - emulate graphics
        #   - emulate sound
        # 2 - increase PC
        # 3 - check interruption (DT)
        # 4 - check ST to beep

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop(on_quit)
                if event.type == pygame.KEYDOWN:
                    self.keyboard.handle_pygame_event(event)

            self.execute_cpu_cycle()

            # emulate graphics
            self.display.render()

            # simulate 60Hz refresh rate
            time.sleep(1 / Cpu.CLOCK_SPEED)
            # self.clock.tick(Cpu.CLOCK_SPEED)

    def stop(self, on_quit):
        if on_quit is not None:
            on_quit()

        pygame.quit()
        pygame.mixer.quit()
        sys.exit()

    def update_timers(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_time

        # timer update at rate of 60Hz
        if elapsed_time >= (1 / Cpu.TIMERS_CLOCK_SPEED):
            self.last_time = current_time

            # update delay timer
            if self.memory.read_8bit(self.REGISTER_DT_ADDRESS) > 0:
                self.memory.write_8bit(self.REGISTER_DT_ADDRESS, self.memory.read_8bit(self.REGISTER_DT_ADDRESS) - 1)

            # update sound timer
            if self.memory.read_8bit(self.REGISTER_ST_ADDRESS) > 0:
                self.sound.play()

                self.memory.write_8bit(self.REGISTER_ST_ADDRESS, self.memory.read_8bit(self.REGISTER_ST_ADDRESS) - 1)

    def execute_cpu_cycle(self):
        """ CPU cycle execution.

        Steps:
        - fetch instruction
        - decode instruction
        - step PC
        - execute
        """

        # fetch the opcode
        pc = self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS)
        opcode = self.memory.read_16bit(pc)

        # empty memory just do nothing
        if opcode == 0x0000:
            self.step_pc()
            return

        try:
            # decode it
            decoded_opcode = self.decode_opcode(opcode)
            # print(f'\tPC {hex(pc)}; Opcode {hex(opcode)}')

            # step PC
            self.step_pc()

            # execute it
            if decoded_opcode is not None:
                decoded_opcode()
        except Exception as ex:
            print('\n=== Debug Trace ===')
            print(f'PC {hex(pc)}; Opcode {hex(opcode)}; Error: {ex}\n')
            raise ex

    def decode_opcode(self, opcode):
        opcode_function = None
        for opcode_mask in self.opcodes_masks:
            if opcode & opcode_mask['mask'] == opcode_mask['opcode']:
                opcode_function = self.opcodes_functions_map[opcode_mask['opcode']]
                break

        if opcode_function is None:
            return None
            # raise Exception('Opcode cannot be decoded: %s' % hex(opcode));

        return lambda: opcode_function(opcode)

    def get_opcode_value_X(self, opcode):
        """ Extract value X from opcode with format 0X00. """
        return (opcode & 0x0F00) >> 8

    def get_opcode_value_Y(self, opcode):
        """ Extract value Y from opcode with format 00Y0. """
        return (opcode & 0x00F0) >> 4

    def get_opcode_value_K(self, opcode):
        """ Extract value K from opcode with format 000K. """
        return opcode & 0xF

    def get_opcode_value_KK(self, opcode):
        """ Extract value KK from opcode with format 00KK. """
        return opcode & 0xFF

    def get_opcode_value_NNN(self, opcode):
        """ Extract value NNN from opcode with format 0NNN. """
        return opcode & 0xFFF

    def step_pc(self):
        """ Increment PC by 2 bytes """
        pc_value = self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS)
        pc_value = pc_value + 0x2
        # TODO: check if is in even position
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, pc_value)

    def is_valid_hexadecimal(self, value):
        return value >= 0 and value <= 0xF

    def validate_data_register(self, register):
        """ Validate if the given register is a variable (hex 0 to F). """

        if not self.is_valid_hexadecimal(register):
            raise Exception('Invalid register, use V0 to VF')

    def calculate_data_register_memory_address(self, register):
        """ Return the memory position for the given register (0 to F). """

        self.validate_data_register(register)
        return Cpu.MEMORY_REGISTERS_DATA_START_ADDRESS + register

    def get_stack_current_memory_address(self):
        """ Return the current address pointed by register `SP`. """

        sp_value = self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS)
        return Cpu.MEMORY_STACK_START_ADDRESS + sp_value

    def read_top_address_in_stack(self):
        """ Return the current address on top of stack. """

        return self.memory.read_16bit(self.get_stack_current_memory_address())

    def pop_address_from_stack(self):
        stack_counter = self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS)
        if stack_counter == 0x00:
            raise Exception('No more address to pop')

        address = self.read_top_address_in_stack()
        stack_counter = stack_counter - 2
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, stack_counter)

        return address

    def push_address_into_stack(self, addr):
        stack_counter = self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS)
        if Cpu.MEMORY_STACK_START_ADDRESS + stack_counter + 2 > Cpu.MEMORY_STACK_END_ADDRESS:
            raise Exception('Stack overflow')

        stack_counter = stack_counter + 2
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, stack_counter)
        stack_address = Cpu.MEMORY_STACK_START_ADDRESS + stack_counter
        self.memory.write_16bit(stack_address, addr)

    def write_V(self, register, value):
        """ Store a value into one of registers V0-VF """
        self.memory.write_8bit(self.calculate_data_register_memory_address(register), value)

    def write_flag(self, value):
        """ Store a value into register flag VF """
        self.memory.write_8bit(Cpu.REGISTER_DATA_VF_ADDRESS, value)

    def read_V(self, register):
        """ Read a value from one of registers V0-VF """
        return self.memory.read_8bit(self.calculate_data_register_memory_address(register))

    def write_register_pc(self, addr):
        """ Set register `PC` to the given address. """

        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, addr)

    def opcode_0NNN(self, addr=None):
        """ Jump to a machine code routine at NNN.

        This instruction is only used on the old computers on which Chip-8 was
        originally implemented. It is ignored by modern interpreters.
        """

        raise Exception('0NNN is not implemented')

    def opcode_00E0(self):
        """ Clear the display. """

        for addr in range(self.MEMORY_DISPLAY_AREA_START_ADDRESS, self.MEMORY_DISPLAY_AREA_END_ADDRESS):
            self.memory.write_8bit(addr, 0x0)

    def opcode_00EE(self):
        """ Return from a subroutine.

        The interpreter sets the program counter to the address at the top of
        the stack, then subtracts 1 from the stack pointer.
        """

        address = self.pop_address_from_stack()
        # print('Poping stack to ', hex(address))
        self.write_register_pc(address)

    def opcode_1NNN(self, addr):
        """ Jump to location NNN.

        The interpreter sets the program counter to NNN.
        """
        self.write_register_pc(addr)

    def opcode_2NNN(self, addr):
        """ Call subroutine at NNN.

        The interpreter increments the stack pointer, then puts the current PC
        on the top of the stack. The PC is then set to NNN.
        """

        current_addr = self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS)
        self.push_address_into_stack(current_addr)
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, addr)

    def opcode_3XKK(self, x, kk):
        """ Skip next instruction if VX == KK.

        The interpreter compares register Vx to kk, and if they are equal,
        increments the program counter by 2.
        """
        kk = kk & 0xFF
        if self.read_V(x) is kk:
            self.step_pc()

    def opcode_4XKK(self, x, kk):
        """ Skip next instruction if VX != KK.

        The interpreter compares register Vx to kk, and if they are not equal,
        increments the program counter by 2.
        """
        kk = kk & 0xFF
        if self.read_V(x) is not kk:
            self.step_pc()

    def opcode_5XY0(self, x, y):
        """ Skip next instruction if VX = VY.

        The interpreter compares register Vx to register Vy, and if they are
        equal, increments the program counter by 2.
        """
        if self.read_V(x) is self.read_V(y):
            self.step_pc()

    def opcode_6XKK(self, x, kk):
        """ Set VX = KK.

        The interpreter puts the value kk into register Vx.
        """
        self.write_V(x, kk)

    def opcode_7XKK(self, x, kk):
        """ Set VX = VX + KK.

        Adds the value kk to the value of register VX, then stores the result in VX.
        """
        x_value = self.read_V(x)
        kk = kk & 0xFF
        self.write_V(x, x_value + kk)

    def opcode_8XY0(self, x, y):
        """ Set VX = VY.

        Stores the value of register VY in register VX.
        """
        y_value = self.read_V(y)
        self.write_V(x, y_value)

    def opcode_8XY1(self, x, y):
        """ Set Vx = Vx OR Vy.

        Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx.
        A bitwise OR compares the corrseponding bits from two values, and if either bit
        is 1, then the same bit in the result is also 1. Otherwise, it is 0.
        """
        x_value = self.read_V(x)
        y_value = self.read_V(y)
        self.write_V(x, x_value | y_value)
        self.write_flag(0)

    def opcode_8XY2(self, x, y):
        """ Set VX = VX AND VY.

        Performs a bitwise AND on the values of VX and VY, then stores the result in VX.
        A bitwise AND compares the corrseponding bits from two values, and if both bits are
        1, then the same bit in the result is also 1. Otherwise, it is 0.
        """
        x_value = self.read_V(x)
        y_value = self.read_V(y)
        self.write_V(x, x_value & y_value)
        self.write_flag(0)

    def opcode_8XY3(self, x, y):
        """ Set VX = VX XOR VY.

        Performs a bitwise exclusive OR on the values of VX and VY, then stores the result
        in VX. An exclusive OR compares the corrseponding bits from two values, and if the
        bits are not both the same, then the corresponding bit in the result is set to 1.
        Otherwise, it is 0.
        """
        x_value = self.read_V(x)
        y_value = self.read_V(y)
        self.write_V(x, x_value ^ y_value)
        self.write_flag(0)

    def opcode_8XY4(self, x, y):
        """ Set VX = VX + VY, set VF = carry.

        The values of VX and VY are added together. If the result is greater than 8 bits
        (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are
        kept, and stored in VX.
        """
        x_value = self.read_V(x)
        y_value = self.read_V(y)
        result = x_value + y_value

        self.write_V(x, result)
        # set the carry flag (1 for carry used)
        self.write_flag(result > 0xFF)

    def opcode_8XY5(self, x, y):
        """ Set VX = VX - VY, set VF = NOT borrow.

        If VX > VY, then VF is set to 1, otherwise 0. Then VY is subtracted from VX, and
        the results stored in VX.
        """
        x_value = self.read_V(x)
        y_value = self.read_V(y)

        self.write_V(x, x_value - y_value)
        # set the borrow flag (1 for not borrow)
        if x_value > y_value:
            self.write_flag(1)
        else:
            self.write_flag(0)

    def opcode_8XY6(self, x, y):
        """ Set VX = VY >> 1.

        If the least-significant bit of VY is 1, then VF is set to 1, otherwise 0.
        Then VY is divided by 2.
        """
        y_value = self.read_V(y)
        self.write_V(x, y_value >> 1)
        self.write_flag(y_value & 0b1)

    def opcode_8XY7(self, x, y):
        """ Set VX = VY - VX, set VF = NOT borrow.

        If VY > VX, then VF is set to 1, otherwise 0. Then VX is subtracted from VY, and
        the results stored in VX.
        """
        x_value = self.read_V(x)
        y_value = self.read_V(y)

        self.write_V(x, y_value - x_value)
        # set the borrow flag (1 for not borrow)
        if y_value > x_value:
            self.write_flag(1)
        else:
            self.write_flag(0)

    def opcode_8XYE(self, x, y):
        """ Set VX = VY << 1.

        If the most-significant bit of VY is 1, then VF is set to 1, otherwise to 0.
        Then VY is multiplied by 2.
        """
        y_value = self.read_V(y)
        result = y_value << 1
        self.write_V(x, result)
        self.write_flag(y_value >> 7)

    def opcode_9XY0(self, x, y):
        """ Skip next instruction if VX != VY.

        The values of VX and VY are compared, and if they are not equal, the program
        counter is increased by 2.
        """
        if self.read_V(x) is not self.read_V(y):
            self.step_pc()

    def opcode_ANNN(self, addr):
        """ Set I = NNN.

        The value of register I is set to NNN.
        """
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, addr)

    def opcode_BNNN(self, addr):
        """
        Jump to location NNN + V0.

        The program counter is set to NNN Plus the value of V0.
        COSMAC VIP implemented this way.
        """
        v0_value = self.read_V(0x0)
        addr = addr + (v0_value * 2) # double as PC uses 2-bytes (?)
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, addr)

    def opcode_CXKK(self, x, k):
        """
        Set Vx = random byte AND kk.

        The interpreter generates a random number from 0 to 255, which is then
        ANDed with the value KK. The results are stored in VX.
        """
        random_value = random.randint(0, 0xFF) & k
        self.memory.write_8bit(Cpu.REGISTER_RANDOM_NUMBER_ADDRESS, random_value)
        self.write_V(x, random_value)

    def opcode_DXYK(self, vx, vy, nibble):
        """ Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.

        The interpreter reads n bytes from memory (indicates the heigh of the sprite), starting at the address stored in I.
        These bytes are then displayed as sprites on screen at coordinates (Vx, Vy).
        Sprites are XORed onto the existing screen. If this causes any pixels to be erased, VF is set to 1, otherwise it is set to 0.
        If the sprite is positioned so part of it is outside the coordinates of the display, it wraps around to the opposite side of the screen.
        """

        addr = self.memory.read_16bit(Cpu.REGISTER_I_ADDRESS)
        x = self.read_V(vx) & Display.WIDTH
        y = self.read_V(vy) & Display.HEIGHT
        y_warped_at = -1

        collision_flag = 0

        # sprite lines
        for l in range(nibble):
            mem_byte_offset = x % PIXELS_PER_BYTE

            count = 1
            if mem_byte_offset > 0:
                count = 2

            x_warped = False

            # j will be greater 1 if X start in the middle of a memory byte
            for j in range(count):
                # calculate the offset to transform the screen MxN to memory array position (even if in the middle of byte)
                screen_addr = calculate_memory_address_offset(x, y + l) + j

                # row of 8 bits
                sprite_row = self.memory.read_8bit(addr)

                # offset sprite line in the middle of memory address byte
                if mem_byte_offset > 0:
                    # calcutes the sprite line byte to fill in corresponding screen byte (after offset)
                    if j > 0:
                        sprite_row = (sprite_row & (0xFF >> (8 - mem_byte_offset))) << (8 - mem_byte_offset)

                        # if changed the row during split, warps to start of the current row
                        if (calculate_memory_address_offset(x, y + l) // ROW_WIDTH_OFFSET) != (screen_addr // ROW_WIDTH_OFFSET):
                            x_warped = True
                            screen_addr = screen_addr - (x // PIXELS_PER_BYTE) - j # because of splitted byte by j
                    else:
                        sprite_row = sprite_row >> mem_byte_offset

                # if the row is out of screen warps it to the top
                if screen_addr > MEMORY_DISPLAY_AREA_END_ADDRESS:
                    if y_warped_at == -1:
                        y_warped_at = l
                    screen_addr = calculate_memory_address_offset(x, l - y_warped_at) + j
                    if x_warped:
                        screen_addr = screen_addr - ROW_WIDTH_OFFSET

                curr_screen_row = self.memory.read_8bit(screen_addr)

                # only apply XOR flag rule if the current pixel is on
                if curr_screen_row > 0 & collision_flag == 0:
                    collision_flag = sprite_row & curr_screen_row

                # XOEed the sprite row into the screen, turning it off if there is a collision
                draw_result = sprite_row ^ curr_screen_row

                # print(f'Writing {hex(screen_addr)} value {bin(draw_result)}')
                self.memory.write_8bit(screen_addr, draw_result)

            # next sprite line
            addr += 0x1

        if (collision_flag > 0):
            self.write_V(0xF, 1)
        else:
            self.write_V(0xF, 0)

    def opcode_EX9E(self, x):
        """ Skip next instruction if key with the value of VX is pressed.

        Checks the keyboard, and if the key corresponding to the value of VX
        is currently in the down position, PC is increased by 2.
        """
        key_pressed = self.keyboard.read_key()
        x_value = self.read_V(x)

        if key_pressed == x_value:
            self.step_pc()

    def opcode_EXA1(self, x):
        """ Skip next instruction if key with the value of VX is not pressed.

        Checks the keyboard, and if the key corresponding to the value of VX
        is currently in the up position, PC is increased by 2.
        """
        key_pressed = self.keyboard.read_key()
        x_value = self.read_V(x)

        if key_pressed is not x_value:
            self.step_pc()

    def opcode_FX00(self, x):
        """ Set pitch = VX """

        raise Exception("Not implemented")

    def opcode_FX07(self, x):
        """ Set VX = delay timer value.

        The value of DT is placed into VX.
        """
        dt_value = self.memory.read_8bit(Cpu.REGISTER_DT_ADDRESS)
        self.write_V(x, dt_value)

    def opcode_FX0A(self, x):
        """ Wait for a key press, store the value of the key in VX.

        All execution stops until a key is pressed, then the value of that key
        is stored in VX.
        """
        key_pressed = self.keyboard.wait_key_press()
        print(f'Key pressed {key_pressed}')
        self.write_V(x, key_pressed)

    def opcode_FX15(self, x):
        """ Set delay timer = VX.

        DT is set equal to the value of VX.
        """
        x_value = self.read_V(x)
        self.memory.write_8bit(Cpu.REGISTER_DT_ADDRESS, x_value)

    def opcode_FX18(self, x):
        """ Set sound timer = VX.

        ST is set equal to the value of VX.
        """
        x_value = self.read_V(x)
        self.memory.write_8bit(Cpu.REGISTER_ST_ADDRESS, x_value)

    def opcode_FX1E(self, x):
        """ Set I = I + VX.

        The values of I and VX are added, and the results are stored in I.
        """
        x_value = self.read_V(x)
        I_value = self.memory.read_16bit(Cpu.REGISTER_I_ADDRESS)
        new_address = x_value + I_value
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, new_address)

    def opcode_FX29(self, x):
        """ Set I = location of sprite for digit VX.

        The value of I is set to the location for the hexadecimal sprite
        corresponding to the value of VX. See section 2.4, Display, for more
        information on the Chip-8 hexadecimal font.
        """
        x_value = self.read_V(x)

        # multiply by the sprite length to offset to start
        sprite_address = (x_value & 0xFF) * 0x5

        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, sprite_address)

    def opcode_FX33(self, x):
        """ Store BCD representation of VX in memory locations I, I+1, and I+2.

        The interpreter takes the decimal value of VX, and places the hundreds
        digit in memory at location in I, the tens digit at location I+1,
        and the ones digit at location I+2.
        COSMAC VIP doesn't change register I.
        """
        x_value = self.read_V(x)
        addr = self.memory.read_16bit(Cpu.REGISTER_I_ADDRESS)
        self.memory.write_8bit(addr, x_value // 100)
        self.memory.write_8bit(addr + 1, x_value // 10 % 10)
        self.memory.write_8bit(addr + 2, x_value % 10)

    def opcode_FX55(self, x):
        """ Store the values of registers V0 through VX, inclusive, in memory starting at address I.

        The interpreter copies the values of registers V0 through VX into memory, starting at the address in I.
        I is set to I + X + 1 after operation.
        """
        addr = self.memory.read_16bit(Cpu.REGISTER_I_ADDRESS)
        for i in range(0, x + 1):
            value = self.read_V(i)
            self.memory.write_8bit(addr, value)
            addr = addr + 1

        # COSMAC VIP changes I to I + X + 1 (modern implementations doesn't, this can be toggle)
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, addr)

    def opcode_FX65(self, x):
        """ Read registers V0 through VX, inclusive, with the values stored in memory starting at address I.

        The interpreter reads values from memory starting at location I into registers V0 through VX.
        I is set to I + X + 1 after operation.
        """
        addr = self.memory.read_16bit(Cpu.REGISTER_I_ADDRESS)
        for i in range(0, x + 1):
            value = self.memory.read_8bit(addr)
            self.write_V(i, value)
            addr = addr + 1

        # COSMAC VIP changes I to I + X + 1 (modern implementations doesn't, this can be toggle)
        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, addr)

