from Cpu import Cpu
from Display import Display
from Keyboard import Keyboard
from Memory import Memory
from Sound import Sound

print("Chip8 Emulator")

def main():
    memory = Memory()
    keyboard = Keyboard()
    display = Display(memory)
    display.initialize()
    sound = Sound()

    cpu = Cpu(memory, display, keyboard, sound)

    load_print_font_program(memory)
    # load_screen_warp_program(memory)
    # load_delay_timer_program(memory)

    # load_rom_file_into_memory('roms/delay_timer_test.ch8', memory)

    cpu.start()

def load_print_font_program(memory: Memory):
    addr = Cpu.MEMORY_PROGRAM_CODE_AREA_START_ADDRESS
    memory.write_16bit(addr, 0xA000 + (5 * 9))
    addr += 2
    memory.write_16bit(addr, 0x6100)
    addr += 2
    memory.write_16bit(addr, 0x6200)
    addr += 2
    memory.write_16bit(addr, 0xD125)
    addr += 2
    memory.write_16bit(addr, 0x6104)
    addr += 2
    memory.write_16bit(addr, 0x6200)
    addr += 2
    memory.write_16bit(addr, 0xD125)
    addr += 2
    memory.write_16bit(addr, 0x1000 + addr)


def load_screen_warp_program(memory: Memory):
    memory.write_16bit(0x200, 0xA222)

    # dot warped in the 4 corners
    # memory.write_16bit(0x200, 0xA21C)
    # memory.write_16bit(0x202, 0x613F)
    # memory.write_16bit(0x204, 0x621F)
    # memory.write_16bit(0x206, 0xD122)
    # memory.write_16bit(0x208, 0x1208)

    memory.write_16bit(0x202, 0x6100)
    memory.write_16bit(0x204, 0x6200)
    memory.write_16bit(0x206, 0xD125)
    memory.write_16bit(0x208, 0x1208)

    memory.write_16bit(0x208, 0x613F)
    memory.write_16bit(0x20A, 0x6205)
    memory.write_16bit(0x20C, 0xD125)
    memory.write_16bit(0x20E, 0x6138)
    memory.write_16bit(0x210, 0x621D)
    memory.write_16bit(0x212, 0xD125)

    memory.write_16bit(0x214, 0x6803)
    memory.write_16bit(0x216, 0xF818)

    memory.write_16bit(0x218, 0x1218)

    memory.write_16bit(0x222, 0xFF99)
    memory.write_16bit(0x224, 0xFF99)
    memory.write_16bit(0x226, 0xFF00)
    memory.write_16bit(0x228, 0xC0C0)

def read_rom_file(file) -> str:
    with open(file, 'rb') as f:
        return f.read().hex()

def load_rom_file_into_memory(filename: str, memory: Memory):
    rom_data = read_rom_file(filename)

    rom_data_lines = ''

    i = 0
    for l in rom_data:
        i += 1
        rom_data_lines += l
        if i >= 4:
            rom_data_lines += '\n'
            i = 0

    load_rom_into_memory(rom_data_lines, memory)

def load_rom_into_memory(rom_data: str, memory: Memory):
    print('\n=== Reading Rom ===')
    addr = Cpu.MEMORY_PROGRAM_CODE_AREA_START_ADDRESS
    for line in rom_data.split('\n'):
        if len(line.strip()) == 0:
            continue
        data = int(line.strip(), 16)
        print(f'\t{hex(addr)} === {hex(data)}')

        memory.write_16bit(addr, data)
        addr += 2
    print('=== Finished ===\n')

def load_delay_timer_program(memory: Memory):
    # Program to test timer delay (2 to increase, 8 to decrease, 5 to start counting down)
    rom_data = '''6400
    221E
    F50A
    4502
    7601
    4508
    76FF
    3505
    1202
    F615
    F607
    221E
    3600
    1214
    1202
    00E0
    A23A
    F633
    F265
    6300
    F029
    D345
    7305
    F129
    D345
    7305
    F229
    D345
    00EE'''

    load_rom_into_memory(rom_data, memory)

if __name__ == "__main__":
    main()

