# Memory area reserved for builtin fonts
MEMORY_FONT_AREA_START_ADDRESS = 0x000
MEMORY_FONT_AREA_END_ADDRESS = 0x050

class Memory:
    """ Memory with 4 KB

    The memory has the layout with big-endian.
    The memory is read/written using AND 0xFF to enforce byte size.
    """
    MEMORY_SIZE = 4096

    def __init__(self):
        """ Initialize the memory with 0x000

        Initialize the builtin fonts from 0x00 to 0x80
        """

        self.memory = [0] * 4096

        # each digit is 5 bytes long (8x5 pixels)
        self.memory[MEMORY_FONT_AREA_START_ADDRESS:MEMORY_FONT_AREA_END_ADDRESS] = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0x0 => 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 0x5 => 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 0xA => 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 0xF => 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 0x14 => 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 0x19 => 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 0x1E => 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 0x23 => 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 0x28 => 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 0x2D => 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # 0x32 => A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # 0x37 => B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # 0x3C => C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # 0x41 => D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # 0x46 => E
            0xF0, 0x80, 0xF0, 0x80, 0x80, # 0x4B => F
        ]


    def write_8bit(self, address, value):
        # print(f'\tWriting {hex(value)} at address {hex(address)}')
        """ Store a 8-bit value at given address. """
        self.memory[address] = value & 0xFF

    def read_8bit(self, address):
        """ Read a 8-bit value from given address. """
        return self.memory[address] & 0xFF

    def write_16bit(self, address, value):
        """ Store a 16-bit value into two 8-bit cells starting at given address. """

        self.memory[address] = (value >> 8) & 0xFF
        address = address + 1
        self.memory[address] = value & 0xFF
        # print(f'Memory {hex(self.memory[address - 1])} {hex(self.memory[address])}')

    def read_16bit(self, address):
        """ Read a 16-bit value from two 8-bit cells starting at given address. """

        val = (self.memory[address] & 0xFF) << 8
        address = address + 1
        return val | (self.memory[address] & 0xFF)

    def read_range(self, offset, number_bytes):
        return self.memory[offset:(offset + number_bytes)]

