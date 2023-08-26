# Example 2-12. Pattern matching with match/case — requires Python ≥ 3.10

def evaluate(exp: Expression, env: Environment) -> Any:
    "Evaluate an expression in an environment."
    match exp:
    # ... lines omitted
        case ['quote', x]:
            return x
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        case ['lambda', [*parms], *body] if body:
            return Procedure(parms, body, env)
        case ['define', Symbol() as name, value_exp]:
            env[name] = evaluate(value_exp, env)
        # ... more lines omitted
        case _:
            raise SyntaxError(lispstr(exp))
