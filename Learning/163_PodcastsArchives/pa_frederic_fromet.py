# pa_frederic_fromet.py
# Download France Inter Podcasts Arcives, Frédéric Fromet
#
# 2025-10-21    PV      First version, using core

import pa_core

for p in range(24, 25):
    print("--------------------------------------")
    print(f"Page {p}\n")
    pa_core.process_page("la-chanson-de-frederic-fromet", f"https://www.radiofrance.fr/franceinter/podcasts/la-chanson-de-frederic-fromet?p={p}")
