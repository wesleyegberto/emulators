from Cpu import Cpu

print("Chip8 Emulator")

def main():
    cpu = Cpu()
    cpu.plot_char(0x5)

    # 1 - execute CPU clock
    # 2 - generate interrupts
    # 3 - emulate graphics
    # 4 - emulate sound


if __name__ == "__main__":
    main()
