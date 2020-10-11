# Chip8 Emulator

Chip8 emulator implemented in Python 3.

It implements a COSMIC VIP with the original 36 instructions and with 4 KB of memory.

## Architecture

### CPU

Instructions are 16-bit long.

### Memory

This [COSMIC VIP](https://github.com/Chromatophore/HP48-Superchip/blob/master/investigations/quirk_memlimit.md) implementation divides the memory as following:

* 0x00 to 0x1FF (512 bytes): reserved to Chip8 implementation (here is empty, maybe I will put the actually code available [here](https://archive.org/details/bitsavers_rcacosmacCManual1978_6956559/page/n35/mode/2up)):
  * 0x000 to 0x050: builtin fonts for hexadecimal digits (0 to F) of 5 bytes long (8x5 pixels)
* 0x200 to 0xE9F (3,232 bytes): memory to program code;
* 0xEA0 to 0xEFF (96 bytes): memory reserved internal user:
  * 0xEA0 to 0xEBF (32 bytes): stack;
  * 0xED0 to 0xEEF (32 bytes): registers (`I`, `PC`, `SP`, `DT`, `ST`):
    * 0xED0: register `PC`
    * 0xED2: register `I`
    * 0xED4: register `SP`
    * 0xED5: register `DT`
    * 0xED6: register `ST`
    * 0xED9: random number
    * Note: this address was defined by manual intepretention (see COSMAC VIP Instruction Manual p 15).
  * 0xEF0 to 0xEFF (16 bytes): data registers (from `V0` to `VF`).
* 0xF00 to 0xFFF (256 bytes): reserved to display refresh.

```
'-' 0xFFF - end of memory
 |
 | (registers and stack)
 |
'-' 0xEA0 - start of reserved area to internal use
 |
 |
 | (program code)
 |
 |
 |
'-' 0x200 - start of program memory (instructions and variables)
 |
 |  (reserved to Chip8 interpreter code)
 |
'-' 0x81 - interpreter reserved memory start
 |
'-' 0x00 - builtin font reserved memory start
```

## Notes about COSMIC VIP implementation

* Instructions `8XY6` and `8XYE` use `VY`, see [here](https://github.com/Chromatophore/HP48-Superchip#8xy6--8xye-aka-x--y-x--y).

## TODO

* [ ] CPU
    * [x] Handle `SP`
    * [x] Handle `V0` to `VF`
    * [x] Handle `PC`
    * [x] Handle `I`
    * [ ] Handle `DT`
    * [ ] Handle `ST`
    * [ ] Implement cycle
* [ ] Memory
    * [x] Memory: bultin fonts
    * [x] Memory: verify if needs to reserve memory for call stack and registers (`I`, `PC`, `SP`, `V0` to `VF`)
    * [x] Move logic to update register to `Cpu` class
* [ ] Screen
* [ ] Keyboard
* [ ] Rom reader

## Links

* [Study of the techniques for emulation programming](http://www.codeslinger.co.uk/files/emu.pdf)
* [Unified Chip8 Documentation (Best one)](https://github.com/trapexit/chip-8_documentation)
* [Wiki](https://en.wikipedia.org/wiki/CHIP-8)
* [Cowgod's Chip8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0)
* [Mastering Chip8](http://mattmik.com/files/chip8/mastering/chip8.html)
* [Programming in Chip-8 - EIT ed Nov 1981](https://archive.org/stream/ETIA1981/ETI%201981-11%20November#page/n113/mode/2up))
* [Doc with Interesting Comments](https://github.com/Chromatophore/HP48-Superchip)
* [Chip8 Technical Reference](https://github.com/mattmikolay/chip-8/wiki/CHIP%E2%80%908-Technical-Reference)
* [Emulating Chip8 System](http://www.codeslinger.co.uk/pages/projects/chip8.html)
* [Chip8 Classic Manual](https://storage.googleapis.com/wzukusers/user-34724694/documents/5c83d6a5aec8eZ0cT194/CHIP-8%20Classic%20Manual%20Rev%201.3.pdf)
* [Chip8 Emulator](http://vanbeveren.byethost13.com/stuff/CHIP8.pdf)
* [Octo IDE - High level assembler for Chip8 VM](https://github.com/JohnEarnest/Octo)
* [COSMAC VIP Instruction Manual](https://archive.org/details/bitsavers_rcacosmacCManual1978_6956559/page/n1/mode/2up)
* [DREAM 6800 Manual](https://archive.org/stream/EA1979/EA%201979-05%20May#page/n85/mode/2up)

