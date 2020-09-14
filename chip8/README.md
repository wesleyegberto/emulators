# Chip8 Emulator

Chip8 emulator implemented in Python 3.

It implements a VIPs with the original 36 instructions and with 4 KB of memory.

## Architecture

### Memory

This implementation divides the memory as following:

* 0x00 to 0x1FF (512 bytes): reserved to Chip8 implementation (here is empty, maybe I will put the actually code available [here](https://archive.org/details/bitsavers_rcacosmacCManual1978_6956559/page/n35/mode/2up)):
  * 0x000 to 0x050: builtin fonts for hexadecimal digits (0 to F) of 5 bytes long (8x5 pixels)
* 0x200 to 0xE9F (3,232 bytes): memory to program code;
* 0xEA0 to 0xEFF (96 bytes): memory reserved internal user:
  * 0xEA0 to 0xECF (48 bytes): stack;
  * 0xEC0 to 0xEBF (47 bytes): registers (`I`, `PC`, `SP`, `DT`, `ST`, `V0` to `VF`):
    * 0xED0: register `PC`
    * 0xED1: register `SP`
    * 0xED2: register `I`
    * 0xED3: register `DT`
    * 0xED4: register `ST`
* 0xF00 to 0xFFF (256 bytes): reserved to display refresh.

```
'-' 0xFFF - end of memory
 |
 | (registers and stack)
 |
'-' 0xE9F - start of reserved area to internal use
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
 |
'-' 0x00 - interpreter reserved memory start
```

## TODO

* [ ] CPU
    * [ ] Handle `PC`
    * [ ] Handle `SP`
    * [ ] Handle `I`
    * [ ] Handle `V0` to `VF`
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
* [Wiki](https://en.wikipedia.org/wiki/CHIP-8)
* [History](http://vanbeveren.byethost13.com/stuff/CHIP8.pdf?i=1)
* [Cowgod's Chip8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0)
* [Mastering Chip8](http://mattmik.com/files/chip8/mastering/chip8.html)
* [Doc Chip8](https://github.com/trapexit/chip-8_documentation)
* [Chip8 Technical Reference](https://github.com/mattmikolay/chip-8/wiki/CHIP%E2%80%908-Technical-Reference)
* [Emulating Chip8 System](http://www.codeslinger.co.uk/pages/projects/chip8.html)
* [Octo IDE - High level assembler for Chip8 VM](https://github.com/JohnEarnest/Octo)
* [Chip8 Classic Manual](https://storage.googleapis.com/wzukusers/user-34724694/documents/5c83d6a5aec8eZ0cT194/CHIP-8%20Classic%20Manual%20Rev%201.3.pdf)

