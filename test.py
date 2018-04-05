#!/usr/bin/python3
from lexer import Tokenizer
import sys

"""Script to test the lexer

Outputs a list of formated tokens for each file passed as input 
Usage:
    test.py [list-of-files]
"""

for filename in sys.argv[1:]:
    print(filename + ":")
    with open(filename) as f:
        target = f.read()
        tokenizer = Tokenizer(target)
        
        while tokenizer.hasToken():
            print(tokenizer.nextToken())

        print()
