# roman.py
# Handle roman numbers conversions
#
# 2023-04-10    PV      First version

from tokenizer import *

Tokens: list[Token]
RomanDigits: dict[int, str]
StatesDataObject: StatesData

def init_roman():
    global Tokens, RomanDigits, StatesDataObject

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

    Tokens = []
    AddTokens(1, 'I', 'V', 'X')
    AddTokens(10, 'X', 'L', 'C')
    AddTokens(100, 'C', 'D', 'M')
    AddTokens(1_000, 'M', 'V̄', 'X̄')
    AddTokens(10_000, 'X̄', 'L̄', 'C̄')
    AddTokens(100_000, 'C̄', 'D̄', 'M̄')
    Tokens.append(Token('M̄', 1_000_000))
    Tokens.append(Token('M̄M̄', 2_000_000))
    Tokens.append(Token('M̄M̄M̄', 3_000_000))

    # Build a convenient int -> str digits map
    RomanDigits = {t.Value: t.Str for t in Tokens}

    StatesDataObject = BuildStatesData(Tokens)
    DumpStatesTable(StatesDataObject)


def RomanToInt(s: str) -> int:
    global StatesDataObject
    pos = 0
    val = 0
    while True:
        (t, nextPos) = GetTokenUsingDic(StatesDataObject, s, pos)
        if t == 0:
            return val
        if t < 0:
            print(f'Syntax error (token not found) pos={pos}')
            breakpoint()
        val += t
        pos = nextPos

def IntToRoman(value: int) -> str:
    res = ''
    if not 0<=value<4_000_000:
        raise ValueError('IntToRoman: value must be in [0..4_000_000[')
    m = 1_000_000
    while m>0:
        d = value//m
        value %= m
        if d>0:
            res += RomanDigits[d*m]
        m //= 10
    return res