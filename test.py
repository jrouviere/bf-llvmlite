#!/usr/bin/env python3

from interpreter import interpret
from jit import jit
from jit_link import run


test0 = "+++."

test1 = """
++++ ++++
[
> +++ +++
< -
]
> .
"""

test2 = """
++++++++ ++++++++ ++++++++ ++++++++ ++++++++ ++++++++

>+++++
[<+.>-]
"""

test3 = "+[[][]]"

helloworld = """
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
"""


import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

if __name__ == '__main__':
    ir = jit(helloworld)

    run(str(ir))
