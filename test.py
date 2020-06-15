#!/usr/bin/env python3

from interpreter import interpret
from jit import jit


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

helloworld = """
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
"""

if __name__ == '__main__':
    interpret(test2)
    jit(test2)

