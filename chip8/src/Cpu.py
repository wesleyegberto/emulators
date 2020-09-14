from matplotlib import pyplot as plt
from Memory import Memory

class Cpu:
    """ CPU with registers and cycles """

    """ Instruction length: 2 bytes """
    OPCODE_LENGTH = 0x2

    """ Program area for opcodes of 2 bytes long """
    PROGRAM_CODE_AREA_START = 0x200

    INTERPRETER_START_RESERVED_AREA = 0xEA0

    """ Stack area has size of 12 x 2-byte """
    STACK_START_ADDRESS = 0xEA0
    STACK_END_ADDRESS = 0xECF

    # internal registers
    REGISTER_PC_ADDRESS = 0xED0
    REGISTER_SP_ADDRESS = 0xED1
    REGISTER_I_ADDRESS = 0xED2
    REGISTER_DT_ADDRESS = 0xED3
    REGISTER_ST_ADDRESS = 0xED4

    # data registers start memory position: 0xEF0 + V (where V is a variable from V0 to VF)
    REGISTERS_DATA_START_ADDRESS = 0xEF0
    # reserved data register VF
    REGISTER_DATA_VF = 0xEFF

    DISPLAY_RESERVED_START_ADDRESS = 0xF00

    def __init__(self):
        self.memory = Memory()

        self.initialize()

    def initialize(self):
        """ Initialize the registers

        - `PC`: program counter of 16-bit
        - `SP`: stack pointer of 8-bit
        - `I`: address pointer of 16-bit
        - `DT`: delay timer of 8-bit
        - `ST`: sound timer of 8-bit
        """

        # program start at memory address 0x200
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, Cpu.PROGRAM_CODE_AREA_START)

        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, Cpu.PROGRAM_CODE_AREA_START)

        # stack points start at reserved memory address
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, Cpu.STACK_START_ADDRESS)

        self.memory.write_8bit(Cpu.REGISTER_DT_ADDRESS, 0x00)
        self.memory.write_8bit(Cpu.REGISTER_ST_ADDRESS, 0x00)


    def is_valid_hexadecimal(self, value):
        return value >= 0 and value <= 0xF

    def calculate_variable_register(self, register):
        """ Return the memory position for the given register (0 to F) """
        self.validate_variable_register(register)
        return Memory.REGISTERS_DATA_START_ADDRESS + register

    def validate_allowed_address(self, address):
        """ Validate if the given address is allowed to be accessed """

        if address < Memory.PROGRAM_CODE_AREA_START or address > Memory.INTERPRETER_START_RESERVED_AREA:
            raise Exception('Illegal memory access')

    def validate_variable_register(self, register):
        """ Validate if the given register is a variable (hex 0 to F) """
        if not self.is_valid_hexadecimal(register):
            raise Exception('Invalid register, use V0 to VE')
        if register == 0xF:
            raise Exception('Illegal access: reserved register')

    def write_V(self, register, value):
        """ Store a value into one of registers V0-VF """
        # TODO: check if this can be on CPU
        self.memory.write_8bit(this.calculate_variable_register(register), value)

    def read_V(self, register):
        """ Read a value from one of registers V0-VF """
        return self.memory.read(this.calculate_variable_register(register))

    def read_font(self, value):
        if not self.is_valid_hexadecimal(value):
            raise Exception('Invalid font, please choose between hex 0 and F')
        # offset to skip the unwanted positions (hex * sprite length)
        offset = value * 5
        return self.memory.read_range(offset, 5)

    def plot_char(self, value):
        """ Plots the builtin font (0 to F) """

        char = self.read_font(value)
        sprite = [self.bitfield(val) for val in char]
        plt.imshow(sprite, cmap='Greys', interpolation='nearest')
        plt.show()

    def bitfield(self, n):
        bits = [int(digit) for digit in bin(n)[2:]]
        if len(bits) < 8:
            for i in range(8 - len(bits)):
                bits.insert(0, 0)
        return bits

    def step_pc(self):
        """ Increment PC by 2 bytes """
        # TODO: check if has reached the limit
        # TODO: check if is in even position
        # TODO: increment PC
        pass

    def cycle_dt(self):
        """ Check if DT needs to count down """
        pass

    def check_beep(self):
        """ Check if needs to emit beep """
        pass

    def start(self):
        # Steps:
        # 1 - advance clock
        # 2 - increase PC
        # 3 - check interruption (DT)
        # 4 - check ST to beep
        while True:
            # TODO: clock
            self.step_pc()
            self.check_dt()
            self.check_beep()

