#!/usr/bin/env python3

import sys

# naive interpreter
def interpret(pgm):
    array = [0,] *30000
    pc = 0
    ptr = 0

    while True:
        c = pgm[pc]

        if c == '>':
            ptr += 1
        elif c == '<':
            ptr -= 1
        elif c == '+':
            array[ptr] +=1
        elif c == '-':
            array[ptr] -=1
        elif c == '.':
            sys.stdout.write(chr(array[ptr]))
        elif c == ',':
            array[ptr] = sys.stdin.read(1)
        elif c == '[':
            if array[ptr] == 0:
                # jump to matching ']'
                pc = match_close(pgm, pc)
        elif c == ']':
            if array[ptr] != 0:
            # jump to matching '['
                pc = match_open(pgm, pc)

        pc += 1
        if pc >= len(pgm):
            return


def match_open(pgm, pc):
    depth = 0
    
    while True:
        c = pgm[pc]
        if c == '[':
            depth -= 1
        elif c == ']':
            depth += 1

        if depth == 0:
            return pc

        pc -= 1

def match_close(pgm, pc):
    depth = 0

    while True:
        c = pgm[pc]
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1

        if depth == 0:
            return pc

        pc += 1