# plsscom.py
# Plus longue sous-séquence commune
# Programmation efficace
# 2022-02-22    PV

def plsscom(x: str, y: str) -> str:
    n = len(x)
    m = len(y)

    A = [[0 for j in range(m+1)] for i in range(n+1)]
    for i in range(n):
        for j in range(m):
            if x[i] == y[j]:
                A[i+1][j+1] = A[i][j]+1
            else:
                A[i+1][j+1] = max(A[i][j+1], A[i+1][j])

    # Extract solution
    sol = []
    i, j = n, m
    while A[i][j] > 0:
        if A[i][j] == A[i-1][j]:
            i -= 1
        elif A[i][j] == A[i][j-1]:
            j -= 1
        else:
            i -= 1
            j -= 1
            sol.append(x[i])

    return ''.join(sol[::-1])


s1 = 'ABCDAE'
s2 = 'AEDBEA'
print(plsscom(s1, s2))
