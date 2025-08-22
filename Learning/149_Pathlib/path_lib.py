# path_lib.py
# Playing with pathlib
#
# 2025-07-15    PV

from pathlib import Path
import hashlib

root = Path(r"C:\Development")

for f in root.glob("Git*/**/*.go"):
    if f.is_file():
        print(f)
print()

f = root / "GitVSTS/DevForFun/06_Generics/Go/go_generics.go"
content = f.read_text()
l = content.splitlines()
print(len(l), "lines in go_generics.go")

with f.open("r", encoding="utf-8") as fh:
    nl = 0
    for line in fh:
        nl += 1
print(nl, "lines in go_generics.go")

with f.open("r", encoding="utf-8") as fh:
    lines: list = fh.readlines()
print(len(lines), "lines in go_generics.go")
print()

print(f.stat())
print()

# Hashing (shann, md5, ...)
bytes = f.read_bytes()
digest = hashlib.md5(bytes).hexdigest()
print(digest)
print()

# hashing for big files one slice at a time using .update()
h = hashlib.md5()
with f.open('rb') as fh:
    while True:
        data = fh.read(1024) # lire par paquet de 1024 octets
        if data == b"": # il n'y a plus rien à lire dans le fichier
            break
        h.update(data) # mise à jour du hash avec la nouvelle séquence d'octets
md5sum = h.hexdigest()
print(digest)
print()

