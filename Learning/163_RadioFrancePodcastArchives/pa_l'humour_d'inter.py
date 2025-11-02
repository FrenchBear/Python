# pa_l'humour_d'inter.py
# Download France Inter Podcasts Arcives, L'humour d'Inter
#
# 2025-11-02    PV      First version, using core

import pa_core

for p in range(11, 100):
    print("--------------------------------------")
    print(f"Page {p}\n")
    pa_core.process_page("C:\\MusicOD2\\Podcasts\\Archives l'humour d'inter\\<serie>", f"https://www.radiofrance.fr/franceinter/podcasts/bouquet-l-humour-d-inter?p={p}")
