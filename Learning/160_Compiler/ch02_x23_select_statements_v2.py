# ch02_x23_select_statements_v2.py
# Essential of compilation, python ch 2, Exercise 2.5, select X86 instructions, version 2
# Keep variables names. Also "a=b" translated in "movq b, q" is potentially incorrect since movq can contain
# at most one memory reference, this will be addressed later
#
# 2025-10-10    PV      First version
# 2025-10-11    PV      v2

from ch02_x21_remove_complex_v2 import *
from x86_ast import *
from typing import cast

class Compiler2(Compiler):
    ############################################################################
    # Select Instructions
    ############################################################################

    # The expression e passed to select_arg should furthermore be an atom.
    # (But there is no type for atoms, so the type of e is given as expr.)
    def select_arg(self, e: expr) -> arg:
        match e:
            case Constant(n):
                i = cast(int, n)
                return Immediate(i)

            case Name(id):
                return cast(arg, Name(id))

            case _:
                return cast(arg, e)

    def process_expression(self, exp: expr, target: location) -> List:
        match exp:
            case Constant(n):
                i = cast(int, n)
                if -32768 <= i <= 32767:
                    return [Instr('movq', [Immediate(i), target])]
                else:
                    return [Instr('movq', [Immediate(i), Reg('rax')]),
                            Instr('movq', [Reg('rax'), target])]
            
            case Name(id):
                return [Instr('movq', [self.select_arg(Name(id)), target])]
            
            case Call(Name('input_int'), []):
                return [Callq(label_name('read_int'), 0),
                        Instr('movq', [Reg('rax'), target])]
            
            case BinOp(left, op, right):
                x86op = 'addq' if isinstance(op, Add) else 'subq'
                if left==target:
                    # Case name = name op right
                    return [Instr(x86op, [self.select_arg(right), target])]
                elif right==target:
                    # Case name = left op name
                    return [Instr(x86op, [self.select_arg(left), target])]
                else:
                    return [Instr('movq', [self.select_arg(left), target]),
                            Instr(x86op, [self.select_arg(right), target])]

            case UnaryOp(USub(), arg):
                source = self.select_arg(arg)
                if source==target:
                    return [Instr('negq', [target])]
                return [Instr('movq', [source, target]),
                        Instr('negq', [target])]
            case _:
                return []

    def select_stmt(self, s: stmt):
        match s:
            case Expr(Call(Name('print'), [atm])):
                a = self.select_arg(atm)
                i1 = Instr('movq', [a, Reg('rdi')])
                i2 = Callq(label_name('print_int'), 1)
                return [i1, i2]

            case Assign([Name(name)], exp):
                return self.process_expression(exp, cast(location, Name(name)))
            
            # A simple expression is actually useless except for size effect of calling functions such as input_int()
            case Expr(exp):
                return self.process_expression(exp, Reg('rax'))

            case _:
                return []

    def select_instructions(self, p: Module) -> X86Program:
        asm_body = []
        asm_body.append(Instr('pushq', [Reg('rdi')]))
        for statement in p.body:
            asm_body.extend(self.select_stmt(statement))
        asm_body.append(Instr('popq', [Reg('rdi')]))
        asm_body.append(Instr('movq', [Immediate(0), Reg('rax')]))
        asm_body.append(Instr('retq', []))
        x86p = X86Program(asm_body)
        return x86p

if __name__ == '__main__':
    def process_program(program):
        print("------------------------------------")
        print("Original program:\n", program, sep='')
        p = ast.parse(program)
        # print("\nAST:\n", ast.dump(p, indent=2), sep='')
        # print("\nExecution:")
        # InterpLvar.interp_Lvar(p)

        print("\n------\nAfter removing complex expressions:")
        q = Compiler2().remove_complex_operands(p)
        print(ast.unparse(q))
        # print("\nAST:\n", ast.dump(q, indent=2), sep='')
        # print("\nExecution:")
        # InterpLvar.interp_Lvar(q)

        print("\n------\nX86 code generation:")
        r = Compiler2().select_instructions(q)
        print(str(r).lstrip(), '\n\n')


    #program = 'x=-5+input_int()\nx=x+1\ny=1+x\nprint(x)'
    #program = 'x=-3\nx=-input_int()\nprint(x)'
    program = 'x=-input_int()'
    #program = 'a=42\nb=a\nprint(b)'
    #program = 'x=2\nx=-x\nprint(x)'
    process_program(program)
