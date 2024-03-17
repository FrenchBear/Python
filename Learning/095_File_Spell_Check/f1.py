
with open(r'words\expressions.fr.txt', 'r', encoding='UTF-8') as f:
    dic_expressions = dict((expression.casefold(), expression) for expression in f.read().splitlines())


def proc(nn: str) -> str:
    nncf = nn.casefold()
    for expression in dic_expressions.keys():
        if expression in nncf:
            p = nncf.index(expression)
            nn = nn[:p] + dic_expressions[expression] + nn[p+len(expression):]
    return nn

print(proc("L'histoire d'alexandre le grand - Que-sais-je.epub"))
