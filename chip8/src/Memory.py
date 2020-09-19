
class Memory:
    MEMORY_SIZE = 4096

    """ Memory with 4 KB """

    def __init__(self):
        """ Initialize the memory with 0x000

        Initialize the builtin fonts
        """

        self.memory = [0] * 4096

        # each digit is 5 bytes long (8x5 pixels)
        self.memory[:80] = [
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x80, 0x80, 0x80, 0xF0, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80, # F
        ]


    def write_8bit(self, address, value):
        """ Store a 8-bit value at address. """
        self.memory[address] = value & 0xFF

    def read_8bit(self, address):
        return self.memory[address]

    def write_16bit(self, address, value):
        """ Store a 16-bit value into two 8-bit cells starting at given address. """

        self.memory[address] = (value >> 8) & 0xFF
        address = address + 1
        self.memory[address] = value & 0xFF

    def read_16bit(self, address):
        """ Read a 16-bit value from two 8-bit cells starting at given address. """

        # TODO: read 2 8-bit cells
        val = (self.memory[address] & 0xFF) << 8
        address = address + 1
        return val | (self.memory[address] & 0xFF)

    def read_range(self, offset, number_bytes):
        return self.memory[offset:(offset + number_bytes)]

