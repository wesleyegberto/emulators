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
    STACK_START_ADDRESS = 0xEA0 # Addr 0xEA0 + REGISTER_SP_ADDRESS
    STACK_END_ADDRESS = 0xEC0 # 16 levels of nested subroutines

    # internal registers
    REGISTER_PC_ADDRESS = 0xED0 # 16-bit
    REGISTER_I_ADDRESS = 0xED2 # 16-bit
    REGISTER_SP_ADDRESS = 0xED4 # 8-bit
    REGISTER_DT_ADDRESS = 0xED5 # 8-bit
    REGISTER_ST_ADDRESS = 0xED6 # 8-bit

    # data registers start memory position: 0xEF0 + V (where V is a variable from V0 to VF)
    REGISTERS_DATA_START_ADDRESS = 0xEF0
    # reserved data register VF
    REGISTER_DATA_VF = 0xEFF

    DISPLAY_RESERVED_START_ADDRESS = 0xF00

    def __init__(self):
        self.memory = Memory()

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
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, Cpu.PROGRAM_CODE_AREA_START)

        self.memory.write_16bit(Cpu.REGISTER_I_ADDRESS, Cpu.PROGRAM_CODE_AREA_START)

        # stack points start at reserved memory address
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, 0x00)

        self.memory.write_8bit(Cpu.REGISTER_DT_ADDRESS, 0x00)
        self.memory.write_8bit(Cpu.REGISTER_ST_ADDRESS, 0x00)

    def start(self):
        """ Start the CPU processing. """
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

    def step_pc(self):
        """ Increment PC by 2 bytes """
        # TODO: check if has reached the limit
        # TODO: check if is in even position
        # TODO: increment PC
        pass

    def check_dt(self):
        """ Check if DT needs to count down """
        pass

    def check_beep(self):
        """ Check if needs to emit beep """
        pass

    def is_valid_hexadecimal(self, value):
        return value >= 0 and value <= 0xF

    def validate_data_register(self, register):
        """ Validate if the given register is a variable (hex 0 to F). """

        if not self.is_valid_hexadecimal(register):
            raise Exception('Invalid register, use V0 to VE')

    def calculate_data_register_memory_address(self, register):
        """ Return the memory position for the given register (0 to F). """

        self.validate_data_register(register)
        return Cpu.REGISTERS_DATA_START_ADDRESS + register

    def get_stack_current_memory_address(self):
        """ Return the current address pointed by register `SP`. """

        sp_value = self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS)
        return Cpu.STACK_START_ADDRESS + sp_value

    def read_top_address_in_stack(self):
        """ Return the current address on top of stack. """

        return self.memory.read_16bit(self.get_stack_current_memory_address())

    def pop_address_from_stack(self):
        address = self.read_top_address_in_stack()

        sp_value = self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS)
        if sp_value == 0x00:
            raise Exception('No more address to pop')
        sp_value = sp_value - 2 # 16-bit memory address
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, sp_value)

        return address

    def push_address_into_stack(self, addr):
        sp_value = self.memory.read_8bit(Cpu.REGISTER_SP_ADDRESS)
        sp_value = sp_value + 2 # 16-bit memory address
        self.memory.write_8bit(Cpu.REGISTER_SP_ADDRESS, sp_value)

        stack_addr = self.get_stack_current_memory_address()
        if stack_addr == Cpu.STACK_END_ADDRESS:
            raise Exception('Stack overflow')

        self.memory.write_16bit(stack_addr, addr)

    def validate_memory_access_address(self, address):
        """ Validate if the given address is allowed to be accessed. """

        if address < Cpu.PROGRAM_CODE_AREA_START or address >= Cpu.INTERPRETER_START_RESERVED_AREA:
            raise Exception('Illegal memory access')

    def write_V(self, register, value):
        """ Store a value into one of registers V0-VF """
        # TODO: check if this can be on CPU
        self.memory.write_8bit(self.calculate_data_register_memory_address(register), value)

    def read_V(self, register):
        """ Read a value from one of registers V0-VF """
        return self.memory.read_8bit(self.calculate_data_register_memory_address(register))

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

    def write_register_pc(self, addr):
        """ Set register `PC` to the given address. """

        self.validate_memory_access_address(addr)
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, addr)

    def opcode_0NNN(self, addr):
        """ Jump to a machine code routine at nnn.

        This instruction is only used on the old computers on which Chip-8 was
        originally implemented. It is ignored by modern interpreters.
        """

        raise Exception('0NNN is not implemented')

    def opcode_00E0(self):
        """ Clear the display. """

        for addr in range(0xF00, 0xFFF):
            self.memory.write_8bit(addr, 0x0)

    def opcode_00EE(self):
        """ Return from a subroutine.

        The interpreter sets the program counter to the address at the top of
        the stack, then subtracts 1 from the stack pointer.
        """

        address = self.pop_address_from_stack()
        self.write_register_pc(address)

    def opcode_1NNN(self, addr):
        """ Jump to location NNN.

        The interpreter sets the program counter to NNN.
        """
        self.validate_memory_access_address(addr)
        self.write_register_pc(addr)

    def opcode_2NNN(self, addr):
        """ Call subroutine at NNN.

        The interpreter increments the stack pointer, then puts the current PC
        on the top of the stack. The PC is then set to nnn.
        """

        current_addr = self.memory.read_16bit(Cpu.REGISTER_PC_ADDRESS)
        self.push_address_into_stack(current_addr)
        self.memory.write_16bit(Cpu.REGISTER_PC_ADDRESS, addr)

