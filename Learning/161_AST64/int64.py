# int64.py
# An interpreter for A64 AST program
#
# 2025-10-12    PV      First version

from ast64 import *

def runA64Program(program: A64Program):
    registers = {'rsp': 100, 'rbp': 0, 'rax': 0, 'rbx': 0, 'rcx': 0, 'rdx': 0, 'rsi': 0, 'rdi': 0,
                 'r8': 0, 'r9': 0, 'r10': 0, 'r11': 0, 'r12': 0, 'r13': 0, 'r14': 0, 'r15': 0}
    stack = {i: 0 for i in range(100, 0, -8)}

    for statement in program:
        match statement:
            case A64Comment(c):
                pass

            case A64Label(l):
                # For now, ignore
                pass

            case A64Instruction(opcode, args):
                match opcode:
                    case 'retq':
                        # For now, simplified version, first return = end program
                        if registers['rsp'] == 100:
                            return
                        else:
                            breakpoint()
                            pass

                    case 'pushq':
                        match args:
                            case [A64OperandRegister64(r)]:
                                stack[registers['rsp']] = registers[r]
                                registers['rsp'] -= 8
                                if registers['rsp'] < 0:
                                    print("Stack overflow")
                            case _:
                                print("Invalid pushq args:", args)

                    case 'popq':
                        match args:
                            case [A64OperandRegister64(r)]:
                                registers['rsp'] += 8
                                if registers['rsp'] > 100:
                                    print("Stack underflow")
                                registers[r] = stack[registers['rsp']]
                            case _:
                                print("Invalid popq args:", args)

                    case 'addq' | 'subq' | 'movq':
                        match args:
                            case [source, dest]:
                                s = None
                                source_from_stack = False
                                source_from_immediate = False
                                match source:
                                    case A64OperandImmediate(n):
                                        s = n
                                        source_from_immediate = True
                                    case A64OperandRegister64(rs):
                                        s = registers[rs]
                                    case A64OperandMemory64(A64OperandRegister64(rbase), displacement, index, scale):
                                        a = registers[rbase] + displacement
                                        if index:
                                            a += registers[index.register] * scale
                                        s = stack[a]
                                        source_from_stack = True
                                    case _:
                                        print(f"Invalid {opcode} source:", source)
                                        continue

                                match dest:
                                    case A64OperandRegister64(rd):
                                        match opcode:
                                            case 'addq':
                                                registers[rd] += s
                                            case 'subq':
                                                registers[rd] -= s
                                            case 'movq':
                                                registers[rd] = s

                                    case A64OperandMemory64(A64OperandRegister64(rbase), displacement, index, scale):
                                        if source_from_stack:
                                            print(f"Invalid {opcode} args, source and dest can't be both from stack")
                                            continue
                                        if source_from_immediate and not -32768 <= s <= 32767:
                                            print(f"Invalid {opcode} args, immediate value {s} out of range with memory reference target")
                                            continue
                                        a = registers[rbase] + displacement
                                        if index:
                                            a += registers[index.register] * scale
                                        match opcode:
                                            case 'addq':
                                                stack[a] += s
                                            case 'subq':
                                                stack[a] -= s
                                            case 'movq':
                                                stack[a] = s
                                    case _:
                                        print(f"Invalid {opcode} dest:", dest)
                                        continue
                            case _:
                                print(f"Invalid/unsupported {opcode} args:", args)

                    case 'callq':
                        match args:
                            case [A64OperandLabel(l)]:
                                if l == 'print_int':
                                    print(registers['rdi'])
                                else:
                                    print("Unknown subroutine", l)
                            case _:
                                print("Invalid callq args:", args)

                    case 'negq':
                        match args:
                            case [A64OperandRegister64(rd)]:
                                registers[rd] = -registers[rd]

                            case [A64OperandMemory64(A64OperandRegister64(rbase), displacement, index, scale)]:
                                a = registers[rbase] + displacement
                                if index:
                                    a += registers[index.register] * scale
                                stack[a] = -stack[a]

                            case _:
                                print("Invalid negq target:", args)

                    case _:
                        print("Unknown opcode:", opcode)

            case _:
                print("Unknown statement:", statement)


if __name__ == "__main__":
    p = A64Program()
    p.add_statement(A64Comment('My first A64 program'))
    p.add_statement(A64Label('main'))
    p.add_statement(A64Instruction.pusq(A64OperandRegister64('rbp')))
    p.add_statement(A64Instruction.movq(A64OperandRegister64('rsp'), A64OperandRegister64('rbp')))
    p.add_statement(A64Instruction('subq', [A64OperandImmediate(16), A64OperandRegister64('rsp')]))
    p.add_statement(A64Instruction('movq', [A64OperandImmediate(12), A64OperandMemory64(A64OperandRegister64.rbp(), -8)]))
    p.add_statement(A64Instruction('addq', [A64OperandImmediate(8), A64OperandMemory64(A64OperandRegister64.rbp(), -8)]))
    p.add_statement(A64Instruction('negq', [A64OperandMemory64(A64OperandRegister64.rbp(), -8)]))
    p.add_statement(A64Instruction('movq', [A64OperandMemory64(A64OperandRegister64.rbp(), -8), A64OperandRegister64('rdi')]))
    p.add_statement(A64Instruction.callq(A64OperandLabel('print_int')))
    p.add_statement(A64Instruction('addq', [A64OperandImmediate(16), A64OperandRegister64('rsp')]))
    p.add_statement(A64Instruction('popq', [A64OperandRegister64('rbp')]))
    p.add_statement(A64Instruction.retq())

    runA64Program(p)
