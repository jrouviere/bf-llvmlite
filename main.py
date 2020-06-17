#!/usr/bin/env python3

from interpreter import interpret
from jit import jit
from jit_link import run

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=str, help="program to be run")
    parser.add_argument("--interpret", help="Use the interpreter instead of the jit", action="store_true")
    parser.add_argument("-o", "--optlevel", help="Optimisation level", type=int, default=2)
    parser.add_argument("-v", "--verbose", help="Verbose: print out llvm-ir", action="store_true")
    args = parser.parse_args()

    pgm = open(args.program).read()

    if args.interpret:
        interpret(pgm)
    else:
        ir = jit(pgm)
        run(str(ir), args.optlevel, args.verbose)
