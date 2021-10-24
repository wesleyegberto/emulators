from Cpu import Cpu

print("Chip8 Emulator")

def main():
    cpu = Cpu()
    cpu.plot_char(0x5)

if __name__ == "__main__":
    main()
