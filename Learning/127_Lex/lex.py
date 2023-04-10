# Lex
# Efficient tokenizer
#
# 2023-04-10    PV      First version

from dataclasses import dataclass
from operator import itemgetter
from tokenizer import *

Tokens: list[Token] = []


def AddTokens(base: int, one: str, five: str, ten: str):
    Tokens.append(Token(one, base))
    Tokens.append(Token(one+one, 2*base))
    Tokens.append(Token(one+one+one, 3*base))
    Tokens.append(Token(one+five, 4*base))
    Tokens.append(Token(five, 5*base))
    Tokens.append(Token(five+one, 6*base))
    Tokens.append(Token(five+one+one, 7*base))
    Tokens.append(Token(five+one+one+one, 8*base))
    Tokens.append(Token(one+ten, 9*base))


AddTokens(1, 'I', 'V', 'X')
AddTokens(10, 'X', 'L', 'C')
AddTokens(100, 'C', 'D', 'M')
Tokens.append(Token('M', 1000))
Tokens.append(Token('MM', 2000))
Tokens.append(Token('MMM', 3000))

# print(Tokens)

statesData = BuildStatesData(Tokens)
print(statesData)
DumpStatesTable(statesData)

s = "MCMLXV"
pos = 0
val = 0
while True:
    (t, nextPos) = GetTokenUsingDic(statesData, s, pos)
    if t == 0:
        print('Value:', val)
        break
    if t < 0:
        print(f'Syntax error (token not found) pos={pos}')
        break
    print(t)
    val += t
    pos = nextPos
