# kmp.py
# Knuth-Morris-Pratt search algorithm
# Search yhe index of a substring in a string
#
# Code from https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
#
# 2022-02-07    PV

def KMPSearch(txt, pat, lps=None):
    M = len(pat)
    N = len(txt)

    # Preprocess the pattern (calculate lps[] array)
    if not lps:
        lps = computeLPSArray(pat)
        print(lps)

    i = 0  # index for txt[]
    j = 0  # index for pat[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            print('Found pattern at index', i-j)
            j = lps[j-1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters, they will match anyway
            if j != 0:
                j = lps[j-1]
            else:
                i += 1


def computeLPSArray(pat: str, verbose=False) -> list[int]:
    M = len(pat)
    # create lps[] that will hold the longest prefix suffix values for pattern
    lps = [0]*M

    length = 0  # length of the previous longest prefix suffix

    # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i=1 to M-1
    while i < M:
        if pat[i] == pat[length]:
            if verbose:
                print(f'Match pat[{i=}]==pat[{length=}]')
            length += 1
            if verbose:
                print(f'Len incremented {length=}, lps[{i=}]=length, ++i={i+1}')
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # Since we don't match but still have a non-zero match in progress, try again reducing length
                if verbose:
                    print(f'Mismatch rollback length=lps[length-1={length-1}]={lps[length-1]}')
                length = lps[length-1]
                # Note that we do not increment i here
            else:
                if verbose:
                    print(f'Mismatch reset lps[{i=}]=0, ++i={i+1}')
                lps[i] = 0
                i += 1
    
    return lps

# txt = 'ABABDABACDABABCABAB'
# pat = 'ABABCABAB'


#txt = 'AABAACAAABAACAABAABAC'
#pat = 'AABAACAABAAB'

txt = 'BCDDABDDABBCDDDDAABBBBBBCDABBCAACCCCCDDACDDAAAAAAACABBBBBCDAAAAAABCDACCCAAAABBCC'
pat = 'CDAACD'
KMPSearch(txt, pat)
