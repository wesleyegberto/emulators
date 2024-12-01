from Cpu import Cpu
from Display import Display
from Keyboard import Keyboard
from Memory import Memory

print("Chip8 Emulator")

def main():
    memory = Memory()
    display = Display(memory)
    display.initialize()
    keyboard = Keyboard()

    cpu = Cpu(memory, display, keyboard)

    # test program
    memory.write_16bit(0x200, 0xA216)

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

    memory.write_16bit(0x214, 0x1214)
    memory.write_16bit(0x216, 0xFF99)
    memory.write_16bit(0x218, 0xFF99)
    memory.write_16bit(0x21A, 0xFF00)
    memory.write_16bit(0x21C, 0xC0C0)

    cpu.start()

if __name__ == "__main__":
    main()
