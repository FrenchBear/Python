# ch02_lvar.py
# Essential of compilation, python, ch 02, integers and variables, base interpreter
#
# 2025-10-09    PV      First version

from ast import *
from ast import Assign, Expr
from typing import Any
from utils import *


# ch01 lint is reimplemented using a class, so it allows virtual function calls enabling extensions for lvar,
# so it can be extended through inheritance and method overriding (open recursion): see 02_open_recursion.py
# Also add env, environment dict. Even if it's not needed in Lint, it's required for LVar, and method overrides
# must have the same signature, so we add env parameter to Lint too
class InterpLint:
    def interp_exp(self, e, env):
        match e:
            case BinOp(left, Add(), right):
                l = self.interp_exp(left, env)
                r = self.interp_exp(right, env)
                return add64(l, r)
            case BinOp(left, Sub(), right):
                l = self.interp_exp(left, env)
                r = self.interp_exp(right, env)
                return sub64(l, r)
            case UnaryOp(USub(), v):
                return neg64(self.interp_exp(v, env))
            case Constant(value):
                return value
            case Call(Name('input_int'), []):
                return int(input("Enter int: "))

    # s is a single statement, cont is a continuation list of follow-up statements
    # This allows for a statement to decide whether to continue or not, for instance, allowing a return statement
    # to exit early from a function
    def interp_stmt(self, s, env, cont):
        match s:
            case Expr(Call(Name('print'), [arg])):
                val = self.interp_exp(arg, env)
                # print(val, end='')
                print(val)
                return self.interp_stmts(cont, env)
            case Expr(value):
                self.interp_exp(value, env)
                return self.interp_stmts(cont, env)
            case _:
                raise Exception('error in interp_stmt, unexpected ' + repr(s))

    # I really don't like the abuse of call stack: interp_stmts -> interp_stmt -> interp_stmts -> interp_stmt -> ...
    # Rewrite this using a while loop, but still allowing interp_stmt to decide whether to continue or not
    def interp_stmts(self, ss, env):
        match ss:
            case []:
                return 0
            case [s, *ss]:
                return self.interp_stmt(s, env, ss)

    def interp(self, p):
        match p:
            case Module(body):
                self.interp_stmts(body, {})     # Start with mpty environment

    @staticmethod
    def interp_Lint(p):
        return InterpLint().interp(p)


# ----------------------
# Extension for Lvar, adding variables

class InterpLvar(InterpLint):
    def interp_exp(self, e, env):
        match e:
            case Name(id):
                return env[id]      # Will halt with error if variable is not defined, it's Ok for now
            case _:
                return super().interp_exp(e, env)

    def interp_stmt(self, s, env, cont):
        match s:
            case Assign([Name(id)], value):
                env[id] = self.interp_exp(value, env)
                return self.interp_stmts(cont, env)
            case _:
                return super().interp_stmt(s, env, cont)

    @staticmethod
    def interp_Lvar(p):
        return InterpLvar().interp(p)


if __name__ == '__main__':
    for program in [
        'x=42+10+3\ny=2 + -3\nprint(x+y+input_int())',
        'x=(1+2)+3\nprint(x+2)',
        'x = 1+input_int()', ]:
        print("\n\n------------------------------------")
        print("program: ", program)
        p = ast.parse(program)
        print("\nAST:\n", ast.dump(p, indent=2))

        print("\nExecution:")
        InterpLvar.interp_Lvar(p)
