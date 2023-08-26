# Example 27-2. skin.py: the thumbs up emoji by itself, followed by all available skin tone modifiers.

from unicodedata import name

SKIN1 = 0x1F3FB  # EMOJI MODIFIER FITZPATRICK TYPE-1-2
SKINS = [chr(i) for i in range(SKIN1, SKIN1 + 5)]
THUMB = '\U0001F44d'  # THUMBS UP SIGN

examples = [THUMB]
examples.extend(THUMB + skin for skin in SKINS)

for example in examples:
    print(example, end='\t')
    print(' + '.join(name(char) for char in example))
