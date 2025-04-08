# Sous-programmes communs relatif au filesystem
#
# 2020-03-05    PV
# 2021-04-10    PV      Support du filesystem isolé sous common_fs.py
# 2022-01-06    PV      Version avec commentaires
# 2022-01-08    PV      basename
# 2022-05-26    PV      file_exists et folder_exists
# 2022-06-17    PV      folder_part; file_part renamed file_part; extension
# 2023-02-10    PV      file_readalltext_encoding, file_readalltext
# 2023-04-05    PV      Corrigé le commentaire d'extension; extension -> extension_part, basename -> stem_part
# 2024-02-12    PV      Argument optionnel fullpath for get_files and get_folders
# 2024-02-28    PV      @deprecated
# 2025-04-07    PV      basename renamed stem, it was a mistake, Unix basename command/call returns file+ext without path

# Function 	        Copies      Copies          Uses file       Destination
#                   metadata 	permissions 	object 	        may be directory
# shutil.copy 	    No          Yes             No              Yes
# shutil.copyfile 	No          No              No              No
# shutil.copy2 	    Yes         Yes             No              Yes
# shutil.copyfileobjNo          No              Yes             No

# os.rmdir() does not remove non-empty directories, use shutil.rmtree(path) instead
# os.makedirs(folder) creates all parent directories if needed

'''Sous-programmes communs relatif au filesystem'''

import os
import codecs
from typing import Iterable
from typing_extensions import deprecated


def get_files(source: str, fullpath: bool = False) -> list[str]:
    '''Retourne juste les fichiers d'un dossier, noms.ext sans chemins sauf si fullpath est True'''
    _1, _2, files = next(os.walk(source))
    if fullpath:
        return [os.path.join(source, file) for file in files]
    else:
        return files


def get_folders(source: str, fullpath: bool = False) -> list[str]:
    '''Retourne juste les sous-dossiers d'un dossier, noms sans chemins sauf si fullpath est True'''
    _1, folders, _2 = next(os.walk(source))
    
    if fullpath:
        return [os.path.join(source, folder) for folder in folders]
    else:
        return folders


def get_all_files(path: str) -> Iterable[str]:
    '''Retourne un itérateur produisant tous les fichiers à partir d'une racine, chemin complet'''
    for root, subs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)


def get_all_folders(path: str) -> Iterable[str]:
    '''Retourne un itérateur produisant tous les dossiers à partir d'une racine, chemin complet'''
    for root, folders, _ in os.walk(path):
        for folder in folders:
            yield os.path.join(root, folder)

# Simple helpers
def file_part(fullpath: str) -> str:
    '''Retourne un nom de fichier sans son chemin'''
    _, file = os.path.split(fullpath)
    return file


def folder_part(fullpath: str) -> str:
    '''Retourne un nom de dossier sans le fichier'''
    folder, _ = os.path.split(fullpath)
    return folder


@deprecated("Utiliser stem_part")
def stem(filewithext: str) -> str:
    '''Retourne le nom de fichier sans extension (n'enlève pas le chemin éventuel). DEPRECIÉ - Utiliser stem_part'''
    stem, _ = os.path.splitext(filewithext)
    return stem


def stem_part(filewithext: str) -> str:
    '''Retourne le nom de fichier sans extension (n'enlève pas le chemin éventuel)'''
    stem, _ = os.path.splitext(filewithext)
    return stem


@deprecated("Utiliser extension_part")
def extension(filewithext: str) -> str:
    '''Retourne l'extension du fichier, point inclus. DEPRECIÉ - Utiliser extension_part'''
    _, ext = os.path.splitext(filewithext)
    return ext


def extension_part(filewithext: str) -> str:
    '''Retourne l'extension du fichier, point inclus'''
    _, ext = os.path.splitext(filewithext)
    return ext


def file_exists(fullpath: str) -> bool:
    '''Teste si un fichier existe'''
    return os.path.exists(fullpath) and os.path.isfile(fullpath)


def folder_exists(fullpath: str) -> bool:
    '''Teste si un dossier existe'''
    return os.path.exists(fullpath) and os.path.isdir(fullpath)


