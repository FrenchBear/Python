    # (λ (a b) (/ (+ a b) 2) )
    case ['lambda' | 'λ', [*parms], *body] if body:
        return Procedure(parms, body, env)
