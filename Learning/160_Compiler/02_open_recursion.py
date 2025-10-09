# 02_open_recursion.py
# Example to understand how class inheritance and method override work in Python to implement open_recursion
#
# 2025-10-09    PV      First version

from ast import *
from utils import *

class InterpLint:
    # Because class InterpLvar is derived from InterpLint, this method can be called with self: InterpLVar,
    # so self.interp_exp(..) will actually call InterpLVar.interp_exp(..) in this case
    def interp_exp(self, e, env):
        match e:
            case UnaryOp(USub(), e1):
                return neg64(self.interp_exp(e1, env))

class InterpLvar(InterpLint):
    def interp_exp(self, e, env):
        match e:
            case Name(id):
                return env[id]
            case _:
                return super().interp_exp(e, env)
            

e = UnaryOp(USub(), Name('y'))
res = InterpLvar().interp_exp(e, {'y': 5})
print(res)
