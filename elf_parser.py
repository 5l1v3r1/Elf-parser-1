import argparse
import sys
from struct import *

fileName = ''
fileClassID = ''

fileTypes = {0:'No file type', 1:'Relocatable object file', 2:'Executable file', 3:'Shared object file', 4:'Core file'}
machines = {3:'Intel 80386', 62:'AMD x86-64 architecture'}
versions = {0:'Invalid version', 1:'Current version'}
datas = {1:'Little-endian', 2:'Big-endian'}
classes = {1:'32-bit objects', 2:'64-bit objects'}

sectionTypes = {0:'SHT_NULL', 1:'SHT_PROGBITS', 2:'SHT_SYMTAB', 3:'SHT_STRTAB', 4:'SHT_RELA', 5:'SHT_HASH', 6:'SHT_DYNAMIC', 7:'SHT_NOTE', 8:'SHT_NOBITS', 9:'SHT_REL', 10:'SHT_SHLIB', 11:'SHT_DYNSYM', 14:'SHT_INIT_ARRAY', 15:'SHT_FINI_ARRAY', 16:'SHT_PREINIT_ARRAY', 17:'SHT_GROUP', 18:'SHT_SYMTAB_SHNDX', 19:'SHT_NUM'}
sectionFlags = {0:'', 1:'SHF_WRITE', 2:'SHF_ALLOC', 3:'SHF_EXECINSTR'}
sectionInfos = {}

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

class sectionHeaderClass:
    sh_name = ''
    sh_type = ''
    sh_flags = ''
    sh_addr = ''
    sh_offset = ''
    sh_size = ''
    sh_link = ''
    sh_info = ''
    sh_addralign = ''
    sh_entsize = ''

curElfHeader = elfHeaderClass()
curSectionHeader = []

def elfHeaderParser():
    global curElfHeader
    global fileClassID
    offset = 0
    decimalValue = 0

    file = open(fileName, 'rb')

    for i in range(16):
        chunk = file.read(1)
        offset += 1
        curElfHeader.e_indent.append(chunk.encode('hex'))

    if not magicalCheck():
        file.close()
        exit()

    fileClassID = int(curElfHeader.e_indent[4], 16)

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_type = fileTypes[decimalValue]

    chunk = file.read(2)
    offset += 2
    decimalValue = unpack('H', chunk)[0]
    curElfHeader.e_machine = machines[decimalValue]

    chunk = file.read(4)
    offset += 4
    decimalValue = unpack('I', chunk)[0]
    curElfHeader.e_version = versions[decimalValue]

    if fileClassID == 1:
        for i in range(4):
            chunk = file.read(1)
            offset += 1
            curElfHeader.e_entry = chunk.encode('hex') + curElfHeader.e_entry

        curElfHeader.e_entry = '0x' + curElfHeader.e_entry

        for i in range(4):
            chunk = file.read(1)
            offset += 1
            curElfHeader.e_phoff = chunk.encode('hex') + curElfHeader.e_phoff

        curElfHeader.e_phoff = '0x' + curElfHeader.e_phoff

        for i in range(4):
            chunk = file.read(1)
            offset += 1
            curElfHeader.e_shoff = chunk.encode('hex') + curElfHeader.e_shoff

        curElfHeader.e_shoff = '0x' + curElfHeader.e_shoff
    else:
        for i in range(8):
            chunk = file.read(1)
            offset += 1
            curElfHeader.e_entry = chunk.encode('hex') + curElfHeader.e_entry

        curElfHeader.e_entry = '0x' + curElfHeader.e_entry

        for i in range(8):
            chunk = file.read(1)
            offset += 1
            curElfHeader.e_phoff = chunk.encode('hex') + curElfHeader.e_phoff

        curElfHeader.e_phoff = '0x' + curElfHeader.e_phoff

        for i in range(8):
            chunk = file.read(1)
            offset += 1
            curElfHeader.e_shoff = chunk.encode('hex') + curElfHeader.e_shoff

        curElfHeader.e_shoff = '0x' + curElfHeader.e_shoff

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

    if offset != curElfHeader.e_ehsize:
        file.close()
        exit()
    file.close()

def magicalCheck():
    check = False
    magicNumber = ''

    for i in range(4):
        magicNumber += curElfHeader.e_indent[i]

    if magicNumber == '7f454c46':
        check = True

    return check

