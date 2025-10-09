# 01_lint.py
# Essential of compilation, python, ch 01, simple langage with integers, ast
#
# 2025-10-08    PV      First version

from ast import *
from utils import *

s = "print(4*len('hello'))"
#s = "a = 8*7\nprint(a+2)"
a = parse(s)

print(s)
print(dump(a))
print(dump(a, indent=2))
print(unparse(a))
print()

for x in walk(a):
    match x:
        case Module(m):
            print("Module", m)
        case Expr(e):
            print("Expr", e)
        case Name(n):
            print("Name", n)
        case BinOp(l, o, r):
            print("BinOp", l, o, r)
        case Constant(c):
            print("Constant", c)
        case Mult():
            print("Mult")
        case _:
            print(x)
print()

# Concrete syntax
# exp ::= int | input_int() | - exp | exp + exp | exp - exp | (exp)
# stmt ::= print(exp) | exp
# LInt ::= stmt∗

# Abstract syntax
# exp ::= Constant(int) | Call(Name('input_int'),[]) | UnaryOp(USub(),exp) | BinOp(exp,Add(),exp) | BinOp(exp,Sub(),exp)
# stmt ::= Expr(Call(Name('print'),[exp])) | Expr(exp)
# LInt ::= Module(stmt∗)


eight = Constant(8)
neg_eight = UnaryOp(USub(), eight)
read = Call(Name('input_int'), [])
ast1_1 = BinOp(read, Add(), neg_eight)

# Recognizes when an LInt node is a leaf in the AST.
def leaf(arith):
    match arith:
        case Constant(n):
            return True
        case Call(Name('input_int'), []):
            return True
        case UnaryOp(USub(), e1):
            return False
        case BinOp(e1, Add(), e2):
            return False
        case BinOp(e1, Sub(), e2):
            return False


print(leaf(Call(Name('input_int'), [])))
print(leaf(UnaryOp(USub(), eight)))
print(leaf(Constant(8)))
print()

def is_exp(e):
    match e:
        case Constant(n):
            return True
        case Call(Name('input_int'), []):
            return True
        case UnaryOp(USub(), e1):
            return is_exp(e1)
        case BinOp(e1, Add(), e2):
            return is_exp(e1) and is_exp(e2)
        case BinOp(e1, Sub(), e2):
            return is_exp(e1) and is_exp(e2)
        case _:
            return False

def is_stmt(s):
    match s:
        case Expr(Call(Name('print'), [e])):
            return is_exp(e)
        case Expr(e):
            return is_exp(e)
        case _:
            return False

def is_Lint(p):
    match p:
        case Module(body):
            return all([is_stmt(s) for s in body])
        case _:
            return False


print(is_Lint(Module([Expr(ast1_1)])))
print(is_Lint(Module([Expr(BinOp(read, Sub(), UnaryOp(UAdd(), Constant(8))))])))        # Unitary + before 8 is not part of LInt grammar
print()

# -----------------------------------------
# Interpretation

def interp_exp(e):
    match e:
        case BinOp(left, Add(), right):
            l = interp_exp(left); r = interp_exp(right)
            return add64(l, r)
        case BinOp(left, Sub(), right):
            l = interp_exp(left); r = interp_exp(right)
            return sub64(l, r)
        case UnaryOp(USub(), v):
            return neg64(interp_exp(v))
        case Constant(value):
            return value
        case Call(Name('input_int'), []):
            return input_int()

def interp_stmt(s):
    match s:
        case Expr(Call(Name('print'), [arg])):
            print(interp_exp(arg))
        case Expr(value):
            interp_exp(value)

def interp_Lint(p):
    match p:
        case Module(body):
            for s in body:
                interp_stmt(s)


p1 = Module([Expr(Call(Name('print'), [BinOp(Constant(10), Add(), Constant(32))]))])
interp_Lint(p1)
# interp_Lint(Module([Expr(Call(Name('print'), [ast1_1]))]))            # Remember that input_int in ast1_1 stops the program, waiting for integer input
print()

# -----------------------------------------
# Example compiler: partial evaluator

# we consider a compiler that translates LInt programs into LInt programs that may be more efficient. The compiler
# eagerly computes the parts of the program that do not depend on any inputs, a process known as partial evaluation
# (Jones, Gomard, and Sestoft 1993). For example, given the following program
# print(input_int() + -(5 + 3) )
# our compiler translates it into the program
# print(input_int() + -8)

def pe_neg(r):
    match r:
        case Constant(n):
            return Constant(neg64(n))
        case _:
            return UnaryOp(USub(), r)

def pe_add(r1, r2):
    match (r1, r2):
        case (Constant(n1), Constant(n2)):
            return Constant(add64(n1, n2))
        case _:
            return BinOp(r1, Add(), r2)

def pe_sub(r1, r2):
    match (r1, r2):
        case (Constant(n1), Constant(n2)):
            return Constant(sub64(n1, n2))
        case _:
            return BinOp(r1, Sub(), r2)

def pe_exp(e):
    match e:
        case BinOp(left, Add(), right):
            return pe_add(pe_exp(left), pe_exp(right))
        case BinOp(left, Sub(), right):
            return pe_sub(pe_exp(left), pe_exp(right))
        case UnaryOp(USub(), v):
            return pe_neg(pe_exp(v))
        case Constant(value):
            return e
        case Call(Name('input_int'), []):
            return e        # return as is, non-evaluated call

def pe_stmt(s):
    match s:
        case Expr(Call(Name('print'), [arg])):
            return Expr(Call(Name('print'), [pe_exp(arg)]))     # type: ignore
        case Expr(value):
            return Expr(pe_exp(value))     # type: ignore

def pe_P_int(p):
    match p:
        case Module(body):
            new_body = [pe_stmt(s) for s in body]
            return Module(new_body)     # type: ignore
    print("Err: pe_P_int only process modules")
    return Module()
        
p1a = Module([Expr(Call(Name('print'), [BinOp(Constant(10), Add(), Constant(32))]))])
p1b = pe_P_int(p1a)
print(ast.dump(p1a, indent=2))
interp_Lint(p1a)
print(ast.dump(p1b, indent=2))
interp_Lint(p1b)
print()

p2a = Module([Expr(BinOp(BinOp(Constant(3), Add(), Constant(5)), Sub(), UnaryOp(USub(), Constant(5))))])
p2b = pe_P_int(p2a)
print(ast.dump(p2a, indent=2))
print(ast.dump(p2b, indent=2))
