# Brainfuck llvmlite

[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) JIT compiler implemented in python with [llvmlite](https://llvmlite.readthedocs.io/en/latest/).

The implementation is heavily inspired by [Eli Bendersky amazing blog](https://eli.thegreenplace.net/2017/adventures-in-jit-compilation-part-3-llvm/).

## Usage

Requires llvmlite, tested with version 0.32.1.

```shell
# Default to optimised JIT compilation:
python main.py tests/mandelbrot.bf

# Run a naive python interpreted version (slow)
python main.py --interpret tests/mandelbrot.bf

# Print out llvm-ir before and after optimisation
python main.py --verbose --optlevel=2 tests/count5.bf
```
