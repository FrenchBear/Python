# find_efficient_word.py
# Play with wordle
#
# 2022-02-03    PV

with open(r'words.txt', encoding='UTF-8') as f:
    words = {mot for mot in f.read().splitlines()}

print(len(words))
