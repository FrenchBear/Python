import operator

def mod(m: int, n: int) -> int:
    return m - (m // n * n)

def gcd(m: int, n: int) -> int:
    if n == 0:
        return m
    else:
        return gcd(n, mod(m, n))

print(gcd(18, 45))


def double(x):
    return 2*x

print(list(map(double, [1, 2, 3, 4])))

dic = {'gcd':gcd, '+':operator.add}

args = (18,45)
print(dic['gcd'](*args))
print(dic['+'](*args))
