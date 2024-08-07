# Compte le nombre de chansons par chanteur dans un dossier
# 2017-08-17    PV

import os
import re

#source = r"C:\Users\Pierr\GoogleDrive\MusicGD\MP3P\Chansons Intl\_Divers"
source = r"C:\Users\Pierr\GoogleDrive\MusicGD\MP3P\Chansons France\_Divers"
l = [f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))]

accent_tabin_str = u'àâäéèêëîïôöûüùÿç'
accent_tabout_str = u'aaaeeeeiioouuuyc'
accent_tabin = [ord(char) for char in accent_tabin_str]
accent_table = dict(zip(accent_tabin, accent_tabout_str))


def LowerNoAccent(s):
    return s.lower().translate(accent_table)


dicChanteurs: dict[str, list[str]] = {}
for f in l:
    match = re.search(r'^(.*) - (.*)\.mp3', f, re.IGNORECASE)
    if match:
        chanteur = LowerNoAccent(match.groups(0)[0])
        if chanteur in dicChanteurs:
            dicChanteurs[chanteur].append(f)
        else:
            dicChanteurs[chanteur] = [f]
    else:
        print("No match: "+f)

# Chanteurs avec au moins 3 chansons
print([k for k in dicChanteurs.keys() if len(dicChanteurs[k]) >= 4])
