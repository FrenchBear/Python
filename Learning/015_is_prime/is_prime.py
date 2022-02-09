# is_prime

def is_prime(x):
    if x<=3: return True
    if x%2==0: return False
    c = 3
    while c*c<=x:
        if x%c==0: return False
        c += 2
    return True

l = [n for n in range(2,100) if is_prime(n)]
print(l)
