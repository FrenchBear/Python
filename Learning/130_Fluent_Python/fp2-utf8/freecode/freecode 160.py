# (lambda (a b) (/ (+ a b) 2))
case ['lambda', [*parms], *body] if body:
    return Procedure(parms, body, env)
