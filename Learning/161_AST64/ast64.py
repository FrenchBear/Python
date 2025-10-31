# ast64.py
# An example of matchable class hierarchy, representing a simplified assembly language
#
# 2025-10-12    PV      First version

import abc
from dataclasses import dataclass
from typing import Iterator, List

class A64Program:
    def __init__(self) -> None:
        self.statements: list[A64Statement] = []

    def add_statement(self, statement) -> None:
        self.statements.append(statement)

    def __repr__(self):
        # return "A64Program:\n  " + "\n  ".join(str(s) for s in self.statements)
        return "\n".join(str(s) for s in self.statements)

    # A64Program is direcly iterable for convenience, without referencing statements attribute
    def __iter__(self) -> Iterator['A64Statement']:
        return iter(self.statements)

# Abstract base class for any program statement
class A64Statement:
    @abc.abstractmethod
    def __init__(self): pass

class A64Label(A64Statement):
    def __init__(self, name: str):
        self.name = name

    __match_args__ = ('name',)

    def __repr__(self):
        return f"Label({self.name})"

class A64Comment(A64Statement):
    def __init__(self, comment: str):
        self.comment = comment

    __match_args__ = ('comment',)

    def __repr__(self):
        return f";{self.comment}"

class A64Operand:
    ...

@dataclass
class A64OperandImmediate(A64Operand):
    def __init__(self, immediate: int) -> None:
        if -(2**63) <= immediate <= 2**63-1:
            self.immediate = immediate
        else:
            raise ValueError(f"Invalid immediate value: {immediate}")


        self.immediate = immediate

    __match_args__ = ('immediate',)

    def __repr__(self): return f"${self.immediate}"

@dataclass
class A64OperandName(A64Operand):
    def __init__(self, name: str) -> None:
        self.name = name

    __match_args__ = ('name',)

    def __repr__(self): return f"«{self.name}»"

@dataclass
class A64OperandLabel(A64Operand):
    def __init__(self, label: str) -> None:
        self.label = label

    __match_args__ = ('label',)

    def __repr__(self): return self.label

@dataclass
class A64OperandRegister64(A64Operand):
    def __init__(self, register: str) -> None:
        if register in ['rsp', 'rbp', 'rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']:
            self.register = register
        else:
            raise ValueError(f"Invalid register name: {register}")

    __match_args__ = ('register',)

    def __repr__(self): return f"%{self.register}"

    @staticmethod
    def rsp() -> 'A64OperandRegister64':
        return A64OperandRegister64('rsp')

    @staticmethod
    def rbp() -> 'A64OperandRegister64':
        return A64OperandRegister64('rbp')


@dataclass
class A64OperandMemory64(A64Operand):
    def __init__(self, base: A64OperandRegister64, displacement: int = 0, index: A64OperandRegister64 | None = None, scale: int = 1) -> None:
        self.base = base
        self.displacement = displacement
        self.index = index
        self.scale = scale

    __match_args__ = ('base', 'displacement', 'index', 'scale')

    def __repr__(self):
        s = ""
        if self.displacement != 0:
            s += f"{self.displacement}"
        s += f"({self.base}"
        if self.index:
            s += f", {self.index}"
            if self.scale != 1:
                s += f", {self.scale}"
        s += ")"
        return s

@dataclass
class A64Instruction(A64Statement):
    def __init__(self, opcode: str, operands: List[A64Operand]):
        self.opcode = opcode
        self.operands = operands

    __match_args__ = ('opcode', 'operands')

    def __repr__(self):
        return f"{self.opcode} " + (", ".join(f"{op}" for op in self.operands) if len(self.operands) > 0 else "")

    @staticmethod
    def retq() -> 'A64Instruction':
        return A64Instruction('retq', [])

    @staticmethod
    def pusq(r: A64OperandRegister64) -> 'A64Instruction':
        return A64Instruction('pushq', [r])
    
    @staticmethod
    def movq(source: A64Operand, target: A64Operand) -> 'A64Instruction':
        return A64Instruction('movq', [source, target])
    
    @staticmethod
    def callq(label: A64OperandLabel) -> 'A64Instruction':
        return A64Instruction('callq', [label])

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

    print(p, "\n")

    for statement in p:
        match statement:
            case A64Comment(c):
                print(f"Comment: {c}")
            case A64Label(l):
                print("Label:", l)
            case A64Instruction('retq', []):
                print("Instruction retq")
            case A64Instruction('pushq', [A64OperandRegister64('rbp')]):
                # case A64Instruction('pushq', [r]):
                print("Instruction pushq %rbp  detected")
            case A64Instruction(opcode, [A64OperandImmediate(n), target]):
                print("Instruction with immediate constant:", statement)
            case A64Instruction(opcode, operands):
                print("Instruction:", statement)
            case _:
                print("Unknown statement:", statement)

    # print("\n")
    # r1 = A64OperandRegister64('rbp')
    # r2 = A64OperandRegister64('rbp')
    # print(r1 == r2)
