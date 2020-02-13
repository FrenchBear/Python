# LSystem, Générateur L-System en Python
# 2018-03-09 PV

import sys
import numpy as np
import matplotlib.pyplot as plt

class SystemDefinition(object):
    def __init__(self, argname):
        self.name = argname
        self.rules = {}

    def __str__(self):
        s = self.name + "{\n" + "  Angle " + str(self.angle) + "\n  Axiom " + self.axiom + '\n'
        for k,i in self.rules.items():
            s += "  " + k + ": " + i + '\n'
        s += '}'
        return s


dicsd = {}
with open("fractint.l", 'r') as f:
    for line in f:
        line = line.strip()                 # Remove final \r\n
        p = line.find(';')                  # Remove comment
        if p >= 0: line = line[:p].strip()
        if len(line) == 0: continue           # Ignore white lines

        p = line.find('{')                  # Start a definition?
        if p >= 0:
            name = line[:p].strip()
            sd = SystemDefinition(name)
            dicsd[name] = sd
            continue
    
        token = "angle"
        if line[:len(token)].lower() == token:
            sd.angle = int(line[len(token):].strip('='))
            continue
        token = "axiom"
        if line[:len(token)].lower() == token:
            sd.axiom = line[len(token):].strip('=').strip().upper()
            continue
        p = line.find('=')
        if p > 0:
            letter = line[:p].strip().upper()
            expansion = line[p + 1:].strip().upper()
            sd.rules[letter] = expansion
            continue
        if line == '}':
            sd = None
            continue
        print(line)
        assert(False)


# Recursive iterator implementation
# Not the fastest, but for this example, good enough
def LSystemIterator(depth, axiom, rules):
    """Implements a L-System engine using a recursive iterator model
    that uses little memory for complex/deep systems"""
    # End recursivity case, depth==0, simply returns axiom
    if depth == 0:
        for c in axiom:
            yield c
    else:
        # General case, apply transformation rules on depth-1 version
        for c in LSystemIterator(depth - 1, axiom, rules):
            if c in rules:
                for c2 in rules[c]:
                    yield c2
            else:
                yield c

# matplotlib will automatically take care of boundaries management
# Just assume here we start at (0, 0) and all segments have a length of one unit
def PlotLSystem(rule, level, name, angle):
    x, y = 0.0, 0.0
    a = 0
    dx = np.cos(np.linspace(0.0, 2 * np.pi, angle, endpoint=False))
    dy = -np.sin(np.linspace(0.0, 2 * np.pi, angle, endpoint=False))

    px = [x]
    py = [y]

    for c in rule:
        if c == '+': a += 1
        if c == '-': a -= 1
        if c == 'F':
            x += dx[a % angle]
            y += dy[a % angle]
            px.append(x)
            py.append(y)

    print("Rendering")
    plt.figure(num=None, figsize=(10, 7), dpi=100, facecolor='w', edgecolor='k')
    plt.title(name + " level=" + str(level))
    plt.plot(px, py)
    plt.axis('off')
    plt.savefig("C:\\Temp\\" + name + str(level) + ".png", bbox_inches='tight')
    plt.show()


def GenerateAndPlot(name, level):
    sd = dicsd.get(name)
    if sd==None:
        print("LSystem: "+name+" not found in definitions.")
        print("Known definitions:")
        for name in dicsd.keys():
            print(name, end=' ')
        print()
        return

    print("Generating level", level)
    print(sd)
    generated = LSystemIterator(level, sd.axiom, sd.rules)
    print("Generation done, drawing")
    PlotLSystem(generated, level, sd.name, sd.angle)


GenerateAndPlot("Hilbert", 6)

# if __name__=="__main__":
#     if len(sys.argv)>1:
#         name = sys.argv[1]
#     else:
#        name = "Dragon"
#     if len(sys.argv)>2:
#         level = int(sys.argv[2])
#     else:
#        level = 6
#     GenerateAndPlot(name, level)
# else:
#     GenerateAndPlot("Hilbert", 6)