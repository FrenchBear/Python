# lev.py
# Distance de Levenshtein basée sur le plus court chemin dans une grille orientée
# Programmer efficacement p.53
#
# 2022-02-17    PV
# 2022-05-25    PV      Bug fixed for i in range(n+1) -> for i in range(n+1)

# This algorithm is in O(len(x)×len(y))
# We can do better putting a cap to max edit distance s, and just compute A values at a distance at most s from diagonal
def levenshtein(x: str, y: str) -> int:
    """Retourne le nombre minimum d'insertions, suppressions ou remplacements pour aller de x à y"""
    n = len(x)
    m = len(y)
    # Initialisation du tableau, ligne 0 et colonne 0, et initialize la grille
    # Les valeurs A[i,j] for i!=0 j!=0 ne servent qu'à créer des éléments de la liste et ne sont pas significatives
    A = [[i+j for j in range(m+1)] for i in range(n+1)]
    for i in range(n):
        for j in range(m):
            A[i+1][j+1] = min(A[i][j+1]+1,                  # insertion
                              A[i+1][j]+1,                  # suppression
                              A[i][j]+int(x[i] != y[j]))    # substitution
    #print()
    #print(A)
    return A[n][m]


if __name__=='__main__':
    print(levenshtein('AUDI', 'LADA'))
