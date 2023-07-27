from common_fs import get_folders

source = r'W:\TempBD\final'


diffMax = 1
# Adapted from https://en.wikipedia.org/wiki/Levenshtein_distance and personal app DiffMP3Names


def levenshtein_distance(s: str, t: str):
    # Optimisation perso, j'ai pas besoin des distances supérieures à diffMax
    if abs(len(s) - len(t)) > diffMax:
        return diffMax + 1

    # degenerate cases
    if s == t:
        return 0
    if len(s) == 0:
        return len(t)
    if len(t) == 0:
        return len(s)

    # # convert to lowercase, we're doing case insensitive compare here
    # s = s.lower()
    # t = t.lower()

    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    v0 = list(range(len(t)+1))
    v1 = [0] * (len(t)+1)

    for i in range(len(s)):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]


folders = get_folders(source)
print(f'{len(folders)} dossiers à analyser')
with open("folders_dist1.txt", 'w', encoding='utf-8') as out:
    for i in range(len(folders)):
        for j in range(i+1, len(folders)):
            if levenshtein_distance(folders[i], folders[j]) <= 1:
                print(f"{folders[i]:<40} {folders[j]}")
                out.write("("+repr(folders[i])+", "+repr(folders[j])+"),\n")
