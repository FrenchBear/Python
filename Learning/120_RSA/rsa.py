# Rrsa.py
# Decryptage du vote, 15 énigmes ludiques pour s'initier à la programmation Python, chap 8
#
# 2023-01-27    PV

# Source: https://www.dcode.fr/exponentiation-modulaire
# base b, exponent e, modulus m (calcule b^e mod m)
def powmod(b: int, e: int, m: int) -> int:
    r = 1
    b = b % m
    if b == 0:
        return 0
    while e > 0:
        if e % 2:
            r = (r * b) % m
        e = e >> 1
        b = (b ** 2) % m
    return r
# print(powmod(11,13,19))

def rapide_exp(x,n,p) : # Calcul de x^n mod p
    if n==1:
        return x % p
    else:
        if n %2==0:
            return rapide_exp((x*x)%p,n//2,p)
        else:
            return x*rapide_exp((x*x)%p,n//2,p) %p
# print(rapide_exp(11,13,19))

def encode_str(s: str) -> int:
    n = 0
    for c in s:
        n = (1000*n)+ord(c)
    return n
# print(encode_str("Python"))


def decode_num(n: int) -> str:
    s = ''
    while n > 0:
        n1 = n % 1000
        s = chr(n1) + s
        n //= 1000
    return s
# print(decode_num(encode_str("Python")))


e, n = 15213133, 881856821380357         # Clé publique

C = 229446820549265

M1 = "OUI"
M2 = "NON"
M3 = "BLANC"

print(M1, encode_str(M1), powmod(encode_str(M1), e, n), powmod(encode_str(M1), e, n)==C)
print(M2, encode_str(M2), powmod(encode_str(M2), e, n), powmod(encode_str(M2), e, n)==C)
print(M3, encode_str(M3), powmod(encode_str(M3), e, n), powmod(encode_str(M3), e, n)==C)

