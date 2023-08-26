case ['lambda', [*parms], *body] if body:
    return Procedure(parms, body, env)
