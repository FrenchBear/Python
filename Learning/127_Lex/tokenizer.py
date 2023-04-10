# Lex tokenizer
# Efficient tokenizer
#
# 2023-04-10    PV      First version

from dataclasses import dataclass
from operator import itemgetter
from typing import Tuple


@dataclass
class Token:
    Str: str
    Value: int


@dataclass
class Decision:
    NextState_Or_TokenValue: int
    Length: int


class StatesData:
    def __init__(self) -> None:
        self.DecisionsDic = dict()


class ListAndRollback:
    def __init__(self) -> None:
        self.RollbackLength: int = 0
        self.TerminalTokenValue: int = 0
        self.Tokens: list[Token] = []


stateGen: int


def BuildStatesData(Tokens: list[Token]) -> StatesData:

    def BuildStatesDictionary(decisions: dict[int, Decision], tokens: list[Token], pos: int, rollbackTokenValue: int, rollbackLength: int):
        nonlocal stateGen
        state = stateGen
        stateGen += 1

        # Build counter of next letter
        nextLetter: dict[int, ListAndRollback] = dict()
        for t in tokens:
            c = ord(t.Str[pos])
            if not c in nextLetter:
                nextLetter[c] = ListAndRollback()
            if pos == len(t.Str) - 1:
                assert nextLetter[c].TerminalTokenValue == 0
                assert nextLetter[c].RollbackLength == 0
                nextLetter[c].RollbackLength = len(t.Str)
                nextLetter[c].TerminalTokenValue = t.Value
            else:
                nextLetter[c].Tokens.append(t)

        for (c, lrb) in nextLetter.items():
            if len(lrb.Tokens) == 0:
                assert lrb.TerminalTokenValue > 0
                decisions[(state << 16) + c] = Decision(-lrb.TerminalTokenValue, lrb.RollbackLength)
            else:
                rtv = rollbackTokenValue
                rl = rollbackLength
                if lrb.TerminalTokenValue > 0:
                    rtv = lrb.TerminalTokenValue
                    rl = lrb.RollbackLength
                decisions[(state << 16) + c] = Decision(stateGen, 0)
                BuildStatesDictionary(decisions, lrb.Tokens, pos + 1, rtv, rl)

        if rollbackTokenValue > 0:
            decisions[(state << 16) + ord('$')] = Decision(-rollbackTokenValue, rollbackLength)

    stateGen = 0
    data = StatesData()
    BuildStatesDictionary(data.DecisionsDic, Tokens, 0, 0, 0)
    return data


def DumpStatesTable(data: StatesData):
    print("State Char Decision")
    print("----- ---- ----------------------------------")

    for (k, v) in sorted(data.DecisionsDic.items(), key=itemgetter(0)):
        state = k >> 16
        c = chr(k & 0xFFFF)
        print(f"{state:<5} {c}    ", end='')
        if v.NextState_Or_TokenValue > 0:
            print(f"State {v.NextState_Or_TokenValue}")
        elif v.NextState_Or_TokenValue < 0:
            print(f"Token {-v.NextState_Or_TokenValue} length {v.Length}")
    print()

# Return: 0: end of string, -1: no token recognized, otherwise token value


def GetTokenUsingDic(data: StatesData, s: str, pos: int) -> Tuple[int, int]:
    nextPos = pos
    if pos == len(s):
        return (0, 0)
    if pos < 0 or pos > len(s):
        raise IndexError(pos)

    state = 0
    while True:
        c: str
        if pos < len(s):
            c = s[pos]
            pos += 1
        else:
            c = '$'
        ix = (state << 16) + ord(c)
        if ix in data.DecisionsDic:
            d = data.DecisionsDic[ix]
            if (d.NextState_Or_TokenValue > 0):
                state = d.NextState_Or_TokenValue
                continue
            nextPos += d.Length
            return (-d.NextState_Or_TokenValue, nextPos)
        else:
            ix = (state << 16) + ord('$')
            if ix in data.DecisionsDic:
                d = data.DecisionsDic[ix]
                nextPos += d.Length
                return (-d.NextState_Or_TokenValue, nextPos)

        return (-1, nextPos)