def sectionHeaderParser():
    if not curElfHeader:
        exit()
    
    offset = 0
    chunk = ''
    decimalValue = 0
    headerOffset = int(curElfHeader.e_shoff, 16)

    entryCount = curElfHeader.e_shnum
    entrySize = curElfHeader.e_shentsize

    file = open(fileName, 'rb')
    file.seek(headerOffset)

    for i in range(entryCount):
        curSectionHeader.append(sectionHeaderClass())
        index = len(curSectionHeader) - 1

        chunk = file.read(4)
        offset += 4
        decimalValue = unpack('I', chunk)[0]
        curSectionHeader[index].sh_name = decimalValue

        chunk = file.read(4)
        offset += 4
        decimalValue = unpack('I', chunk)[0]
        if decimalValue <= 19:
            curSectionHeader[index].sh_type = sectionTypes[decimalValue]
        else:
            curSectionHeader[index].sh_type = 'PROGBITS'

        if fileClassID == 1:
            chunk = file.read(4)
            offset += 4
            decimalValue = unpack('I', chunk)[0]
            curSectionHeader[index].sh_flags = decimalValue

            for i in range(4):
                chunk = file.read(1)
                offset += 1
                curSectionHeader[index].sh_addr = chunk.encode('hex') + curSectionHeader[index].sh_addr
            
            curSectionHeader[index].sh_addr = '0x' + curSectionHeader[index].sh_addr
            
            for i in range(4):
                chunk = file.read(1)
                offset += 1
                curSectionHeader[index].sh_offset = chunk.encode('hex') + curSectionHeader[index].sh_offset
            
            curSectionHeader[index].sh_offset = '0x' + curSectionHeader[index].sh_offset

            chunk = file.read(4)
            offset += 4
            decimalValue = unpack('I', chunk)[0]
            curSectionHeader[index].sh_size = decimalValue
        else:
            chunk = file.read(8)
            offset += 8
            decimalValue = unpack('Q', chunk)[0]
            curSectionHeader[index].sh_flags = decimalValue

            for i in range(8):
                chunk = file.read(1)
                offset += 1
                curSectionHeader[index].sh_addr = chunk.encode('hex') + curSectionHeader[index].sh_addr
            
            curSectionHeader[index].sh_addr = '0x' + curSectionHeader[index].sh_addr

            for i in range(8):
                chunk = file.read(1)
                offset += 1
                curSectionHeader[index].sh_offset = chunk.encode('hex') + curSectionHeader[index].sh_offset
            
            curSectionHeader[index].sh_offset = '0x' + curSectionHeader[index].sh_offset

            chunk = file.read(8)
            offset += 8
            decimalValue = unpack('Q', chunk)[0]
            curSectionHeader[index].sh_size = decimalValue

        for i in range(4):
            chunk = file.read(1)
            offset += 1
            curSectionHeader[index].sh_link = chunk.encode('hex') + curSectionHeader[index].sh_link
        
        curSectionHeader[index].sh_link = '0x' + curSectionHeader[index].sh_link

        chunk = file.read(4)
        offset += 4
        decimalValue = unpack('I', chunk)[0]
        curSectionHeader[index].sh_info = decimalValue

        if fileClassID == 1:
            chunk = file.read(4)
            offset += 4
            decimalValue = unpack('I', chunk)[0]
            curSectionHeader[index].sh_addralign = decimalValue

            chunk = file.read(4)
            offset += 4
            decimalValue = unpack('I', chunk)[0]
            curSectionHeader[index].sh_entsize = decimalValue
        else:
            chunk = file.read(8)
            offset += 8
            decimalValue = unpack('Q', chunk)[0]
            curSectionHeader[index].sh_addralign = decimalValue

            chunk = file.read(8)
            offset += 8
            decimalValue = unpack('Q', chunk)[0]
            curSectionHeader[index].sh_entsize = decimalValue

    if len(curSectionHeader) != curElfHeader.e_shnum or offset != (curElfHeader.e_shnum * curElfHeader.e_shentsize):
        file.close()
        exit()
    else:
        stringTableParser()
    file.close()

def stringTableParser():
    offset = 0
    tableSectionIndex = int(curElfHeader.e_shstrndx)
    tableOffset = int(curSectionHeader[tableSectionIndex].sh_offset, 16)
    size = int(curSectionHeader[tableSectionIndex].sh_size)
    chunk = ''
    decimalValue = 0
    strValue = ''

    file = open(fileName, 'rb')

    for i in curSectionHeader:
        strOffset = int(i.sh_name)
        file.seek(tableOffset + strOffset)

        while chunk != '\0':
            chunk = file.read(1)
            if(chunk != '\0'):
                strValue += chunk
        
        i.sh_name = strValue
        strValue = ''
        chunk = ''


    file.seek(tableOffset)

