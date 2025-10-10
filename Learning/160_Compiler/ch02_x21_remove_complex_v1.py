# ch02_x1_remove_complex_v1.py
# Essential of compilation, python, ch 2.4, Remove complex operands, Exercise 2.1, first version
#
# 2025-10-09    PV      First version

from ch02_lvar import *
from utils import *

# ----------------------
# 1st step, remove_complex_operand

def is_atomic_expression(e):
    match e:
        case Constant(n):
            return True
        case Name(id):
            return True
        case _:
            return False

def is_simple_expression(e):
    if is_atomic_expression(e):
        return True
    match e:
        case BinOp(left, op, right):
            return is_atomic_expression(left) and is_atomic_expression(right)
        case UnaryOp(USub(), arg):
            return is_atomic_expression(arg)
        case Expr(Call(Name('input_int'), [])):
            return True
        case _:
            return False

def make_atomic_expression(name, e):
    statements = []
    match e:
        case BinOp(left, op, right):
            if not is_atomic_expression(left):
                tn = generate_name('temp')
                statements.extend(make_atomic_expression(tn, left))
                left = Name(tn)
            if not is_atomic_expression(right):
                tn = generate_name('temp')
                statements.extend(make_atomic_expression(tn, right))
                right = Name(tn)
            statements.append(Assign([Name(name)], BinOp(left, op, right), lineno=0))

        case UnaryOp(USub(), arg):
            if not is_atomic_expression(arg):
                tn = generate_name('temp')
                for ss in make_atomic_expression(tn, arg):
                    statements.append(ss)
                arg = Name(tn)
            statements.append(Assign([Name(name)], UnaryOp(USub(), arg), lineno=0))

        case Call(Name('input_int'), []):
            statements.append(Assign([Name(name)], e, lineno=0))    # type: ignore

        case _:
            statements.append(e)

    return statements

def make_simple_expression(e: expr):
    statements = []
    match e:
        case BinOp(left, op, right):
            if not is_atomic_expression(left):
                tn = generate_name('temp')
                statements.extend(make_atomic_expression(tn, left))
                left = Name(tn)
            if not is_atomic_expression(right):
                tn = generate_name('temp')
                statements.extend(make_atomic_expression(tn, right))
                right = Name(tn)
            return statements, BinOp(left, op, right)

        case UnaryOp(op, arg):
            if not is_atomic_expression(arg):
                tn = generate_name('temp')
                for ss in make_atomic_expression(tn, arg):
                    statements.append(ss)
                arg = Name(tn)
            return statements, UnaryOp(op, arg)

        case _:
            return [], e

def Remove_complex_operands(p):
    new_body = []
    match p:
        case Module(body):
            for statement in body:
                match statement:
                    case Expr(Call(Name('print'), [arg])):
                        if not is_atomic_expression(arg):
                            tn = generate_name('temp')
                            for ss in make_atomic_expression(tn, arg):
                                new_body.append(ss)
                            arg = Name(tn)
                        new_body.append(Expr(Call(Name('print'), [arg])))

                    case Assign([Name(name)], exp):
                        if not is_simple_expression(exp):
                            substat, exp = make_simple_expression(exp)
                            new_body.extend(substat)
                        new_body.append(Assign([Name(name)], exp, lineno=0))

                    case Expr(exp):
                        if not is_simple_expression(exp):
                            substat, exp = make_simple_expression(exp)
                            new_body.extend(substat)
                        new_body.append(Expr(exp, lineno=0))

                    case _:
                        breakpoint()
                        pass

    return Module(new_body)


if __name__ == '__main__':
    for program in [
        # 'x=42+10+3\ny=2 + -3\nprint(x+y+input_int())',
        'x=(1+2)+3\nprint(x+2)',
        # 'x = 1+input_int()',
    ]:
        print("\n\n------------------------------------")
        print("Original program:\n", program, sep='')
        p = ast.parse(program)
        print("\nAST:\n", ast.dump(p, indent=2), sep='')
        print("\nExecution:")
        InterpLvar.interp_Lvar(p)

        q = Remove_complex_operands(p)
        print("\n------\nAfter removing complex expressions:")
        print(ast.unparse(q))
        print("\nAST:\n", ast.dump(q, indent=2), sep='')
        print("\nExecution:")
        InterpLvar.interp_Lvar(q)
