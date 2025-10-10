# ch02_x24_select_statements
# Essential of compilation, python, ch 2.4, Remove complex operands, Exercise 2.4, select X86 instructions
# but keep variables names. Also "a=b" translated in "movq b, q" is potentially incorrect since movq can contain
# at most one memory reference, this will be addressed later
#
# 2025-10-10    PV      First version

from ch02_x21_remove_complex_v2 import *
from x86_ast import *
from typing import cast

class Compiler2(Compiler):
    ############################################################################
    # Select Instructions
    ############################################################################

    # The expression e passed to select_arg should furthermore be an atom.
    # (But there is no type for atoms, so the type of e is given as expr.)
    def select_arg(self, e: expr):
        match e:
            case Constant(n):
                return Immediate(n)

            case Name(id):
                return Name(id)

            case _:
                return e

    def select_stmt(self, s: stmt):
        match s:
            case Expr(Call(Name('print'), [atm])):
                a = self.select_arg(atm)
                i1 = Instr('movq', [a, Reg('rdi')])
                i2 = Callq(label_name('print_int'), 1)
                return [i1, i2]

            case Assign([Name(name)], exp):
                match exp:
                    case Constant(n):
                        return [Instr('movq', [Immediate(n), Name(name)])]
                    
                    case Name(id):
                        return [Instr('movq', [Name(id), Name(name)])]
                    
                    case Call(Name('read_int'), []):
                        return [Callq(label_name('read_int'), 0),
                                Instr('movq', [Reg('rax'), Name(name)])]
                    
                    case BinOp(left, op, right):
                        x86op = 'addq' if isinstance(op, Add) else 'subq'
                        if isinstance(left, Name) and left.id==name:
                            # Case name = name op right
                            return [Instr(x86op, [self.select_arg(right), Name(name)])]
                        elif isinstance(right, Name) and right.id==name:
                            # Case name = left op name
                            return [Instr(x86op, [self.select_arg(left), Name(name)])]
                        else:
                            return [Instr('movq', [self.select_arg(left), Name(name)]),
                                    Instr(x86op, [self.select_arg(right), Name(name)])]

                    case UnaryOp(USub(), arg):
                        return [Instr('movq', [self.select_arg(arg), Name(name)]),
                                Instr('negq', [Name(name)])]
                    case _:
                        return []
            
            # The case Expr(...) is useless except the side effect of read_int()
            case Expr(exp):
                match exp:
                    case Call(Name('read_int'), []):
                        return [Callq(label_name('read_int'), 0)]
                    case BinOp(Call(Name('read_int'), []), op, Call(Name('read_int'), [])):
                        return [Callq(label_name('read_int'), 0),
                                Callq(label_name('read_int'), 0)]
                    case BinOp(Call(Name('read_int'), []), op, _) | BinOp(_, op, Call(Name('read_int'), [])):
                        return [Callq(label_name('read_int'), 0)]
                    case UnaryOp(USub(), Call(Name('read_int'), [])):
                        return [Callq(label_name('read_int'), 0)]
                    case _:
                        return []

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
    #program = 'x=-5+read_int()\nx=x+1\ny=1+x\nprint(x)'
    #program = 'x=-3\n-read_int()\nprint(x)'
    program = 'a=42\nb=a\nprint(b)'

    print("\n\n------------------------------------")
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
    print(str(r).lstrip())
