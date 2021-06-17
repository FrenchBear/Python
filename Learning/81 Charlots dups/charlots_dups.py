# Charlots_dups.py
# Liste les fichiers manquants entre la 1ère compil et la 2è
# 2021-04-10    PV

from common_fs import *
import os

first_root = r'U:\Pierre\Albums\Les Charlots'
full_root = r'U:\Pierre\A_Trier\A_Trier Brut\Les Charlots - Discographie Intégrale'

first_set = set(name.split(" - ")[3] for name in get_files(first_root) if name.endswith('.mp3'))

full_set = set(filepart(name).split(" - ")[1] for name in get_all_files(full_root) if name.endswith('.mp3'))

print("Names in first not in full:")
print(first_set-full_set)

print("Names in full not in first:")
print(full_set-first_set)
