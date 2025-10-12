# ch02_x25_patch_instructions.py
# Essential of compilation, python ch 2, Exercise 2.5, patch incorrect instructions
#
# 2025-10-11    PV      First version

from ch02_x24_assign_homes import *

class Compiler4(Compiler):
    ############################################################################
    # Patch statements
    ############################################################################

    def patch_instructions(self, p: X86Program) -> X86Program:
        asm_body = []
        for statement in p.body:
            match statement:
                case Instr(instruction, args):
                    match args:
                        case (Immediate(n), Deref(reg, offset)):
                            if n<-32768 or n>32767:
                                asm_body.append(Instr('movq', [Immediate(n), Reg('rax')]))
                                asm_body.append(Instr(instruction, [Reg('rax'), Deref(reg, offset)]))
                                continue
                            asm_body.append(statement)

                        case (Deref(reg1, offset1), Deref(reg2, offset2)):
                            asm_body.append(Instr('movq', [Deref(reg1, offset1), Reg('rax')]))
                            asm_body.append(Instr(instruction, [Reg('rax'), Deref(reg2, offset2)]))
                            continue
                        case _:
                            asm_body.append(statement)
                case _:
                    asm_body.append(statement)

        x86p = X86Program(asm_body)
        return x86p


if __name__ == '__main__':
    def process_program(program):
        print("------------------------------------")
        print("Original program:\n", program, sep='')
        p = ast.parse(program)

        print("\n------\nAfter removing complex expressions:")
        q = Compiler2().remove_complex_operands(p)
        print(ast.unparse(q))

        print("\n------\nX86 code generation:")
        r = Compiler2().select_instructions(q, with_pre_post=False)
        print(str(r).lstrip())

        print("------\nAssign homes:")
        s = Compiler3().assign_homes(r)
        print(str(s).lstrip())

        print("------\nPatch instructions:")
        t = Compiler4().patch_instructions(s)
        print(str(t).lstrip())

    #program = 'x=35000\ny=25000\nprint(x+y)'
    program = "x=12+8\nprint(x)"
    process_program(program)