def file_size(fullpath: str) -> int:
    '''Retourne la taille d'un fichier en octets'''
    return os.stat(fullpath).st_size

def file_readalltext_encoding(filepath: str) -> tuple[str, str]:
    '''Lit tout le texte d'un fichier en détectant le type de fichier automatiquement
       Retourne (texte, encodage)
       Encodage est 'utf_8_sig', 'utf_8' ou 'mbcs' (ANSI)
    '''
    data = open(filepath, "rb").read()
    if data.startswith(codecs.BOM_UTF8):
        return (codecs.decode(data, encoding='utf_8_sig', errors='strict'), 'utf_8_sig')

    # Either UTF-8 without BOM or ANSI
    # Since UTF-8 is strict on encoding, try it first, it it fails, then assume it's ANSI
    try:
        return (codecs.decode(data, encoding='utf_8', errors='strict'), 'utf_8')
    except Exception:
        return (codecs.decode(data, encoding='mbcs', errors='strict'), 'mbcs')

def file_readalltext(filepath: str) -> str:
    '''Lit tout le texte d'un fichier en détectant le type de fichier automatiquement'''
    return file_readalltext_encoding(filepath)[0]


r'''
if __name__ == '__main__':
    from typing import Callable
    
    def test(f: Callable, arg: str, res: str):
        rc = f(arg)
        print(f"{f.__name__}(r\'{arg}\') -> {rc}    {'Ok' if rc==res else 'Problem'}")

    test(file_part,   r'c:\temp\f1.txt',                    r'f1.txt')
    test(folder_part, r'c:\temp\f1.txt',                    r'c:\temp')
    test(stem_part,   r'nom_de_fichier.ext',                r'nom_de_fichier')
    test(stem_part,   r'fichier',                           r'fichier')
    test(stem_part,   r'c:\p\nom_de_fichier.ext',           r'c:\p\nom_de_fichier')
    test(stem_part,   r'c:\p1.p2\file',                     r'c:\p1.p2\file')
    test(file_part,   r'C:AUTOEXEC.BAT',                    r'AUTOEXEC.BAT')
    test(folder_part, r'C:AUTOEXEC.BAT',                    r'C:')
    test(stem_part,   r'C:AUTOEXEC.BAT',                    r'C:AUTOEXEC')
    test(stem_part,   r'C:AUTOEXEC.BAT',                    r'C:AUTOEXEC')
    test(file_part,   r'C:\AUTOEXEC.BAT',                   r'AUTOEXEC.BAT')
    test(folder_part, r'C:\AUTOEXEC.BAT',                   'C:\\')
    test(stem_part,   r'C:\AUTOEXEC.BAT',                   r'C:\AUTOEXEC')
    test(file_part,   r'C:\P\AUTOEXEC.BAT',                 r'AUTOEXEC.BAT')
    test(folder_part, r'C:\P\AUTOEXEC.BAT',                 r'C:\P')
    test(stem_part,   r'C:\P\AUTOEXEC.BAT',                 r'C:\P\AUTOEXEC')
    test(file_part,   r'AUTOEXEC.BAT',                      r'AUTOEXEC.BAT')
    test(folder_part, r'AUTOEXEC.BAT',                      r'<empty string>')
    test(stem_part,   r'AUTOEXEC.BAT',                      r'AUTOEXEC')
    test(file_part,   r'\AUTOEXEC.BAT',                     'AUTOEXEC.BAT')
    test(folder_part, r'\AUTOEXEC.BAT',                     '\\')
    test(stem_part,   r'\AUTOEXEC.BAT',                     r'\AUTOEXEC')
    test(file_part,   r'\\Server\Share\Path\File.ext',      r'File.ext')
    test(folder_part, r'\\Server\Share\Path\File.ext',      r'\\Server\Share\Path')
    test(stem_part,   r'\\Server\Share\Path\File.ext',      r'\\Server\Share\Path\File')
    test(stem_part,   r'\\Server\Share\Path\File.ext',      r'\\Server\Share\Path\File')
'''
