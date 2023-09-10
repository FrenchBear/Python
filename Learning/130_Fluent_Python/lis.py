# lis.py
# My own rewrite of flient python lisp/scheme interpreter to play with
# The original code is brilliant!
#
# 2023-09-11    PV

from collections import ChainMap
from itertools import chain
import operator as op
import math
from typing import TypeAlias, Any

Symbol: TypeAlias = str
Atom: TypeAlias = float | int | Symbol
Expression: TypeAlias = Atom | list

def parse_list(q: list[str]) -> Expression:
    if len(q) == 0:
        raise Exception('Empty string to parse')
    token = q.pop(0)
    if token == '(':
        exp = []
        while q[0] != ')':
            exp.append(parse_list(q))
        q.pop(0)    # remove )
        return exp
    if token == ')':
        raise Exception('Syntax error: Unexpected )')
    try:
        return int(token)
    except:
        pass
    try:
        return float(token)
    except:
        pass
    return Symbol(token)

def parse(expression: str) -> Expression:
    return parse_list(expression.replace('(', ' ( ').replace(')', ' ) ').split())

class Environment(ChainMap[Symbol, Any]):
    def change(self, key: Symbol, value: Any) -> None:
        for amap in self.maps:
            if key in amap:
                amap[key] = value
                return
        raise KeyError(key)

def lispstr(exp: object) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

def get_initial_env() -> Environment:
    env = Environment()
    env.update(vars(math))   # sin, cos, sqrt, pi, ...
    env.update({
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            'quotient': op.floordiv,
            '>': op.gt,
            '<': op.lt,
            '>=': op.ge,
            '<=': op.le,
            '=': op.eq,
            'abs': abs,
            'append': lambda *args: list(chain(*args)),
            'apply': lambda proc, args: proc(*args),
            'begin': lambda *x: x[-1],
            'car': lambda x: x[0],
            'cdr': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'display': lambda x: print(lispstr(x)),
            'eq?': op.is_,
            'equal?': op.eq,
            'filter': lambda *args: list(filter(*args)),
            'length': len,
            'list': lambda *x: list(x),
            'list?': lambda x: isinstance(x, list),
            'map': lambda *args: list(map(*args)),
            'max': max,
            'min': min,
            'not': op.not_,
            'null?': lambda x: x == [],
            'number?': lambda x: isinstance(x, (int, float)),
            'procedure?': callable,
            'round': round,
            'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

class Procedure:
    def __init__(self, parms: list[Symbol], body: list[Expression], env: Environment):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args: Expression) -> Any:
        local_env = dict(zip(self.parms, args))
        #local_env = {n:v for (n,v) in zip(self.parms, args)}
        env = Environment(local_env, self.env)
        for exp in self.body:
            result = evaluate(exp, env)
        return result

    def __repr__(self) -> str:
        return 'Proc('+(','.join(self.parms))+') -> '+('; '.join(str(z) for z in self.body))



def evaluate(exp: Expression, env: Environment):
    match exp:
        case int(x)|float(x):
            return x
        case Symbol(name):
            return env[name]
        case ['quote', x]:
            return x
        case ['eval', x]:
            e = evaluate(x, env)
            return evaluate(e, env)
        case ['if', test_exp, true_exp, false_exp]:
            return evaluate(true_exp, env) if evaluate(test_exp, env) else evaluate(false_exp, env)
        case ['lambda'|'λ', [*parms], *body] if body:
            return Procedure(parms, body, env)
        case ['set!', Symbol(name), value_exp]:
            env.change(name, evaluate(value_exp, env))       # And not env[name]=evaluate(...) that always works on the 1st mapping of a chainmap
        case ['define', Symbol(name), value_exp]:
            env[name] = evaluate(value_exp, env)
        case ['define', [Symbol(name), *parms], *body] if body:
            env[name] = Procedure(parms, body, env)
        case [func_exp, *args] if func_exp not in ['quote', 'if', 'lambda', 'define', 'set!']:      # Guard makes invalid use of a keyword not matching keywork contruction, ex: (display (if 5)) raise a syntax error rather than symbol not defined
            proc = evaluate(func_exp, env)
            arguments = [evaluate(arg, env) for arg in args]
            return proc(*arguments)
        case _:
            raise SyntaxError(lispstr(exp))

# pgm = """(
# (define (mod m n)
#     (- m (* n (quotient m n))))

# (define (gcd m n)
#     (if (= n 0)
#         m
#         (gcd n (mod m n))))

# (display (gcd 18 45))
# )
# """
# for statement in parse(pgm):    # type:ignore
#     print(statement)
#     print()

pgm = """(
(define a 8.5)
(define b (+ 4 3))
(define dz (quote(* 2 7)))
(display (eval dz))
(define (double x) (* x 2))
(define (doublemax2 x) (if (< (* x 2) 2)
                           (* x 2)
                           2
                       )
)
(display (double 1.75))
(display (doublemax2 1.75))
(define one_fourth (/ 1 4))
(display (doublemax2 one_fourth))
(if (> a b)
    (display 1)
    (display 2))
(display (* a b))
(define (average a b) (/ (+ a b) 2))
(display (average 5 7))
(define (% a b) (* (/ a b) 100))
(display (% 170 200))
(display a)
(define (make-averager)
    (define count 0)
    (define total 0)
    (lambda (new-value)
        (set! count (+ count 1))
        (set! total (+ total new-value))
        (/ total count)
    )
)
(define avg (make-averager))
(display (avg 10))
(display (avg 11))
(display (avg 15))

(define x̄ (λ (a b) (/ (+ a b) 2)))
(display (x̄ 25 26))

)"""

# pgm="""(
# (define (make-averager)
#     (define count 0)
#     (define total 0)
#     (lambda (new-value)
#         (set! count (+ count 1))
#         (set! total (+ total new-value))
#         (/ total count)
#     )
# )

# (define avg (make-averager))

# (display (avg 10))
# (display (avg 11))
# (display (avg 15))

# )"""

# pgm="""(
# (define (% a b) (* (/ a b) 100))
# (display (% 170 200))
# )"""

env = get_initial_env()
for statement in parse(pgm):    # type:ignore
    res = evaluate(statement, env)
    if res is not None:
        print(res)

#print(env)
