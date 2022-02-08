# kmp.py
# Knuth-Morris-Pratt search algorithm
# Search yhe index of a substring in a string
#
# Code from https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
#
# 2022-02-07    PV

# Python program for KMP Algorithm
def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0]*M
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
    print(lps)

    i = 0  # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            print('Found pattern at index ' + str(i-j))
            j = lps[j-1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1


def computeLPSArray(pat, M, lps):
    len = 0  # length of the previous longest prefix suffix

    lps[0]  # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i=1 to M-1
    while i < M:
        if pat[i] == pat[len]:
            print(f'Match pat[{i=}]==pat[{len=}] and store and forward')
            len += 1
            lps[i] = len
            i += 1
            print(f'Len incremented {len=}, lps[{i=}]={len=}, i incremented {i=}')
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar to search step.
            if len != 0:
                len = lps[len-1]
                print(f'Mismatch rollback len=lps[len-1]: {len=}')
                # Also, note that we do not increment i here
            else:
                print(f'Mismatch rollback lps[{i=}]=0, increment i {i=}')
                lps[i] = 0
                i += 1

# txt = 'ABABDABACDABABCABAB'
# pat = 'ABABCABAB'


txt = 'AABAACAAABAACAABAABAC'
pat = 'AABAACAABAA'
KMPSearch(pat, txt)
