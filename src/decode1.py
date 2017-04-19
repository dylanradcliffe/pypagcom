#!/usr/bin/env python
import sys

with open(sys.argv[1], "rb") as f:
    word = f.read(2)
    addr = 0o4000
    while word:
        wordval = int.from_bytes(word, byteorder='big') // 2
        print (oct(addr), oct(wordval))
        word = f.read(2)
        addr = addr + 1
