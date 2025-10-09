# 01_ast_play.py
# Essential of compilation, python, ch 02, integers and variables
#
# 2025-10-09    PV      First version

from ast import *
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
    def interp_stmt(self, s, env, cont):
        match s:
            case Expr(Call(Name('print'), [arg])):
                val = self.interp_exp(arg, env)
                print(val, end='')
                return self.interp_stmts(cont, env)
            case Expr(value):
                self.interp_exp(value, env)
                return self.interp_stmts(cont, env)
            case _:
                raise Exception('error in interp_stmt, unexpected ' + repr(s))

    # I really don't like the abuse of call stack: interp_stmts -> interp_stmt -> interp_stmts -> interp_stmt -> ...
    # Rewrite this using a while loop
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
