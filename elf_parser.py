import argparse
import sys
from struct import *

fileName = ''

types = {0:'No file type', 1:'Relocatable object file', 2:'Executable file', 3:'Shared object file', 4:'Core file'}
machines = {3:'Intel 80386', 62:'AMD x86-64 architecture'}
versions = {0:'Invalid version', 1:'Current version'}
datas = {1:'Little-endian', 2:'Big-endian'}
classes = {1:'32-bit objects', 2:'64-bit objects'}

class elfHeaderClass:
    e_indent = []
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

curElfHeader = elfHeaderClass()

def elfHeaderParser():
    global curElfHeader
    offset = 0
    decimalValue = 0

    file = open(fileName, 'rb')

    for i in range(16):
        chunk = file.read(1)
        offset += 1
        curElfHeader.e_indent.append(chunk.encode('hex'))

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_type = types[decimalValue]

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_machine = machines[decimalValue]

    chunk = file.read(4)
    offset += 4
    decimalValue = unpack('I', chunk)[0]
    curElfHeader.e_version = versions[decimalValue]

    for i in range(8):
        chunk = file.read(1)
        offset += 1
        curElfHeader.e_entry = chunk.encode('hex') + curElfHeader.e_entry

    curElfHeader.e_entry = '0x' + curElfHeader.e_entry

    chunk = file.read(8)
    offset += 8
    decimalValue = unpack('Q', chunk)[0]
    curElfHeader.e_phoff = decimalValue

    chunk = file.read(8)
    offset += 8
    decimalValue = unpack('Q', chunk)[0]
    curElfHeader.e_shoff = decimalValue

    chunk = file.read(4)
    offset += 4
    decimalValue = unpack('I', chunk)[0]
    curElfHeader.e_flags = decimalValue

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_ehsize = decimalValue

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_phentsize = decimalValue

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_phnum = decimalValue

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_shentsize = decimalValue

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_shnum = decimalValue

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_shstrndx = decimalValue


def elfHeaderPrinter():
    magicSeq = ''
    for i in range(4):
        magicSeq += curElfHeader.e_indent[i] + ' '

    print 
    print 'Elf Header of {}'.format(fileName)
    print
    print ('{:<50}' + magicSeq).format('Magic sequence')
    print ('{:<50}' + classes[int(curElfHeader.e_indent[4], 16)]).format('File class')
    print ('{:<50}' + datas[int(curElfHeader.e_indent[5], 16)]).format('Data encoding')
    print ('{:<50}' + versions[int(curElfHeader.e_indent[6], 16)]).format('File version')
    print ('{:<50}' + str(curElfHeader.e_type)).format('Object file type')
    print ('{:<50}' + str(curElfHeader.e_machine)).format('Machine type ')
    print ('{:<50}' + str(curElfHeader.e_version)).format('Object file version')
    print ('{:<50}' + str(curElfHeader.e_entry)).format('Entry point address')
    print ('{:<50}' + str(curElfHeader.e_phoff)).format('Program header offset')
    print ('{:<50}' + str(curElfHeader.e_shoff)).format('Section header offset')
    print ('{:<50}' + str(curElfHeader.e_flags)).format('Processor-specific flags')
    print ('{:<50}' + str(curElfHeader.e_ehsize)).format('ELF header size')
    print ('{:<50}' + str(curElfHeader.e_phentsize)).format('Size of the program header entry')
    print ('{:<50}' + str(curElfHeader.e_phnum)).format('Number of program header entries')
    print ('{:<50}' + str(curElfHeader.e_shentsize)).format('Size of section header entry')
    print ('{:<50}' + str(curElfHeader.e_shnum)).format('Number of section header entries')
    print ('{:<50}' + str(curElfHeader.e_shstrndx)).format('Section name string table index')


def main():
    global fileName

    argumentParser = argparse.ArgumentParser("Elf parser.")
    argumentParser.add_argument('file', nargs=1, metavar='elf file')
    argumentParser.add_argument('-e', '--elf-header', action='store_true')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    args = argumentParser.parse_args()
    fileName = ''.join(args.file)

    elfHeaderParser()

    if len(sys.argv) == 2 or args.elf_header:
        elfHeaderPrinter()

if __name__ == "__main__":
    main()