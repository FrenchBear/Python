case ['define', [Symbol() as name, *parms], *body] if body:
    env[name] = Procedure(parms, body, env)
