# ch02_x24_assign_homes.py
# Essential of compilation, python ch 2, Exercise 2.4, assign homes, that is, replace var names by stack references
#
# 2025-10-11    PV      First version

from ch02_x23_select_statements_v2 import *

class Compiler3(Compiler):
    ############################################################################
    # Assign homes
    ############################################################################

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

                case _:
                    asm_body.append(statement)

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
