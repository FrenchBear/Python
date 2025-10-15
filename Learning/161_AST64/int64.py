# int64.py
# An interpreter for A64 AST program
#
# 2025-10-12    PV      First version
# 2025-10-15    PV      Rewrite using context and implement proper call/ret using stack

# ToDo: flags

from ast64 import *

class A64ExecutionContext:
    def __init__(self) -> None:
        self.stacksize = 1000
        self.registers = {'rax': 0, 'rbx': 0, 'rcx': 0, 'rdx': 0, 'rsi': 0, 'rdi': 0, 'rsp': self.stacksize, 'rbp': 0, 'r8': 0, 'r9': 0, 'r10': 0, 'r11': 0, 'r12': 0, 'r13': 0, 'r14': 0, 'r15': 0}
        self.stack = {i: 0 for i in range(self.stacksize, -1, -8)}
        self.flags = {'ZF': False, 'SF': False, 'OF': False, 'CF': False}   # Flags: ZF (zero), SF (sign), OF (overflow), CF (carry)
        self.rip = 0   # Instruction pointer
        self.labelsdict: dict[str, int] = {}
        self.error = False  # Stop execution if true

    def __str__(self) -> str:
        msg = "Context:\n" + ", ".join(f"{k}={v}" for k, v in self.registers.items()) + "\n" + f"rip={self.rip}\n" + "Stack: \n"
        rsp = self.registers['rsp']
        for i in range(-5,6):
            if 0<=rsp+i*8<=self.stacksize:
                msg += f"  {rsp+i*8}: {self.stack[rsp+i*8]}\n"
        return msg

def A64Error(ctx: A64ExecutionContext, *args, **kwargs):
    print("*** Err:", *args, **kwargs)
    print(ctx)
    ctx.error = True


def runA64Instruction(ctx: A64ExecutionContext, opcode: str, args: List[A64Operand]):
    match opcode:
        case 'callq':
            match args:
                case [A64OperandLabel('print_int')]:
                    print(ctx.registers['rdi'])
                case [A64OperandLabel(l)]:
                    if l not in ctx.labelsdict:
                        A64Error(ctx, f"Label {l} not found")
                        return
                    ctx.stack[ctx.registers['rsp']] = ctx.rip
                    ctx.registers['rsp'] -= 8
                    ctx.rip = ctx.labelsdict[l]
                case _:
                    A64Error(ctx, "Invalid callq args:", args)

        case 'retq':
            match args:
                case []:
                    ctx.registers['rsp'] += 8
                    ctx.rip = ctx.stack[ctx.registers['rsp']]
                case _:
                    A64Error(ctx, "Invalid retq args:", args)

        case 'pushq':
            match args:
                case [A64OperandRegister64(r)]:
                    ctx.stack[ctx.registers['rsp']] = ctx.registers[r]
                    ctx.registers['rsp'] -= 8
                    if ctx.registers['rsp'] < 0:
                        A64Error(ctx, "Stack overflow")
                case _:
                    A64Error(ctx, "Invalid pushq args:", args)

        case 'popq':
            match args:
                case [A64OperandRegister64(r)]:
                    ctx.registers['rsp'] += 8
                    if ctx.registers['rsp'] > ctx.stacksize:
                        A64Error(ctx, "Stack underflow")
                        return
                    ctx.registers[r] = ctx.stack[ctx.registers['rsp']]
                case _:
                    A64Error(ctx, "Invalid popq args:", args)

        case 'addq' | 'subq' | 'movq':
            match args:
                case [source, dest]:
                    s = 0
                    source_from_stack = False
                    source_from_immediate = False
                    match source:
                        case A64OperandImmediate(n):
                            s = n
                            source_from_immediate = True
                        case A64OperandRegister64(rs):
                            s = ctx.registers[rs]
                        case A64OperandMemory64(A64OperandRegister64(rbase), displacement, index, scale):
                            a = ctx.registers[rbase] + displacement
                            if index:
                                a += ctx.registers[index.register] * scale
                            s = ctx.stack[a]
                            source_from_stack = True
                        case _:
                            A64Error(ctx, f"Invalid {opcode} source:", source)

                    match dest:
                        case A64OperandRegister64(rd):
                            match opcode:
                                case 'addq':
                                    ctx.registers[rd] += s
                                case 'subq':
                                    ctx.registers[rd] -= s
                                case 'movq':
                                    ctx.registers[rd] = s

                        case A64OperandMemory64(A64OperandRegister64(rbase), displacement, index, scale):
                            if source_from_stack:
                                A64Error(ctx, f"Invalid {opcode} args, source and dest can't be both from ctx.stack")
                                return
                            if source_from_immediate and not -32768 <= s <= 32767:
                                A64Error(ctx, f"Invalid {opcode} args, immediate value {s} out of range with memory reference target")
                                return
                            a = ctx.registers[rbase] + displacement
                            if index:
                                a += ctx.registers[index.register] * scale
                            match opcode:
                                case 'addq':
                                    ctx.stack[a] += s
                                case 'subq':
                                    ctx.stack[a] -= s
                                case 'movq':
                                    ctx.stack[a] = s
                        case _:
                            A64Error(ctx, f"Invalid {opcode} dest:", dest)
                            return
                case _:
                    A64Error(ctx, f"Invalid/unsupported {opcode} args:", args)

        case 'negq':
            match args:
                case [A64OperandRegister64(rd)]:
                    ctx.registers[rd] = -ctx.registers[rd]

                case [A64OperandMemory64(A64OperandRegister64(rbase), displacement, index, scale)]:
                    a = ctx.registers[rbase] + displacement
                    if index:
                        a += ctx.registers[index.register] * scale
                    ctx.stack[a] = -ctx.stack[a]

                case _:
                    A64Error(ctx, "Invalid negq args:", args)

        case _:
            A64Error(ctx, "Unknown/Unsupported opcode:", opcode)


def runA64Satement(ctx: A64ExecutionContext, statement: A64Statement):
    match statement:
        case A64Comment(c):
            pass
        case A64Label(l):
            # For now, ignore
            pass
        case A64Instruction(opcode, args):
            runA64Instruction(ctx, opcode, args)
        case _:
            A64Error(ctx, "Unknown statement:", statement)

def runA64Program(program: A64Program):
    ctx = A64ExecutionContext()

    # Build the dict of labels
    for ix, statement in enumerate(program.statements):
        match statement:
            case A64Label(l):
                ctx.labelsdict[l.lower()] = ix

    ctx.rip = -1    # A return address of -1 means end of program
    runA64Instruction(ctx, 'callq', [A64OperandLabel('main')])
    
    # Instruction pointer, local to this function
    while not ctx.error:
        if ctx.rip == -1:
            break
        
        if not 0<=ctx.rip<len(program.statements):
            A64Error(ctx, "Invalid instruction pointer:", ctx.rip)
            break
        statement = program.statements[ctx.rip]
        ctx.rip += 1
        runA64Satement(ctx, statement)


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

    p.add_statement(A64Instruction('movq', [A64OperandRegister64('rbp'), A64OperandRegister64('rsp')]))
    p.add_statement(A64Instruction('popq', [A64OperandRegister64('rbp')]))
    p.add_statement(A64Instruction.retq())

    #print(p)
    runA64Program(p)
    