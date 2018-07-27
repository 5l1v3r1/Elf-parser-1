# Elf-parser

_This project under development._

### Description:

This project aims to validate and parse properly Intel 80386 and AMD x86-64 architecture elf files. According to Wikipedia, Elf is:

>In computing, the Executable and Linkable Format (ELF, formerly named Extensible Linking Format), is a common standard file format for executable files, object code, shared libraries, and core dumps.

With the last commit of time, it has functinality to parse Elf Header, Section Header and String Tables.

```
Elf Header of empty:

Magic number:                                     7f 45 4c 46
File class:                                       64-bit objects
Data encoding:                                    Little-endian
File version:                                     Current version
Object file type:                                 Shared object file
Machine type:                                     AMD x86-64 architecture
Object file version:                              Current version
Entry point address:                              0x0000000000001040
Program header offset:                            0x0000000000000040
Section header offset:                            0x0000000000003908
Processor-specific flags:                         0
ELF header size:                                  64
Size of the program header entry:                 56
Number of program header entries:                 11
Size of section header entry:                     64
Number of section header entries:                 29
Section name string table index:                  28
```

### Usage:

You can clone it and fire up immediately. The only requirement is Python 2.7

```
             ___   ___  _   _
            / _ \ / _ \| | | |
       _ __| | | | | | | |_| |_ ___ _ __
      | '__| | | | | | | __| __/ _ \ '_ \
      | |  | |_| | |_| | |_| ||  __/ | | |
      |_|   \___/ \___/ \__|\__\___|_| |_|

Elf parser by Mert Degirmenci
___________________________________________________
usage: Elf parser. [-h] [-e] [-s] elf file

positional arguments:
  elf file

optional arguments:
  -h, --help            show this help message and exit
  -e, --elf-header
  -s, --section-header
```

### Process

The development phase continues at full speed and it has been aimed to be finished very soon.

