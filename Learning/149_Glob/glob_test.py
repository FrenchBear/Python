# glob_test.py
# Test of globbing in Python using pathlib
#
# 2027-07-15    PV

from pathlib import Path

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
