#!/usr/bin/env python3

from llvmlite import ir


def jit(pgm):
    bit = ir.IntType(1)
    int8 = ir.IntType(8)
    int32 = ir.IntType(32)
    int8ptr = int8.as_pointer()

    module = ir.Module(name="brainfuck_jit")

    fnty = ir.FunctionType(int32, [])
    getchar = ir.Function(module, fnty, name="getchar")
    fnty = ir.FunctionType(ir.VoidType(), [int32])
    putchar = ir.Function(module, fnty, name="putchar")
    memset = module.declare_intrinsic('llvm.memset', [int8ptr, int32])

    fnty = ir.FunctionType(ir.VoidType(), [])
    main = ir.Function(module, fnty, name="main")

    block = main.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    tape = builder.alloca(int32, 30000, name="tape")

    tape8 = builder.ptrtoint(tape, int8)
    tape8 = builder.inttoptr(tape8, int8ptr)
    builder.call(memset, [tape8, int8(0), int32(4 * 30000), bit(0)])

    idx = builder.alloca(int32, name="idx")
    builder.store(int32(0), idx)

    bracket_blocks = []

    for opcode in pgm:
        if opcode == '>':
            # idx++
            idxval = builder.load(idx, "idxval")
            inc = builder.add(idxval, int32(1), name="inc")
            builder.store(inc, idx)

        elif opcode == '<':
            # idx--
            idxval = builder.load(idx, "idxval")
            dec = builder.add(idxval, int32(-1), name="dec")
            builder.store(dec, idx)

        elif opcode == '+':
            # tape[idx] +=1
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')
            incr = builder.add(data, int32(1), name="incr")
            builder.store(incr, el)

        elif opcode == '-':
            # tape[idx] -=1
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')
            incr = builder.add(data, int32(-1), name="incr")
            builder.store(incr, el)

        elif opcode == '[':
            # while tape[idx] != 0:
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')

            inner = main.append_basic_block(name='inner')
            after = main.append_basic_block(name='after')
            cmp = builder.icmp_signed('!=', data, int32(0))
            builder.cbranch(cmp, inner, after)

            # next instructions are written inside the loop now
            builder.position_at_start(inner)
            bracket_blocks.append(after)

        elif opcode == ']':
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')

            cmp = builder.icmp_signed('!=', data, int32(0))
            inner = builder.block
            after = bracket_blocks.pop()
            builder.cbranch(cmp, inner, after)

            builder.position_at_start(after)
    
        elif opcode == '.':
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')
            builder.call(putchar, [data])

        elif opcode == ',':
            # TODO: don't think this is correct
            data = builder.call(getchar)
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            builder.store(data, el)

    print(module)