"""     while offset < size:
        chunk = file.read(1)
        offset += 1
        if chunk.encode('hex') == '\0':
            while chunk != '\0':
                chunk = file.read(1)
                offset += 1
                if chunk != '\0':
                    strValue += unpack('c')[0]
            curStringSection.append(strValue)
            strValue = ''
                    

        curStringSection.append() """

def elfHeaderPrinter():
    magicSeq = ''
    for i in range(4):
        magicSeq += curElfHeader.e_indent[i] + ' '

    print 
    print 'Elf Header of {}:'.format(fileName)
    print
    print ('{:<50}' + magicSeq).format('Magic number:')
    print ('{:<50}' + classes[int(curElfHeader.e_indent[4], 16)]).format('File class:')
    print ('{:<50}' + datas[int(curElfHeader.e_indent[5], 16)]).format('Data encoding:')
    print ('{:<50}' + versions[int(curElfHeader.e_indent[6], 16)]).format('File version:')
    print ('{:<50}' + str(curElfHeader.e_type)).format('Object file type:')
    print ('{:<50}' + str(curElfHeader.e_machine)).format('Machine type:')
    print ('{:<50}' + str(curElfHeader.e_version)).format('Object file version:')
    print ('{:<50}' + str(curElfHeader.e_entry)).format('Entry point address:')
    print ('{:<50}' + str(curElfHeader.e_phoff)).format('Program header offset:')
    print ('{:<50}' + str(curElfHeader.e_shoff)).format('Section header offset:')
    print ('{:<50}' + str(curElfHeader.e_flags)).format('Processor-specific flags:')
    print ('{:<50}' + str(curElfHeader.e_ehsize)).format('ELF header size:')
    print ('{:<50}' + str(curElfHeader.e_phentsize)).format('Size of the program header entry:')
    print ('{:<50}' + str(curElfHeader.e_phnum)).format('Number of program header entries:')
    print ('{:<50}' + str(curElfHeader.e_shentsize)).format('Size of section header entry:')
    print ('{:<50}' + str(curElfHeader.e_shnum)).format('Number of section header entries:')
    print ('{:<50}' + str(curElfHeader.e_shstrndx)).format('Section name string table index:')

def sectionHeaderPrinter():
    index = 0

    print 
    print 'Section Header of {}:'.format(fileName)
    print
    print ('{0:<5}{1:<21}{2:<17}{3:<8}{4:<21}{5:<21}{6:<7}{7:<13}{8:<7}{9:<12}{10:<0}').format('No', 'Name', 'Type', 'Flags', 'Address', 'Offset', 'Size', 'Link', 'Info', 'Alignment', 'EntSize')
    print ('{0:<5}{4:<21}{2:<17}{3:<8}{4:<21}{4:<21}{5:<7}{6:<13}{5:<7}{7:<12}{8:<0}').format('--', '--------', '--------------', '-----', '------------------', '----', '----------', '---------', '-------')

    for i in curSectionHeader:
        print ('{0:<5}{1:<21}{2:<17}{3:<8}{4:<21}{5:<21}{6:<7}{7:<13}{8:<7}{9:<12}{10:<13}').format(index, i.sh_name, i.sh_type, i.sh_flags, i.sh_addr, i.sh_offset, i.sh_size, i.sh_link, i.sh_info, i.sh_addralign, i.sh_entsize)
        index += 1

def sign():
    print
    print "             ___   ___  _   _             "
    print "            / _ \ / _ \| | | |            "
    print "       _ __| | | | | | | |_| |_ ___ _ __  "
    print "      | '__| | | | | | | __| __/ _ \ '_ \ "
    print "      | |  | |_| | |_| | |_| ||  __/ | | |"
    print "      |_|   \___/ \___/ \__|\__\___|_| |_|"
    print
    print "{:^}".format('Elf parser by Mert Degirmenci')
    print '___________________________________________________'

def main():
    sign()
    global fileName

    argumentParser = argparse.ArgumentParser("Elf parser.")
    argumentParser.add_argument('file', nargs=1, metavar='elf file')
    argumentParser.add_argument('-e', '--elf-header', action='store_true')
    argumentParser.add_argument('-s', '--section-header', action='store_true')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    args = argumentParser.parse_args()
    fileName = ''.join(args.file)

    elfHeaderParser()

    if len(sys.argv) == 2 or args.elf_header:
        elfHeaderPrinter()
    if args.section_header:
        sectionHeaderParser()
        sectionHeaderPrinter()

if __name__ == "__main__":
    main()