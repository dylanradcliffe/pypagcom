#!/usr/bin/env python
import sys
from pyagcom import instruction

with open(sys.argv[1], "rb") as f:
    word = f.read(2)
    addr = 0o4000
    extend = False
    while word:
        wordval = int.from_bytes(word, byteorder='big') 
        #code, qc, addr, p = instruction.base_instruction.decode(wordval)
        instr = instruction.instruction.from_word(wordval, extend)
        print ("%05o\t%05o\t%s" % (addr, wordval//2, str(instr)))
        extend = instr.extend
        word = f.read(2)
        addr = addr + 1
