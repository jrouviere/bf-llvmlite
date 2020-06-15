#!/usr/bin/env python3

from llvmlite import ir


def jit(pgm):
    bit = ir.IntType(1)
    int8 = ir.IntType(8)
    int32 = ir.IntType(32)
    int64 = ir.IntType(64)
    int8ptr = int8.as_pointer()

    module = ir.Module(name="brainfuck_jit")

    fnty = ir.FunctionType(int32, [])
    getchar = ir.Function(module, fnty, name="getchar")
    fnty = ir.FunctionType(ir.VoidType(), [int32])
    putchar = ir.Function(module, fnty, name="putchar")
    memset = module.declare_intrinsic('llvm.memset', [int8ptr, int32])

    fnty = ir.FunctionType(ir.VoidType(), [])
    bfrun = ir.Function(module, fnty, name="bfrun")

    block = bfrun.append_basic_block(name="entry")
    builder = ir.IRBuilder(block)

    tape = builder.alloca(int32, 30000, name="tape")

    tape_ptr = builder.ptrtoint(tape, int64)
    tape8 = builder.inttoptr(tape_ptr, int8ptr)
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
            decr = builder.add(data, int32(-1), name="decr")
            builder.store(decr, el)

        elif opcode == '[':
            # while tape[idx] != 0:
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')
            cmp = builder.icmp_signed('!=', data, int32(0))

            inner = bfrun.append_basic_block(name='inner')
            after = ir.Block(parent=bfrun, name='after')
            builder.cbranch(cmp, inner, after)

            # next instructions are written inside the loop now
            builder.position_at_start(inner)

            # save the "after" block for later
            bracket_blocks.append((inner, after))

        elif opcode == ']':
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')
            cmp = builder.icmp_signed('!=', data, int32(0))

            # blocks saved from matching '['
            inner, after = bracket_blocks.pop()
            builder.cbranch(cmp, inner, after)

            bfrun.blocks.append(after)
            builder.position_at_start(after)
    
        elif opcode == '.':
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            data = builder.load(el, 'data')
            builder.call(putchar, [data])

        elif opcode == ',':
            # TODO: don't think this is correct
            data = builder.call(getchar, [])
            idxval = builder.load(idx, "idxval")
            el = builder.gep(tape, [idxval], name="el")
            builder.store(data, el)

    builder.ret_void()
    return module
