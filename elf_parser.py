import argparse
import sys

fileName = ''

class elfHeaderClass:
    e_indent = ''
    e_type = ''
    e_machine = ''
    e_version = ''
    e_entry = ''
    e_phoff = ''
    e_shoff = ''
    e_flags = ''
    e_ehsize = ''
    e_phentsize = ''
    e_phnum = ''
    e_shentsize = ''
    e_shnum = ''
    e_shstrndx = ''

def elfHeader():
    offset = 0


    file = open(fileName, 'rb')

    chunk = file.read(16)
    offset += 16
    e_indent = chunk.encode('hex')

    print(e_indent)



def main():
    global fileName

    argumentParser = argparse.ArgumentParser("Elf parser.")
    argumentParser.add_argument('file', nargs=1, metavar='elf file')
    argumentParser.add_argument('-e', '--elf-header', action='store_true')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    args = argumentParser.parse_args()
    fileName = ''.join(args.file)

    if len(sys.argv) <= 2 or args.elf_header:
        elfHeader()

if __name__ == "__main__":
    main()