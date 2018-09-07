# picg.py Pi compte-gouttes
# D'après Le fascinant nombre π, JP Delahaye, 2è ed, p144
# Adaptation simple en Python du compte-gouttes classique en C
#
# 2018-08-14 PV

a = 10000
c = 8400
f = [a // 5] * c
b = 0
e = 0
f.append(0)

while c > 0:
    g = 2 * c
    d = 0
    b = c
    while b > 0:
        d = d + f[b] * a
        g -= 1
        f[b] = d % g
        d //= g
        g -= 1
        b -= 1
        if b != 0:
            d *= b
    c -= 14
    print("%.4d" % (e + d // a), end='')
    e = d % a
print()
