# ch02_x24_assign_homes.py
# Essential of compilation, python ch 2, Exercise 2.5, select X86 instructions, version 2
# Keep variables names. Also "a=b" translated in "movq b, q" is potentially incorrect since movq can contain
# at most one memory reference, this will be addressed later
#
# 2025-10-10    PV      First version
# 2025-10-11    PV      v2

from ch02_x23_select_statements_v2 import *

class Compiler3(Compiler):
    ############################################################################
    # Assign homes
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
                return [Instr('movq', [Immediate(i), target])]

            case Name(id):
                return [Instr('movq', [self.select_arg(Name(id)), target])]

            case Call(Name('input_int'), []):
                return [Callq(label_name('read_int'), 0),
                        Instr('movq', [Reg('rax'), target])]

            case BinOp(left, op, right):
                x86op = 'addq' if isinstance(op, Add) else 'subq'
                if left == target:
                    # Case name = name op right
                    return [Instr(x86op, [self.select_arg(right), target])]
                elif right == target:
                    # Case name = left op name
                    return [Instr(x86op, [self.select_arg(left), target])]
                else:
                    return [Instr('movq', [self.select_arg(left), target]),
                            Instr(x86op, [self.select_arg(right), target])]

            case UnaryOp(USub(), arg):
                source = self.select_arg(arg)
                if source == target:
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

    def assign_homes(self, p: X86Program) -> X86Program:
        # Build a dictionary mapping name -> %rbp relative address
        names_dict = {}

        # First step, collect names
        for statement in p.body:
            match statement:
                case Instr(instruction, args):
                    arg: Any
                    for arg in args:
                        match arg:
                            case Name(id):
                                names_dict[id] = False

        # need stacksize*8 bytes on stack, rounded to 16 bytes multiple
        stacksize = ((len(names_dict) + 1) & 0xfffe) * 8

        # Allocate names indexes
        ix = -8
        for name in names_dict:
            names_dict[name] = ix
            ix -= 8

        # Preamble
        asm_body = []
        asm_body.append(Instr('pushq', [Reg('rbp')]))
        asm_body.append(Instr('movq', [Reg('rsp'), Reg('rbp')]))
        asm_body.append(Instr('subq', [Immediate(stacksize), Reg('rsp')]))

        # Transform names into memory references
        for statement in p.body:
            match statement:
                case Instr(instruction, args):
                    new_args = []
                    arg: Any
                    for arg in args:
                        match arg:
                            case Name(id):
                                new_args.append(Deref('rbp', names_dict[id]))
                            case _:
                                new_args.append(arg)
                    asm_body.append(Instr(instruction, new_args))

        # Postamble
        asm_body.append(Instr('addq', [Immediate(stacksize), Reg('rsp')]))
        asm_body.append(Instr('popq', [Reg('rbp')]))
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
        r = Compiler2().select_instructions(q, with_pre_post=False)
        print(str(r).lstrip())

        print("------\nAssign homes:")
        s = Compiler3().assign_homes(r)
        print(str(s).lstrip())

    program = 'x=-35000\ny=x\nprint(x+y)'
    process_program(program)
