def fsm_add(state, input):
    if state == "NC":
        if input == "00":
            return ("NC", "0")
        if input == "01" or input == "10":
            return ("NC", "1")
        if input == "11":
            return ("C", "0")
    if state == "C":
        if input == "00":
            return ("NC", "1")
        if input == "01" or input == "10":
            return ("C", "0")
        if input == "11":
            return ("C", "1")


def test_add():
    inputs = ["10", "01", "11", "00", "11", "10"]
    state = "NC"

    for input in inputs:
        (state, output) = fsm_add(state, input)
        print(output)


NS = 15


class Soldier:
    def __init__(self, id: int):
        self.id = id
        self.state = "R"  # Repos
        self.substate = 0

    def process(self, count: bool, fire: bool, rank: int) -> tuple[bool, bool, int]:
        global NS
        if self.state == "R":
            if count:
                rank += 1
                self.state = "C"
                self.substate = rank
                if self.substate == NS:
                    self.state = "F"
                    self.substate -= 1
                    fire = True
        if self.state == "C":
            if fire:
                self.state = "F"
                self.substate -= 1
            else:
                rank = self.substate
        if self.state == "F":
            if self.substate == 0:
                print(self.id, ": Fire")
                self.state = "Z"
            else:
                self.substate -= 1
        return (count, fire, rank)


soldiers: list[Soldier] = [Soldier(s + 1) for s in range(NS)]

inputs: list[tuple[bool, bool, int]] = [(s == 0, False, 0) for s in range(NS)]

time = 0
while soldiers[0].state != "Z":
    outputs: list[tuple[bool, bool, int]] = []
    time += 1

    print("time=", time, "  in = ", end="")
    for s in range(NS):
        print(soldiers[s].state, soldiers[s].substate, inputs[s], "  ", end="")
    print()

    for s in range(NS):
        outputs.append(soldiers[s].process(*inputs[s]))

    print("time=", time, " out = ", end="")
    for s in range(NS):
        print(soldiers[s].state, soldiers[s].substate, outputs[s], "  ", end="")
    print()
    print()

    for s in range(NS):
        if s == NS - 1:
            inputs[s] = (outputs[s - 1][0], outputs[s][1], outputs[s - 1][2])
        else:
            if s == 0:
                inputs[s] = (outputs[s][0], outputs[s + 1][1], 0)
            else:
                inputs[s] = (outputs[s - 1][0], outputs[s + 1][1], outputs[s - 1][2])

    if time == 50:
        break
