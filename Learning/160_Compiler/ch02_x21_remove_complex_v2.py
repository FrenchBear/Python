# ch02_x1_remove_complex_v2.py
# Essential of compilation, python, ch 2.4, Remove complex operands, Exercise 2.1, second version, using book structure
#
# 2025-10-10    PV      First version

from ch02_lvar import *
from utils import *
from typing import List, Tuple

Binding = Tuple[Name, expr]
Temporaries = List[Binding]

class Compiler:

    ############################################################################
    # Remove Complex Operands
    ############################################################################

    def rco_exp(self, e: expr, need_atomic : bool) -> Tuple[expr, Temporaries]:
        tempo: Temporaries = []
        match e:
            case Constant(n):
                return e, tempo
            
            case Name(id):
                return e, tempo
            
            case Call(Name('input_int'), []):
                if need_atomic:
                    tn = generate_name('temp')
                    tempo.append((Name(tn), Call(Name('input_int'), [])))
                    return Name(tn), tempo
                return e, tempo
            
            case BinOp(left, op, right):
                leftproc = self.rco_exp(left, need_atomic=True)
                rightproc = self.rco_exp(right, need_atomic=True)
                tempo.extend(leftproc[1])
                tempo.extend(rightproc[1])
                if need_atomic:
                    tn = generate_name('temp')
                    tempo.append((Name(tn), BinOp(leftproc[0], op, rightproc[0])))
                    return Name(tn), tempo
                return BinOp(leftproc[0], op, rightproc[0]), tempo
            
            case UnaryOp(op, arg):
                argproc = self.rco_exp(arg, need_atomic=True)
                tempo.extend(argproc[1])
                if need_atomic:
                    tn = generate_name('temp')
                    tempo.append((Name(tn), UnaryOp(op, argproc[0])))
                    return Name(tn), tempo
                return UnaryOp(op, arg), tempo

            case _:
                return e, tempo

    def rco_stmt(self, s: stmt) -> List[stmt]:
        match s:
            case Expr(Call(Name('print'), [arg])):
                new_exp, tempos = self.rco_exp(arg, True)
                l1: List[stmt] = [Assign([name], val, lineno=0) for name, val in tempos]
                st:stmt = Expr(Call(Name('print'), [new_exp]))
                l1.append(st)
                return l1

            case Assign([Name(name)], exp):
                new_exp, tempos = self.rco_exp(exp, False)
                return [
                    *[Assign([name], val, lineno=0) for name, val in tempos],
                    Assign([Name(name)], new_exp, lineno=0)
                ]

            case Expr(exp):
                new_exp, tempos = self.rco_exp(exp, False)
                return [
                    *[Assign([name], val, lineno=0) for name, val in tempos],
                    Expr(new_exp)
                ]

            # To make Python type checking happy            
            case _:
                return [s]

    def remove_complex_operands(self, p: Module) -> Module:
        new_body = []
        for statement in p.body:
            new_body.extend(self.rco_stmt(statement))
        return Module(new_body)

if __name__ == '__main__':
    #program = 'x=1+2\nprint(3+4)'
    program = 'x=-2\nprint(-5)'

    print("\n\n------------------------------------")
    print("Original program:\n", program, sep='')
    p = ast.parse(program)
    print("\nAST:\n", ast.dump(p, indent=2), sep='')
    print("\nExecution:")
    InterpLvar.interp_Lvar(p)

    q = Compiler().remove_complex_operands(p)
    print("\n------\nAfter removing complex expressions:")
    print(ast.unparse(q))
    print("\nAST:\n", ast.dump(q, indent=2), sep='')
    print("\nExecution:")
    InterpLvar.interp_Lvar(q)
