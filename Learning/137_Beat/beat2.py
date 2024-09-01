# beat2.py
# Multiproc version of beat
#
# 2024-08-31    PV

from multiprocessing import Pool
from beat import get_beat
from pprint import pprint
import contextlib
import os
from common_fs import get_all_files, extension_part

def tempo(file):
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
        beat = get_beat(file)
        return (file, beat)

# files = [
#     r"C:\MusicOD\Lists\Marche rapide\3 Luis Cobos - Zarzuela - 04 - Las Leandras, Los Nardos - El Pobre Valbuena, Pasacalle - El Rey Que.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\Chips - Having a Party.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\Hermes House Band & Tony Christie - Is This the Way to Amarillo.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\Luis Cobos - Opera Magna - 01 - Carmen Passion.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\Luis Cobos - Opera Magna - 05 - Gloire Immortelle.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\Luis Cobos - Suite 1700 - 01 - Suite 1700.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\1 Luis Cobos - Mas Zarzuelas - 01 - La Tempranica, La del Manojo de Rosas, El Amigo.mp3",
#     r"C:\MusicOD\Lists\Marche rapide\2 Luis Cobos - Tempo D'italia - 01 - Tempo d'Italia.mp3",
# ]

files = [f for f in get_all_files(r'C:\MusicOD\MP3P') if extension_part(f).lower() == ".mp3"]

if __name__ == '__main__':
    with Pool(20) as p:
        res = p.map(tempo, files)
        pprint(res, width=256)
        with open(r'C:\temp\beat.txt', 'w', encoding='utf-8') as fout:
            for (file, beat) in res:
                fout.write(f"{beat}\t{file}\n")
